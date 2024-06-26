from robyn import Robyn, serve_file
from robyn.robyn import Request, Response
from robyn.authentication import AuthenticationHandler, BearerGetter, Identity
import sphinx.crud as crud
from sphinx.utils import load_stt_model, audiototext, call_ollama_text, texttoaudio, load_tts_model
import traceback
import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sphinx.text_utils import clean_no_need_text, normalize_text, split_long_text
import torchaudio

app = Robyn(__file__)
model = None
sessionLocal = None
chat = None
params_infer_code = None
params_refine_text = None

class BasicAuthHandler(AuthenticationHandler):
    def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)
        try:
            payload = crud.decode_access_token(token)
            username = payload["token"]
        except Exception:
            return
        with sessionLocal() as db:
            user = crud.get_user_by_username(db, username=username)
        return Identity(claims={"user": f"{ user }"})

@app.get("/")
async def h(request):
    return f"Hello, Sphinx!"

@app.post("/users/register")
async def register_user(request):
    user = request.json()
    with sessionLocal() as db:
        created_user = crud.create_user(db, user['username'], user['password'])
    return created_user

@app.post("/users/login")
async def login_user(request):
    user = request.json()
    with sessionLocal() as db:
        token = crud.authenticate_user(db, **user)
        return token
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.post("/hi_sphinx/text")
async def hi_sphinx(request):
    try:
        body = request.body
        file = bytearray(body)
        filename = 'temp.wav'
        with open(filename, 'wb') as f:
            f.write(file)
        text = audiototext(model, filename)
        texts = call_ollama_text(prompt=text)
        if len(texts) > 0:
            texts = clean_no_need_text(texts)
            texts = normalize_text(texts)
        return texts
    except Exception as e:
        error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))
        print("Error:", error_message)

@app.post("/hi_sphinx/audio")
async def hi_sphinx(request):
    try:
        body = request.body
        file = bytearray(body)
        filename = 'temp.wav'
        with open(filename, 'wb') as f:
            f.write(file)
        text = audiototext(model, filename)
        texts = call_ollama_text(prompt=text)
        if len(texts) > 0:
            texts = clean_no_need_text(texts)
            texts = normalize_text(texts)
            texts = split_long_text(texts, 100)

        merged_waveform = texttoaudio(texts, chat, params_infer_code, params_refine_text)
        torchaudio.save("output.wav", merged_waveform, 24000, format="wav") # save the wave to local
        return serve_file("./output.wav")
    except Exception as e:
        error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))
        print("Error:", error_message)
        
def main():
    global model
    global sessionLocal
    global chat
    global params_infer_code
    global params_refine_text
    parser = argparse.ArgumentParser(description='Sphinx Application')
    parser.add_argument('--host', type=str, help='The IP address of the application', default='0.0.0.0')
    parser.add_argument('--port', type=int, help='The port of the application', default=8888)
    parser.add_argument('--database_url', type=str, help='The url of the database', default='sqlite:///./database/sphinx.db')
    parser.add_argument('--stt_model_type', type=str, help='The type of the stt model, could be tiny, base, large', default='tiny')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode')
    
    args = parser.parse_args()
    
    for key, value in vars(args).items():
        print(f'{key}: {value}')

    if args.verbose:
        print('Verbose mode is enabled')

    engine = create_engine(args.database_url)
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    model = load_stt_model(args.stt_model_type)

    chat, params_infer_code, params_refine_text = load_tts_model()

    app.configure_authentication(BasicAuthHandler(token_getter=BearerGetter()))
    app.start(host=args.host, port=args.port)

if __name__ == "__main__":
    main()
