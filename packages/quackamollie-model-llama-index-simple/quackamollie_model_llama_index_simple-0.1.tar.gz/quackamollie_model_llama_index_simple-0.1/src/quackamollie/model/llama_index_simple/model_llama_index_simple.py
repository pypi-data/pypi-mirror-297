# -*- coding: utf-8 -*-
__all__ = ["SimpleLlamaIndexQuackamollieModel"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from ast import literal_eval
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.chat_engine.simple import SimpleChatEngine
from llama_index.core.chat_engine.types import StreamingAgentChatResponse
from llama_index.llms.ollama import Ollama
from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings
from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.model.meta.llama_index.llama_index_meta_model import MetaLlamaIndexQuackamollieModel
from typing import AsyncIterable, List, Optional, Tuple

from quackamollie.model.llama_index_simple.prompt.llama_index_simple_prompt import llama_index_simple_context


class SimpleLlamaIndexQuackamollieModel(MetaLlamaIndexQuackamollieModel):
    """ Simple Llama-Index model with chat history, managed by `LlamaIndexQuackamollieModelManager` """

    model_families: List[ModelFamilyIcon] = [ModelFamilyIcon.LLAMA_INDEX]
    DEFAULT_OLLAMA_BASE_MODEL: str = "llama3"

    def __init__(self, model_config: Optional[str] = None):
        """ Initialize the model with model additional configuration retrieved from the database

            :param model_config: Additional configuration given as a string through CLI or Telegram `App Settings`
                                 and retrieved from the database
            :type model_config: Optional[str]
        """
        super().__init__(model_config=model_config)

        # Get config for ollama base URL
        quackamollie_settings: QuackamollieSettings = get_settings_from_context()

        # Get Ollama model name
        ollama_base_model: str = self.DEFAULT_OLLAMA_BASE_MODEL
        if model_config:
            model_config_dict = literal_eval(model_config)
            if isinstance(model_config_dict, dict):
                ollama_base_model = model_config_dict.get("ollama_base_model", self.DEFAULT_OLLAMA_BASE_MODEL)

        # Initialize LLM model
        self.llm = Ollama(base_url=quackamollie_settings.ollama_base_url, model=ollama_base_model,
                          request_timeout=3600.0)
        self.prefix_messages = [ChatMessage(role="system", content=llama_index_simple_context)]

        # Initialize the chat engine
        self.chat_engine: SimpleChatEngine = SimpleChatEngine.from_defaults(llm=self.llm,
                                                                            prefix_messages=self.prefix_messages)

    @classmethod
    async def astream_answer(cls, content: str, chat_history: List[ChatMessage],
                             model_config: Optional[str] = None, **kwargs) -> AsyncIterable[Tuple[str, bool]]:
        """ Asynchronous iterator to stream the answer from a Llama-Index model

            :param content: The new message content
            :type content: str

            :param chat_history: A list of past messages formatted accordingly by model manager
            :type chat_history: List

            :param model_config: Additional configuration given as a string through CLI or Telegram `App Settings`
                                 and retrieved from the database
            :type model_config: Optional[str]

            :param kwargs: Additional streaming arguments
            :type kwargs: Dict

            :return: An asynchronous iterator giving a tuple containing the new chunk and a boolean indicating
                     if the model is done or not
            :rtype: AsyncIterable[Tuple[str, bool]]
        """
        # Initialize model with optional additional config
        model: SimpleLlamaIndexQuackamollieModel = cls(model_config=model_config)

        # Get streaming response async generator
        astream_response: StreamingAgentChatResponse = await model.chat_engine.astream_chat(content,
                                                                                            chat_history=chat_history)

        # Async generator of tuples with the chunk and is_done field
        async for response in astream_response.async_response_gen():
            yield response, False
        else:
            yield "", True
