# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from quackamollie.core.meta.model_manager.meta_quackamollie_model_manager import MetaQuackamollieModelManager
from quackamollie.core.model_manager_registry.model_manager_registry import QuackamollieModelManagerRegistry
from typing import Dict, Type

from quackamollie.model_manager.langchain.langchain_model_manager import LangchainQuackamollieModelManager


def test_model_manager_issubclass_of_mete_model_manager():
    """ Assert LangchainQuackamollieModelManager model manager inherits from MetaQuackamollieModelManager """
    assert issubclass(LangchainQuackamollieModelManager, MetaQuackamollieModelManager), \
        "Model manager should be a subclass of MetaQuackamollieModelManager."


def test_model_manager_referenced_in_model_manager_registry():
    """ Testing LangchainQuackamollieModelManager integration in QuackamollieModelManagerRegistry

        Arrange/Act: Run QuackamollieModelManagerRegistry `load_model_managers()` method to load it from entrypoint
        Assert: The model manager is correctly loaded with the expected entrypoint name
    """
    model_manager_registry = QuackamollieModelManagerRegistry()
    model_manager_registry.load_model_managers()
    model_managers: Dict[str, Type[MetaQuackamollieModelManager]] = model_manager_registry.model_managers

    class_name_to_entrypoint_name: Dict[str, str] = model_manager_registry.class_name_to_entrypoint_name
    assert "langchain" in model_managers, \
        "'langchain' model manager should be auto-discovered by the model manager registry."

    model_manager_class: Type[MetaQuackamollieModelManager] = model_managers["langchain"]
    assert model_manager_class is LangchainQuackamollieModelManager, \
        "'langchain' model manager should point to the LangchainQuackamollieModelManager class."

    assert model_manager_class.__name__ in model_manager_registry.model_managers_by_class_name, \
        "'LangchainQuackamollieModelManager' model manager isn't correctly indexed by class name."

    model_manager_class = model_manager_registry.model_managers_by_class_name[model_manager_class.__name__]
    assert model_manager_class is LangchainQuackamollieModelManager, \
        ("'LangchainQuackamollieModelManager' model manager should point to the"
         " LangchainQuackamollieModelManager class.")

    assert class_name_to_entrypoint_name[model_manager_class.__name__] == 'langchain', \
        "'LangchainQuackamollieModelManager' class name doesn't index 'langchain' entrypoint name"


# TODO: Implement online tests using Ollama
