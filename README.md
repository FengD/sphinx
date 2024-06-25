# Sphinx

## Descriptions
The `Sphinx` is a mythical creature with the body of a lion and the head of a human, known for its wisdom and enigmatic nature. In ancient Egyptian mythology, the Sphinx is a symbol of strength and protection, often depicted guarding important sites. In Greek mythology, the Sphinx is famous for posing a riddle to travelers and devouring those who could not answer correctly. 

`Sphinx`, inspired by the mythical creature known for its wisdom and enigmatic nature, is an advanced AI agent that can accept audio, text, and images, and respond with a voice. Just like the legendary Sphinx who posed riddles to travelers, this AI provides insightful and intelligent interactions, making every conversation a journey of discovery.

## Technicals
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
