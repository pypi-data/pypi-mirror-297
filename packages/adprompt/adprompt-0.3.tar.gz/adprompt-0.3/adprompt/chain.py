from abc import ABCMeta, abstractmethod
from typing import Optional, List

from openai.types.chat import ChatCompletion

from adprompt.chat_model import ChatResponse


class BaseChain(metaclass=ABCMeta):
    """
    链条，做出以下定义：
    （1）当前这个链条做什么
    （2）基于当前链条的结果，确定下一个链条
    （3）无下一个链条时，获取最终结果
    """

    @abstractmethod
    def get_next_chain(self, context: dict) -> Optional['BaseChain']:
        """
        获取下一个链条
        """

    @abstractmethod
    def post_process(self, completion: ChatCompletion, context: dict):
        """
        对大模型输出结果进行后处理
        """

    @abstractmethod
    def get_chat_messages(self, content: str, context: dict) -> List[dict]:
        """
        获取单轮对话的输入
        """

    @abstractmethod
    def get_final_response(self, context: dict) -> ChatResponse:
        """
        获取最终的结果
        """
