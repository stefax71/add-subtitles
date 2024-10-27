import os

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage


class OpenAIRefiner:
    def __init__(self, context):
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("The OPENAI_API_KEY environment variable is not set.")

        self.client = OpenAI(api_key=self.api_key)
        self.context = context


    def refine_text(self, text):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.context },
                {
                    "role": "user",
                    "content": "Please refine the following text: \n" + text + "\nproducing an output as a json with two properties: original, containing the refined text in the original language, and english, containing the refined text translated in English."
                }
            ]
        )

        return completion.choices[0].message

# api_key = os.getenv("OPENAI_API_KEY")
# print(f"API Key: {api_key}")
#
# if not api_key:
#     raise ValueError("The OPENAI_API_KEY environment variable is not set.")
#
# client = OpenAI(api_key=api_key)
#
# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": f"{self.context}"},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )
#
# print(completion.choices[0].message)