from model import *
from util import Util
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from pathlib import Path
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from starlette.responses import JSONResponse

import hashlib
import sys
import os

app = FastAPI()
SAVE_DIRECTORY = Path(os.getenv('AOS_SAVE_DIRECTORY') or "/tmp")


@app.get("/meta/{block_id}", response_model=ResponseMeta)
async def get_meta(block_id: str):
    response_meta = ResponseMeta()
    path = str(SAVE_DIRECTORY / block_id)
    if os.path.exists(path):
        block = Util.load(path)
        response_meta.status = "success"
        response_meta.meta = block.meta
    else:
        response_meta.status = "failed"
        response_block_data.why = "Not found {}".format(block_id)
    return response_meta


@app.get("/block/{block_id}")
async def get_block(block_id: str):
    response_block = ResponseBlock()
    path = str(SAVE_DIRECTORY / block_id)
    if os.path.exists(path):
        block = Util.load(path)
        response_block.status = "success"
        response_block.block = block
    else:
        response_block_data.why = "Not found {}".format(block_id)
        response_block.status = "failed"
    return response_block


@app.get("/block/{block_id}/data", response_model=ResponseBlockData)
async def get_block_data(block_id: str):
    response_block_data = ResponseBlockData()
    path = str(SAVE_DIRECTORY / block_id)
    if os.path.exists(path):
        response_block_data.status = "success"
        block = Util.load(path)
        response_block_data.data = block.data
    else:
        response_block_data.why = "Not found {}".format(block_id)
        response_block_data.status = "failed"
    return response_block_data


@app.delete("/block/{block_id}")
async def delete_block(block_id):
    path = str(SAVE_DIRECTORY / block_id)
    if os.path.exists(path):
        os.remove(path)
        return {"status": "success"}
    else:
        return {"status": "failed"}


@app.post("/block", response_model=ResponseMeta, status_code=HTTP_201_CREATED)
async def post_block(file: UploadFile = File(...)):
    response_meta = ResponseMeta()

    try:
        data = await file.read()
    except IOError:
        response_meta.status = "failed"
        response_meta.why = "Cannot open the uploaded file"
        return response_meta

    block_id = Util.generate_block_id()
    block = Block.create(block_id, data, file)
    path = str(SAVE_DIRECTORY / block_id)
    if os.path.exists(path):
        response_meta.status = "failed"
        response_meta.why = "Duplicated filename. Please try again!"
        return response_meta
    try:
        Util.dump(path, block)
    except IOError:
        response_meta.status = "failed"
        response_meta.why = "Cannot create a file"
        return response_meta

    response_meta.status = "success"
    response_meta.meta = block.meta
    return response_meta
