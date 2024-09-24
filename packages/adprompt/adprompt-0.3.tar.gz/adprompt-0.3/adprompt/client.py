from typing import List

from openai import OpenAI
from openai.types.chat import ChatCompletion

from adprompt.chain import BaseChain
from adprompt.chat_model import ChatResponse
from adprompt.role import BaseRole


class AdpromptClient:

    def __init__(self, base_url: str, api_key: str, model: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model

    def _chat(self, messages: List[dict], temperature: float = 0, **kwargs) -> ChatCompletion:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            **kwargs,
        )
        return completion

    def chat(self, role: BaseRole, content: str, **kwargs) -> ChatResponse:
        messages = role.get_chat_messages(content)
        completion = self._chat(messages, **kwargs)
        result = role.post_process(completion)
        return result

    def multi_turn_chat(self, chain: BaseChain, content: str, **kwargs) -> ChatResponse:
        context = {}
        result = None
        while chain is not None:
            messages = chain.get_chat_messages(content, context)
            completion = self._chat(messages, **kwargs)
            chain.post_process(completion, context)
            next_chain = chain.get_next_chain(context)
            if next_chain is None:
                result = chain.get_final_response(context)
                break
            chain = next_chain
        return result
