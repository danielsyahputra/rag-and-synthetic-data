import os
import uuid

import openai
import requests
from dotenv import load_dotenv

load_dotenv()


class OpenAIWrapper:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.models = ["gpt-4o", "gpt-3.5-turbo-1106"]
        self.model_index = 0
        self.model = self.models[self.model_index]
        self.client = openai.OpenAI()
        self.convos = dict()

    def retry(func):
        def wrapper(self, *args, **kwargs):
            while self.model_index < len(self.models) - 1:
                try:
                    result = func(self, *args, **kwargs)
                    return result
                except Exception as e:
                    print(f"Error with model {self.model}: {str(e)}")
                    print(f"Switching to the next model in {self.models}")
                    self.model_index += 1
                    self.model = self.models[self.model_index]
            else:
                raise Exception(f"All models in {self.models} have been tried")

        return wrapper

    @retry
    def start_convo(self, system):
        convo_id = str(uuid.uuid4())
        self.convos[convo_id] = [{"role": "system", "content": system}]
        return convo_id

    @retry
    def msg_in_convo(self, convo_id, prompt):
        self.convos[convo_id].append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model=self.model, messages=self.convos[convo_id]
        )
        text = response.choices[0].message.content.strip()
        self.convos[convo_id].append({"role": "assistant", "content": text})
        return text

    @retry
    def ask_question_in_convo(self, convo_id, question):
        question += "Answer with only a single word: 'True' or 'False'"
        self.convos[convo_id].append({"role": "user", "content": question})
        response = self.client.chat.completions.create(
            model=self.model, messages=self.convos[convo_id]
        )
        text = response.choices[0].message.content.strip()
        response = True
        if text.lower() == "true":
            response = True
        elif text.lower() == "false":
            response = False
        else:
            raise Exception("Respose is not a bool")

        self.convos[convo_id].append({"role": "assistant", "content": text})
        return response

    @retry
    def generate_photo(self, photo_prompt):
        improved_gpt_prompt = f"A positive image of: {photo_prompt}, rendered artistically in a chic, cartooney, minimalistic style"
        response = self.client.images.generate(
            model="dall-e-2",
            prompt=improved_gpt_prompt,
            size="512x512",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        return img_data
