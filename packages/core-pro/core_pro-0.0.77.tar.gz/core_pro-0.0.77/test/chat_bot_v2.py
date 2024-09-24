import base64
from openai import OpenAI
import os
from pprint import pprint


model = "gpt-3.5-turbo"
# model = 'gpt-4o-mini'
auth = f"{os.environ['OPENAI_USER']}:{os.environ['OPENAI_PASSWORD']}"
auth = f"{base64.b64encode(auth.encode("utf-8")).decode("utf-8")}"
openai_config = {
  # "apiKey": base64.b64encode(b"app_id:secret_key").decode("utf-8"),
    "apiKey": auth,
    "baseURL": "https://gateway.mpi.test.shopee.io/api/v1/mpi/openai"
}

client = OpenAI(
    api_key=openai_config["apiKey"],
    base_url=openai_config["baseURL"]
)

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Say this is a test",
#         }
#     ],
#     model=model,
# )
#
# print(chat_completion)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "Extract information on product name"
        },
        {
            "role": "user",
            "content": "Tinh dầu dưỡng tóc Moroccanoil Treatment chai 10ml không box"
        }
    ],
    functions=[
        {
            "name": "get_product_info",
            "description": "Get product's name and size from document",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the product, e.g. SunSilk"
                    },
                    "size": {
                        "type": "string",
                        "description": "The size of the product, e.g. 100g"
                    },
                },
                "required": ["name"]
            },
        },
    ],
    model=model,
)

pprint(dict(chat_completion))
