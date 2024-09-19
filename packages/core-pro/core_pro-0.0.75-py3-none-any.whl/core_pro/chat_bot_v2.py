import base64
from openai import OpenAI
import os


class OpenAIChat:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        auth = f"{os.environ['OPENAI_USER']}:{os.environ['OPENAI_PASSWORD']}"
        self.auth = f"{base64.b64encode(auth.encode("utf-8")).decode("utf-8")}"
        self.model = model

    def completion(self, messages: list, functions: list = None):
        """
        messages = [
            {
                "role": "system",
                "content": "Extract information on product name"
            },
            {
                "role": "user",
                "content": "Tinh dầu dưỡng tóc Moroccanoil Treatment chai 10ml không box"
            }
        ]
        functions = [
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
        """
        client = OpenAI(
            api_key=self.auth,
            base_url='https://gateway.mpi.test.shopee.io/api/v1/mpi/openai'
        )

        chat_completion = client.chat.completions.create(messages=messages, functions=functions, model=self.model)
        return chat_completion
