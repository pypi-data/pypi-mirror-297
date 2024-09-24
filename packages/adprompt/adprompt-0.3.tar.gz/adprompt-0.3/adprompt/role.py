from abc import ABCMeta, abstractmethod
from typing import List

from openai.types.chat import ChatCompletion

from adprompt.chat_model import ChatResponse


class BaseRole(metaclass=ABCMeta):

    @abstractmethod
    def get_role_context(self) -> List[dict]:
        """
        获取角色构建的上下文
        """

    def get_chat_messages(self, content: str) -> List[dict]:
        messages = self.get_role_context()
        messages.append({
            'role': 'user',
            'content': content,
        })
        return messages

    def post_process(self, completion: ChatCompletion) -> ChatResponse:
        """
        对大模型输出结果进行后处理
        """
        return ChatResponse(
            content=self._get_response_content(completion),
        )

    def _get_response_content(self, completion: ChatCompletion):
        return completion.choices[0].message.content
