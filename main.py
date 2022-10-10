from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from exceptions import StoryException
from router import user, article, product, file, dependencies, blog_get, blog_post
from templates import templates
from auth import authentication
from db import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from client import html
import time

# uvicorn main:app --reload  - uruchamianie aplikacji
app = FastAPI()
app.include_router(dependencies.router)
app.include_router(templates.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(authentication.router)
app.include_router(file.router)


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.name}
    )


@app.get("/")
async def get():
    return HTMLResponse(html
    )

clients = []

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


#@app.exception_handler(HTTPException)
#def custom_handler(request: Request, exc: HTTPException):
#    return PlainTextResponse(str(exc), status_code=status.HTTP_400_BAD_REQUEST)


models.Base.metadata.create_all(engine)

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
# udostępnianie katalogu file
app.mount('/file',
          StaticFiles(directory='files'),
          name='files')
app.mount('/templates/static',
          StaticFiles(directory='templates/static'),
          name='static')
