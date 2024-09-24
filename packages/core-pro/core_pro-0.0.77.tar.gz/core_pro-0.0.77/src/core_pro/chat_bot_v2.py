import base64
from openai import OpenAI
import os
import tiktoken
from colorama import Fore


class OpenAIChat:
    def __init__(self, model: str = 'gpt-3.5-turbo'):
        auth = f'{os.environ['OPENAI_USER']}:{os.environ['OPENAI_PASSWORD']}'
        self.auth = f'{base64.b64encode(auth.encode('utf-8')).decode('utf-8')}'
        self.model = model

    def completion(self, messages: list, functions: list = None):
        """
        messages = [
            {
                'role': 'system',
                'content': 'Extract information on product name'
            },
            {
                'role': 'user',
                'content': 'Tinh dầu dưỡng tóc Moroccanoil Treatment chai 10ml không box'
            }
        ]
        functions = [
            {
                'name': 'get_product_info',
                'description': 'Get product's name and size from document',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'description': 'The name of the product, e.g. SunSilk'
                        },
                        'size': {
                            'type': 'string',
                            'description': 'The size of the product, e.g. 100g'
                        },
                    },
                    'required': ['name']
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


class Calculator:
    """
    https://openai.com/api/pricing/
    """
    PRICE_PER_1K_INPUT_TOKENS = 0.01  # Placeholder: $0.01 per 1000 tokens
    PRICE_PER_1K_OUTPUT_TOKENS = 0.02
    VISUAL_TOKENS = {'low': 85, 'medium': 170, 'high': 255}
    FPS = 1  # Frames per second to process

    def __init__(self, model='gpt-4'):
        self.encoder = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str):
        return len(self.encoder.encode(text))

    def count_image_tokens(self, num_images: int, quality: str = 'medium'):
        return num_images * self.VISUAL_TOKENS[quality]

    def count_video_tokens(self, duration: int, quality: str = 'medium'):
        return int(duration * self.FPS) * self.VISUAL_TOKENS[quality]

    def calculate_cost(self, input_tokens: int, output_tokens: int):
        input_cost = (input_tokens / 1000) * self.PRICE_PER_1K_INPUT_TOKENS
        output_cost = (output_tokens / 1000) * self.PRICE_PER_1K_OUTPUT_TOKENS
        return input_cost + output_cost

    def estimate(self, prompt: str, visual_type: str, output_text='', **kwargs):
        input_text_tokens = self.count_tokens(prompt)
        output_tokens = self.count_tokens(output_text)

        quality = kwargs.get('quality', 'medium')
        if visual_type == 'image':
            num_images = kwargs.get('num_images', 1)
            visual_tokens = self.count_image_tokens(num_images, quality)
            visual_info = f'{num_images} image(s)'
        elif visual_type == 'video':
            duration = kwargs.get('duration', 0)
            visual_tokens = self.count_video_tokens(duration, quality)
            visual_info = f'{duration} seconds of video'
        else:
            raise ValueError('Invalid visual_type. Use `image` or `video`')

        total_input_tokens = input_text_tokens + visual_tokens
        total_tokens = total_input_tokens + output_tokens
        cost = self.calculate_cost(total_input_tokens, output_tokens)

        dict_cost = {
            "input_text_tokens": input_text_tokens,
            "visual_tokens": visual_tokens,
            "total_input_tokens": total_input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "estimated_cost": cost,
            "visual_info": visual_info
        }

        print(
            f'{Fore.CYAN}[OpenAI Token] Calculator :{Fore.RESET} \n'
            f'- Input text tokens: {dict_cost['input_text_tokens']} \n'
            f'- Visual tokens: {dict_cost['visual_tokens']} ({dict_cost['visual_info']}) \n'
            f'- Total input tokens: {dict_cost['total_input_tokens']} \n'
            f'- Output tokens: {dict_cost['output_tokens']} \n'
            f'- Total tokens: {dict_cost['total_tokens']} \n'
            f'- Estimated cost: ${dict_cost['estimated_cost']:.0f} \n'
        )
        if visual_type == "video":
            print(f"Note: Video estimation assumes processing {Calculator.FPS} frame(s) per second.")

        return dict_cost


# calculator = Calculator()
# visual_type = 'video'  # video
# prompt = f'Describe the {visual_type}'
#
# if visual_type == 'image':
#     num_images = 100_000
#     quality = 'medium'  # low/medium/high
#     result = calculator.estimate(prompt, visual_type, num_images=num_images, quality=quality)
# elif visual_type == 'video':
#     duration = 30 * 1_000  # video duration in seconds
#     quality = 'medium'
#     result = calculator.estimate(prompt, visual_type, duration=duration, quality=quality)
