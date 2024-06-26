import whisper
import numpy as np
import torch
torch._dynamo.config.cache_size_limit = 64
torch._dynamo.config.suppress_errors = True
torch.set_float32_matmul_precision('high')
torch.backends.cudnn.enabled = False
import ChatTTS
from IPython.display import Audio
import torchaudio


def load_stt_model(model_name: str):
    return whisper.load_model(model_name)

def audiototext(model, filename: str):
    result = model.transcribe(filename)
    return result["text"]


def load_tts_model():
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
    

    

def texttoautio(chat, params_infer_code, params_refine_text, texts : list):
    if len(texts) > 0:
        # wavs = chat.infer(texts)
        wavs = chat.infer(texts, skip_refine_text=True, params_refine_text=params_refine_text, params_infer_code=params_infer_code)
        waveforms = []
        for wav in wavs:
            waveforms.append(torch.from_numpy(wav))
        merged_waveform = torch.cat(waveforms, dim=1)
        return merged_waveform
        # torchaudio.save("output.wav", merged_waveform, 24000, format="wav")
    else:
        print(f"No response")


if __name__ == '__main__':
    # model = load_stt_model('large')
    # result = audiototext(model, 'source/test.wav')
    # print(result)
    texts = ["Nice to meet you.", "Welcome to China."]
    chat, params_infer_code, params_refine_text = load_tts_model()
    print(chat)
    wave = texttoautio(chat, params_infer_code, params_refine_text, texts)
    torchaudio.save("temp.wav", wave, 24000, format="wav")