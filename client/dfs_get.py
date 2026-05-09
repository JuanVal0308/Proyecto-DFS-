import requests
import sys

NAMENODE_URL = "http://52.23.74.126:8000"

filename = sys.argv[1]

# obtener metadata
response = requests.get(
    f"{NAMENODE_URL}/files/{filename}"
)

metadata = response.json()

blocks = metadata["blocks"]

output_file = f"downloaded_{filename}"

with open(output_file, "wb") as outfile:

    for block in blocks:

        block_id = block["block_id"]
        datanode_url = block["datanode_url"]

        print(f"Downloading {block_id}...")

        block_response = requests.get(
            f"{datanode_url}/block/{block_id}"
        )

        outfile.write(
            block_response.content
        )

print(f"File reconstructed: {output_file}")
