# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from quackamollie.model_manager.langchain.langchain_model_manager import LangchainQuackamollieModelManager
from quackamollie.model_manager.langchain.helpers.langchain_model_entry_point import (
    get_langchain_models_from_entrypoints
)


def test_get_langchain_models_from_entrypoints():
    """ Test if the function returns an empty dict. """
    result = get_langchain_models_from_entrypoints(LangchainQuackamollieModelManager.LANGCHAIN_ENTRYPOINT_GROUP)
    assert result == {}, "The function `get_langchain_models_from_entrypoints` should have returned an empty dict"

# TODO: Add tests with mock entrypoint
