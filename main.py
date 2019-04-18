from model import *
from util import Util
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from starlette.responses import JSONResponse

import hashlib
import sys
import os
import redis

redis = redis.Redis(host='localhost', port=6379, db=0)
app = FastAPI()


@app.get("/meta/{block_id}", response_model=ResponseMeta)
async def get_meta(block_id: str):
    response_meta = ResponseMeta()
    path = "/tmp/{}".format(block_id)
    if os.path.exists(path):
        block = Util.load(path)
        response_meta.status = "success"
        response_meta.meta = block.meta
    else:    
        response_meta.status = "failed"
    return response_meta


@app.get("/block/{block_id}")
async def get_block(block_id: str):
    response_block = ResponseBlock()
    path = "/tmp/{}".format(block_id)
    if os.path.exists(path):
        block = Util.load("/tmp/{}".format(block_id))
        response_block.status = "success"
        response_block.block = block
    else:
        response_block.status = "failed"
    return response_block


@app.get("/block/{block_id}/data", response_model=ResponseBlockData)
async def get_block_data(block_id: str):
    response_block_data = ResponseBlockData()
    path = "/tmp/{}".format(block_id)
    if os.path.exists(path):
        response_block_data.status = "success"
        block = Util.load("/tmp/{}".format(block_id))
        response_block_data.data = block.data
    else:
        response_block_data.status = "failed"
    return response_block_data


@app.delete("/block/{block_id}")
async def delete_block(block_id):
    return {"status": "success"}


@app.post("/block", response_model=ResponseMeta, status_code=HTTP_201_CREATED)
async def post_block(file: UploadFile = File(...)):
    response_meta = ResponseMeta()

    try:
        data = await file.read()
    except:
        response_meta.status = "failed"
        return response_meta

    bid = Util.generate_block_id()
    block = Block.create(bid, data, file)

    try:
        Util.dump("/tmp/{}".format(bid), block)
    except:
        response_meta.status = "failed"
        return response_meta

    if True:
        response_meta.status = "success"
        response_meta.meta = block.meta
    else:
        response_meta.status = "failed"
    return response_meta
