from robyn import Robyn, WebSocket
from robyn.robyn import Request, Response
from robyn.authentication import AuthenticationHandler, BearerGetter, Identity
import crud
from sphinx.utils import load_model, audiototext
import traceback

class BasicAuthHandler(AuthenticationHandler):
    def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)

        try:
            payload = crud.decode_access_token(token)
            username = payload["token"]
        except Exception:
            return

        with models.SessionLocal() as db:
            user = crud.get_user_by_username(db, username=username)

        return Identity(claims={"user": f"{ user }"})

app = Robyn(__file__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite:///./database/sphinx.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
model = load_stt_model('large')

@app.get("/")
async def h(request):
    return f"Hello, Sphinx!"

@app.post("/users/register")
async def register_user(request):
    user = request.json()
    with models.SessionLocal() as db:
        created_user = crud.create_user(db, user['username'], user['password'])
    return created_user

@app.post("/users/login")
async def login_user(request):
    user = request.json()
    with SessionLocal() as db:
        token = crud.authenticate_user(db, **user)
        return token
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/hi_sphinx")
async def hi_sphinx(request):
    try:
        body = request.body
        file = bytearray(body)
        filename = 'temp.wav'
        with open(filename, 'wb') as f:
            f.write(file)
        print(audiototext(model, filename))
    except Exception as e:
        error_message = ''.join(traceback.format_exception(None, e, e.__traceback__))
        print("Error:", error_message)
        # raise HTTPException(status_code=404, detail="Read File Errors")
    # request = json.loads(request.body)



# websocket = WebSocket(app, "/notifications")

# @websocket.on("connect")
# async def notify_connect():
#     return "Connected to notifications"

# #@websocket.on("message")
# #async def notify_message(message):
# #    return f"Received: {message}"


# @websocket.on("message")
# async def message(ws, msg, global_dependencies) -> str:
#     websocket_id = ws.id
#     await ws.async_send_to(websocket_id, "This is a message to self")
#     return ""

# @websocket.on("close")
# async def notify_close():
#     return "Disconnected from notifications"


if __name__ == "__main__":
    app.configure_authentication(BasicAuthHandler(token_getter=BearerGetter()))
    app.start(host="0.0.0.0", port=8888)
