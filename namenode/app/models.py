from pydantic import BaseModel
from typing import List

class BlockMetadata(BaseModel):

    block_id: str
    datanode_url: str

class FileMetadata(BaseModel):

    filename: str
    blocks: List[BlockMetadata]
