import json
import os.path
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile, Form
from typing import Annotated
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
import requests

from makefunimage.upscale.upscale import make_upscale_image

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

with open('cfg.json') as f:
    config = json.load(f)


def verify_recaptcha(recaptcha_response: str) -> bool:
    url = 'https://www.google.com/recaptcha/api/siteverify'
    payload = {
        'response': recaptcha_response,
        'secret': config['auth']['secret']
    }
    response = requests.post(url, data=payload)
    result = response.json()

    return result['success']


@app.get('/')
def index():
    return FileResponse('front/index.html')


@app.post('/upscale')
def upscale(file: Annotated[UploadFile, File(description="Multiple files as bytes")], scale: Annotated[str, Form(...)],
            algorithm: Annotated[str, Form(...)], v: Annotated[str, Form(...)]):
    result = verify_recaptcha(v)
    if result:
        file_name = str(uuid.uuid4())
        out_file_path = 'uploadimg/' + file_name
        with open(out_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        try:
            result = make_upscale_image(makefile=out_file_path, alg=algorithm, scale=scale)
        except:
            remove_file(out_file_path)
        remove_file(out_file_path)
        return {'result': result}
    else:
        return {'result': 'fail'}


def remove_file(filePath):
    if os.path.isfile(filePath):
        os.remove(filePath)


@app.get('/images/{filename}')
def downloadImage(filename):
    targetFile = 'uploadimg/' + filename
    print(f'file Download : {targetFile}')
    return FileResponse(targetFile, media_type='image/png', filename=filename)
