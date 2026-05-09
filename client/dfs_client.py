import math
import requests
import sys

BLOCK_SIZE = 1024 * 1024  # 1 MB

NAMENODE_URL = "http://52.23.74.126:8000"

filename = sys.argv[1]

# calcular tamaño archivo
with open(filename, "rb") as f:

    data = f.read()

file_size = len(data)

num_blocks = math.ceil(
    file_size / BLOCK_SIZE
)

# pedir allocation
response = requests.get(
    f"{NAMENODE_URL}/files/allocate/{filename}/{num_blocks}"
)

allocation = response.json()

blocks_metadata = []

# dividir y subir bloques
for i in range(num_blocks):

    start = i * BLOCK_SIZE
    end = start + BLOCK_SIZE

    chunk = data[start:end]

    block_info = allocation["blocks"][i]

    block_id = block_info["block_id"]
    datanode_url = block_info["datanode_url"]

    temp_block = f"/tmp/{block_id}"

    with open(temp_block, "wb") as f:
        f.write(chunk)

    with open(temp_block, "rb") as f:

        files = {
            "file": f
        }

        upload = requests.post(
            f"{datanode_url}/block/upload/{block_id}",
            files=files
        )

    print(upload.json())

    blocks_metadata.append({
        "block_id": block_id,
        "datanode_url": datanode_url
    })

# registrar metadata
metadata = {
    "filename": filename,
    "blocks": blocks_metadata
}

register = requests.post(
    f"{NAMENODE_URL}/files/register",
    json=metadata
)

print(register.json())
