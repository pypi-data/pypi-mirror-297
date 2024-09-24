# -*- coding: utf-8 -*-
__all__ = ["SimpleLangchainQuackamollieModel"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from ast import literal_eval
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings
from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.model.meta.langchain.langchain_meta_model import MetaLangchainQuackamollieModel
from typing import AsyncIterable, List, Optional, Tuple

from quackamollie.model.langchain_simple.prompt.langchain_simple_prompt import langchain_simple_context


class SimpleLangchainQuackamollieModel(MetaLangchainQuackamollieModel):
    """ Simple Langchain index model with chat history, managed by `LangchainQuackamollieModelManager` """

    model_families: List[ModelFamilyIcon] = [ModelFamilyIcon.LANGCHAIN]
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
        self.llm = ChatOllama(base_url=quackamollie_settings.ollama_base_url, model=ollama_base_model, timeout=600.0)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", langchain_simple_context),
            MessagesPlaceholder("chat_history"),
            ("user", "{content}"),
        ])
        self.parser = StrOutputParser()

        # Initialize the LLM chain
        self.chain = self.prompt | self.llm | self.parser

    @classmethod
    async def astream_answer(cls, content: str, chat_history: List[Tuple[str, str]],
                             model_config: Optional[str] = None, **kwargs) -> AsyncIterable[Tuple[str, bool]]:
        """ Asynchronous iterator to stream the answer from a Langchain model

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
        model: SimpleLangchainQuackamollieModel = cls(model_config=model_config)

        # Async generator of tuples with the chunk and is_done field
        async for chunk in model.chain.astream({"content": content, "chat_history": chat_history}):
            yield chunk, False
        else:
            yield "", True
