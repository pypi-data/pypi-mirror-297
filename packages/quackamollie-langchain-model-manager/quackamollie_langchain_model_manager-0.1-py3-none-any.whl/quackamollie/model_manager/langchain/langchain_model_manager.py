# -*- coding: utf-8 -*-
__all__ = ["LangchainQuackamollieModelManager"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.core.database.model import ChatMessage
from quackamollie.core.meta.model_manager.meta_quackamollie_model_manager import MetaQuackamollieModelManager
from typing import Dict, List, Optional, Tuple, Type

from quackamollie.model.meta.langchain.langchain_meta_model import MetaLangchainQuackamollieModel
from quackamollie.model_manager.langchain.helpers.langchain_model_entry_point import (
    get_langchain_models_from_entrypoints
)


class LangchainQuackamollieModelManager(MetaQuackamollieModelManager):
    """ Model manager managed by the `QuackamollieModelManagerRegistry` and serving models using Langchain """

    families: List[ModelFamilyIcon] = [ModelFamilyIcon.LANGCHAIN]
    LANGCHAIN_ENTRYPOINT_GROUP: str = "quackamollie.model.langchain"
    _entrypoint_model_dict: Optional[Dict[str, Type[MetaLangchainQuackamollieModel]]] = None

    @classmethod
    async def get_entrypoint_model_dict(cls) -> Optional[Dict[str, Type[MetaLangchainQuackamollieModel]]]:
        if cls._entrypoint_model_dict is None:
            cls._entrypoint_model_dict = get_langchain_models_from_entrypoints(cls.LANGCHAIN_ENTRYPOINT_GROUP)
        return cls._entrypoint_model_dict

    @classmethod
    async def get_model_list(cls) -> Optional[List[str]]:
        """ Discover the models available for the model manager at runtime asynchronously

            :return: A list of available models for the model manager
            :rtype: List[str]
        """
        if cls._model_list is None:
            entrypoint_model_dict = await cls.get_entrypoint_model_dict()
            if entrypoint_model_dict is not None:
                cls._model_list = list(entrypoint_model_dict.keys())
        return cls._model_list

    @classmethod
    async def get_model_families(cls) -> Dict[str, List[ModelFamilyIcon]]:
        """ Discover the models families available for the model manager at runtime asynchronously

            :return: A dict with values the list of families indexed by model name
            :rtype: Dict[str, List[ModelFamilyIcon]]
        """
        if cls._model_families is None:
            entrypoint_model_dict = await cls.get_entrypoint_model_dict()
            if cls._entrypoint_model_dict is not None:
                cls._model_families = {}
                for entrypoint_name, model_class in entrypoint_model_dict.items():
                    cls._model_families[entrypoint_name] = model_class.model_families
        return cls._model_families

    @classmethod
    def parse_chat_history(cls, chat_messages: Optional[List[ChatMessage]]) -> List[Tuple[str, str]]:
        """ Parse the chat history given as a list of `ChatMessage` from the database model to a list compatible with
            the model manager's models.

            :param chat_messages: A list of `ChatMessage` from the database model
            :param chat_messages: Optional[List[ChatMessage]]

            :return: A list of messages formatted to be compatible with the model manager's models.
            :rtype: List[Tuple[str, str]]
        """
        chat_history: List[Tuple[str, str]] = []

        # Construct the list of messages in a format supported by Langchain
        if chat_messages:
            for past_msg in chat_messages:
                chat_history.append((past_msg.user.user_type.value.lower(), past_msg.content))

        return chat_history

    @classmethod
    async def get_model_class(cls, model_name: str) -> Optional[Type[MetaLangchainQuackamollieModel]]:
        """ Get the model class from the model name

            :param model_name: Name of the model as listed by `cls.get_model_list`
            :type model_name: str

            :return: A subclass of MetaQuackamollieModel
            :rtype: Optional[Type[MetaLangchainQuackamollieModel]]
        """
        entrypoint_model_dict = await cls.get_entrypoint_model_dict()
        if entrypoint_model_dict is None:
            return None
        else:
            return entrypoint_model_dict.get(model_name, None)

    @classmethod
    def reset(cls):
        """ Reset the model manager dynamic fields to force reloading models. Be careful if used asynchronously """
        cls._entrypoint_model_dict = None
        cls._model_list = None
        cls._model_families = None
