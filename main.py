from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

import hashlib
import sys
sys.path.append(".")
from model import *

app = FastAPI()
blocks = []
@app.get("/meta/{block_id}", response_model=ResponseMeta)
async def get_meta(block_id: int):
    response_meta = ResponseMeta()
    if 0 <= block_id < len(blocks):
        response_meta.status = "success"
        response_meta.meta = blocks[block_id].meta
    else:
        response_meta.status = "failed"
    return response_meta

@app.get("/block/{block_id}")
async def get_block(block_id: int):
    response_block = ResponseBlock()
    if 0 <= block_id < len(blocks):
        response_block.status = "success"
        response_block.block = blocks[block_id]
    else:
        response_block.status = "failed"
    return response_block

@app.get("/block/{block_id}/data", response_model=ResponseBlockData)
async def get_block_data(block_id: int):
    response_block_data = ResponseBlockData()
    if 0 <= block_id < len(blocks):
        response_block_data.status = "success"
        response_block_data.data = blocks[block_id].data
    else:
        response_block_data.status = "failed"
    return response_block_data

@app.post("/block", response_model=ResponseMeta)
async def post_block(file: UploadFile = File(...)):
    response_meta = ResponseMeta()

    try:
        data = await file.read()
    except:
        response_meta.status = "failed"
        return response_meta
    
    block = Block.create(len(blocks), data, file)
    blocks.append(block)
    
    if True:
        response_meta.status = "success"
        response_meta.meta = block.meta
    else:
        response_meta.status = "failed"
    return response_meta
