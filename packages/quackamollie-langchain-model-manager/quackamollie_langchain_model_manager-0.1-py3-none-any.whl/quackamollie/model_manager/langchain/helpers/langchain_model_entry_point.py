# -*- coding: utf-8 -*-
__all__ = ["get_langchain_models_from_entrypoints"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from importlib.metadata import entry_points
from typing import Dict, Type

from quackamollie.model.meta.langchain.langchain_meta_model import MetaLangchainQuackamollieModel


def get_langchain_models_from_entrypoints(entrypoint_group: str) -> Dict[str, Type[MetaLangchainQuackamollieModel]]:
    """ Parse entry_points from a group in order to load and make dynamically available MetaLangchainQuackamollieModels
        through the LangchainQuackamollieModelManager

        :param entrypoint_group: The entry_point group to iterate over to dynamically find langchain custom models
        :type entrypoint_group: str

        :return: A dictionary of MetaLangchainQuackamollieModels indexed by entry_point name
        :rtype: dict
    """
    models: Dict[str, Type[MetaLangchainQuackamollieModel]] = {}
    for script in entry_points(group=entrypoint_group):
        try:
            potential_model = script.load()
        except Exception as error:
            raise AttributeError(f"Error loading MetaLangchainQuackamollieModel from entrypoint"
                                 f" with name '{script.name}' in group '{entrypoint_group}',"
                                 f" with exception:\n{error}")

        if issubclass(potential_model, MetaLangchainQuackamollieModel):
            models[script.name] = potential_model
        else:
            raise AttributeError(f"Error loaded class '{potential_model.__name__}', from entrypoint"
                                 f" with name '{script.name}' in group '{entrypoint_group}',"
                                 f" doesn't inherit from MetaLangchainQuackamollieModel.")

    return models
