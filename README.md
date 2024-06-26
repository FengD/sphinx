# Sphinx

## 1. Descriptions
The `Sphinx` is a mythical creature with the body of a lion and the head of a human, known for its wisdom and enigmatic nature. In ancient Egyptian mythology, the Sphinx is a symbol of strength and protection, often depicted guarding important sites. In Greek mythology, the Sphinx is famous for posing a riddle to travelers and devouring those who could not answer correctly. 

`Sphinx`, inspired by the mythical creature known for its wisdom and enigmatic nature, is an advanced AI agent that can accept audio, text, and images, and respond with a voice. Just like the legendary Sphinx who posed riddles to travelers, this AI provides insightful and intelligent interactions, making every conversation a journey of discovery.

## 2. Technicals
The Sphinx is not an entirely new product; it integrates existing technologies using the [Python Robyn](https://robyn.tech/) framework to achieve identity verification and validation. Once authentication is complete, input audio can be converted to text via [Whisper](https://github.com/openai/whisper), and images can be converted to [base64](https://base64.guru/converter/encode/image) format through a base64 encode interface. The relevant inputs can be processed using the [Ollama](https://github.com/ollama/ollama/blob/main/docs/api.md) framework to call models like [LLaVA](https://huggingface.co/spaces/liuhaotian/LLaVA-1.6) or [LLaMA3 8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) for document or image-based information retrieval. Responses are then generated as voice outputs using [TTS](https://github.com/2noise/ChatTTS) technology.

The completed service can be deployed on low-cost or low-power hardware devices, like [XIAO ESP32](https://wiki.seeedstudio.com/xiao_esp32s3_bluetooth/) for data collection and interaction, and can also be connected to smart speakers for direct voice playback. If data and information security is not a concern, the entire backend service can be published as a service. For data security, offline model interaction can be implemented directly on edge devices. The segmented audio can also be used with projects like [HomeAssistant](https://github.com/geekofweek/homeassistant) for controlling smart home hardware.

Thanks for the project [Openglass](https://github.com/BasedHardware/OpenGlass) to give me the insight. And I tried to use some new tech/framework like [Robyn](https://robyn.tech/) to improve the idea.

``` mermaid
graph LR
A[User speaches] -- voice --> B[whisper]
B -- text request --> C[LLM]
F[texts/pictures] -- request --> C
C -- text response --> D[Chat-TTS]
C -- actionbyHomeAssisstant --> G[hardware]
D -- voice --> E[Earphone or Audio]
```

## 3. How to Use

### 3.1. Install the requirements

``` shell
pip install -r requirements.txt

```

* follow the [Ollama docker](https://github.com/ollama/ollama/blob/main/docs/docker.md) to launch the LLM service.

### 3.2. Execute

* use `python app.py` to launch the app. The app will launch the service, load the tts and stt model and warm up. When you see `Sphinx is ready!`, it means that the service is ready.

``` shell
(python3.8) ding@ding-Precision-3660:~/Documents/sphinx$ python app.py
INFO:robyn.logger:SERVER IS RUNNING IN VERBOSE/DEBUG MODE. Set --log-level to WARN to run in production mode.
INFO:robyn.logger:Added route HttpMethod.GET /
INFO:robyn.logger:Added route HttpMethod.POST /users/register
INFO:robyn.logger:Added route HttpMethod.POST /users/login
INFO:robyn.logger:Added route HttpMethod.POST /hi_sphinx/text
INFO:robyn.logger:Added route HttpMethod.POST /hi_sphinx/audio
host: 0.0.0.0
port: 8888
database_url: sqlite:///./database/sphinx.db
stt_model_type: large
verbose: False
INFO:ChatTTS.core:Load from cache: /home/ding/.cache/huggingface/hub/models--2Noise--ChatTTS/snapshots/c0aa9139945a4d7bb1c84f07785db576f2bb1bfa
INFO:ChatTTS.core:use cuda:0
INFO:ChatTTS.core:vocos loaded.
INFO:ChatTTS.core:dvae loaded.
INFO:ChatTTS.core:gpt loaded.
INFO:ChatTTS.core:decoder loaded.
INFO:ChatTTS.core:tokenizer loaded.
INFO:ChatTTS.core:All initialized.
INFO:ChatTTS.core:All initialized.
 NeMo-text-processing :: INFO     :: Creating ClassifyFst grammars.
INFO:NeMo-text-processing:Creating ClassifyFst grammars.
  5%|████▎                                                                                   | 100/2048 [01:09<22:33,  1.44it/s]
Sphinx is ready!
INFO:robyn.logger:Robyn version: 0.56.0
INFO:robyn.logger:Starting server at http://0.0.0.0:8888
INFO:actix_server.builder:starting 1 workers
INFO:actix_server.server:Actix runtime found; starting in Actix runtime

```

* register a user `curl -X POST -H "Content-Type: application/json" -d '{"username": "Bob", "password": "123456"}' http://localhost:8888/users/register`.
``` shell
# output:
<User(uuid=39b043b9-304d-4679-9fc7-df1d5b9b5f85, username=Bob, hashed_password=$2b$12$3XrBRJ.eLO/KaYlaridpHevwtz3fkghgfgmPotFbFAV5dzXZH7xP.)>
```

* login and get the token `curl -X POST -H "Content-Type: application/json" -d '{"username": "Noe", "password": "123456"}' http://localhost:8888/users/login`

``` shell
# output: 
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6Ik5vZSIsImV4cCI6MTcxOTM5MTY0NX0.jBgg2GJKSeehd3BD4_wJr0eVgwf52uVKqaz2WfvePhs
```

* PS: If you don't want to use authorization, remove `auth_required=True` of the service.

```python
@app.get("/auth", auth_required=True)
async def auth(request: Request):
```

* call service /hi_sphinx/audio_input `curl -X GET -H "Authorization: Bearer [replace with a valid token]" -H "Content-Type: application/json" http://localhost:8888/hi_sphinx/audio_file_input?output_type=base64  -F "file=@temp.wav"      -F "metadata={\"filename\": \"temp.wav\", \"description\": \"Sample audio file\"};type=application/json"` get the repley audio in base64.


* call service /hi_sphinx/text_input `curl -X GET -H "Authorization: Bearer [replace with a valid token]" -H "Content-Type: application/json" -d '{"prompt": "what's your name?"}' http://localhost:8888/hi_sphinx/text_input?output_type=html ` get the replay audio in html.

``` shell
# the audio contents two sentences ["Nice to meet you.", "Welcome to China."]
# use python sphinx/utils.py to generate an audio by Chat-TTS
# texts = ["Nice to meet you.", "Welcome to China."]
# chat, params_infer_code, params_refine_text = load_tts_model()
# wave = texttoaudio(texts, chat, params_infer_code, params_refine_text)
# torchaudio.save("temp.wav", wave, 24000, format="wav")
# output: 
Thank you. Its great to be here in China, and Im excited to learn more about this fascinating country and culture. Im looking forward to our conversation.
```

## 4. Demo

![](demo/demo.png)

* [More To Be Done]

## 5. Test

* use `pytest` to run the unit test


## 6. To Do List

* [x] create the audio to text service
* [x] create the audio to audio service
* [x] create the text to audio service
* [x] create a simple webui to test the service 
* [ ] create image, audio to audio service
* [ ] use XIAO ESP32 sence to get the audio
* [ ] use XIAO ESP32 sense to connect a headphone to play the voice
* [ ] use 3D printer to create a cover
* [ ] create an IOS app to display the result
* [ ] control some IoT device