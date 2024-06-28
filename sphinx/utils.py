import whisper
import torch
torch._dynamo.config.cache_size_limit = 64
torch._dynamo.config.suppress_errors = True
torch.set_float32_matmul_precision('high')
torch.backends.cudnn.enabled = False
import ChatTTS
import torchaudio
import requests
import json
import base64
import io

def load_stt_model(
    model_name: str
    ):
    """
    Load the stt models whisper is used now
    Args:
        model_name(str): The name of the model

    Returns:
        Whisper: The whisper model

    """
    return whisper.load_model(model_name)

def audiototext(
    model,
    filename: str
    ) -> str:
    result = model.transcribe(filename)
    return result["text"]


def load_tts_model():
    """
    Load the tts models ChatTTS is now used

    Returns:
        model
    """
    chat = ChatTTS.Chat()
    chat.load_models()
    spk = torch.load("source/seed_2155_restored_emb.pt")
    params_infer_code = {
        'spk_emb': spk, # add sampled speaker 
        'temperature': .3, # using custom temperature
        'top_P': 0.7, # top P decode
        'top_K': 20, # top K decode
    }

    params_refine_text = {
        'prompt': '[oral_2][laugh_0][break_6]'
    }
    return chat, params_infer_code, params_refine_text
    

def texttoaudio(
        texts : list,
        chat,
        params_infer_code,
        params_refine_text
    ):
    if len(texts) > 0:
        # wavs = chat.infer(texts) # default parameters
        wavs = chat.infer(texts, skip_refine_text=True, params_refine_text=params_refine_text, params_infer_code=params_infer_code)
        waveforms = []
        for wav in wavs:
            waveforms.append(torch.from_numpy(wav))
        merged_waveform = torch.cat(waveforms, dim=1)
        return merged_waveform
        # torchaudio.save("output.wav", merged_waveform, 24000, format="wav") # save the wave to local
    else:
        print(f"No response")

def call_ollama_text(
        prompt: str,
        images: list = None,
        model: str = 'llama3',
        is_stream=False,
        url='http://localhost:11434/api/chat'
    ) -> str:

    if images:
        payload = {
            "model": model,
            "messages":[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt, "images": images}
            ],
            "stream": is_stream
        }
    else:
        payload = {
            "model": model,
            "messages":[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "stream": is_stream
        }

    response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        texts = response.json()['message']['content']
        return texts
    else:
        print(f"Request failed with status code: {response.status_code}, Response text: {response.text}")
    return None

def wav_file_to_base64(file_path):
    with open(file_path, 'rb') as wav_file:
        wav_data = wav_file.read()
        base64_encoded = base64.b64encode(wav_data).decode('utf-8')
    return base64_encoded

def wav_tensor_to_base64(wav):
    buffer = io.BytesIO()
    torchaudio.save(buffer, wav, 24000, format="wav")
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode('utf-8')

def wav_base64_to_html(base64_string):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Embedded Base64 WAV Player</title>
    </head>
    <body>
        <audio id="audioPlayer" controls></audio>

        <script>
            // Base64 encoded WAV string
            const base64String = "{base64_string}";

            // Create a Blob from the base64 string
            const binaryString = atob(base64String);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);

            for (let i = 0; i < len; i++) {{
                bytes[i] = binaryString.charCodeAt(i);
            }}

            const blob = new Blob([bytes], {{ type: 'audio/wav' }});

            // Create a URL for the Blob and set it as the source for the audio element
            const audioUrl = URL.createObjectURL(blob);
            const audioPlayer = document.getElementById('audioPlayer');
            audioPlayer.src = audioUrl;
        </script>
    </body>
    </html>
    """.format(base64_string=base64_string)
    return html_content

if __name__ == '__main__':
    model = load_stt_model('large')
    result = audiototext(model, 'source/test.wav')
    print(result)
    texts = ["Nice to meet you.", "Welcome to China."]
    chat, params_infer_code, params_refine_text = load_tts_model()
    wave = texttoaudio(texts, chat, params_infer_code, params_refine_text)
    torchaudio.save("temp.wav", wave, 24000, format="wav")