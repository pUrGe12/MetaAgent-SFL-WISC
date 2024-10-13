import os
from openai import OpenAI, AzureOpenAI
import json
# export AZURE_OPENAI_API_KEY="d56bd868ff56401595c6e74357c02f04"
# export AZURE_OPENAI_API_BASE="https://yaolun-west.openai.azure.com/"
# Set the OPENAI_API_KEY and OPENAI_API_BASE in the environment variables
class LLM():
    def __init__(self, system_prompt="You are a helpful assistant", use_azure=True):
        self.use_azure = use_azure
        if self.use_azure:
            self.client = AzureOpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE")
            )
        else:
            self.client = OpenAI(
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_API_BASE")
            )
        self.messages = [{"role": "system", "content": system_prompt}]
        self.system_prompt = system_prompt
        self.token_cost = 0

    def chat(self, message):
        self.messages.append({"role": "user", "content": message})
        if self.use_azure:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages,
                temperature=0
            )
        else:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages,
                temperature=0
            )
        rsp = response.choices[0].message.content
        self.token_cost += response.usage.total_tokens
        return rsp

    def add_message(self, message):
        self.messages.append({"role": "user", "content": message})

    def add_tool_message(self, message):
        self.messages.append({"role": "user", "content": "[INFO] This is a tool message:\n" + message})

    def get_whole_message(self):
        return self.messages

    def get_token_cost(self):
        return self.token_cost

    def recount_token(self):
        self.token_cost = 0