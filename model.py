import hashlib
from fastapi import File, UploadFile
from pydantic import BaseModel


class Meta(BaseModel):
    original_filename: str = None
    hash_value: str = None
    block_id: str = None


class Block(BaseModel):
    meta: Meta = None
    data: bytes = None

    @classmethod
    def create(self, block_id: str, data: bytes, file: UploadFile = File(...)):
        block = Block()
        block.meta = Meta()
        block.meta.block_id = block_id
        block.meta.original_filename = file.filename
        block.meta.hash_value = hashlib.sha256(data).hexdigest()
        block.data = data
        return block


class ResponseMeta(BaseModel):
    # success or failed
    status: str = None
    meta: Meta = None


class ResponseBlock(BaseModel):
    # success or failed
    status: str = None
    block: Block = None


class ResponseBlockData(BaseModel):
    # success or failed
    status: str = None
    data: bytes = None
