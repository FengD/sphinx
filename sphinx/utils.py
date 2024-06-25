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
    model = load_stt_model('large')
    result = audiototext(model, 'source/test.wav')
    print(result)
    texts = ['如果你想了解投资理财，我强烈推薦一本经典著作A Random Walk Down Wall Street华尔街随机之旅。這本書是美國財經學家Burton G.', ' Malkiel所寫的，於1973年首次出版。它對投資理財的理解和策略進行了深入的分析和解釋。 這本書的優點在于， 1.', ' 系統性，Malkiel將投資理財的基本概念，市場定義和投资策略進行了一個系統的總結，幫助讀者對投資理財有了一個全面的理解。 2.', ' 實踐性，書中提出了多種實踐性的投资策略，例如平均投资，分散投资和價值投资等，並且對這些策略進行了詳細的分析和比較。 3.', ' 權威性，Malkiel是一位知名的財經學家，他的觀點和分析都是基於經驗和證據支持的，因此這本書的內容是可靠的和有用的。', ' 總之，A Random Walk Down Wall Street是一本經典的投資理財著作，對任何想了解投资理财的人来说都是非常重要和有用的讀物。']
    chat, params_infer_code, params_refine_text = load_tts_model()
    wave = texttoautio(chat, params_infer_code, params_refine_text, texts)
    torchaudio.save("temp.wav", wave, 24000, format="wav")