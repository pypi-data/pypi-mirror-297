# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.core.meta.model.meta_quackamollie_model import MetaQuackamollieModel
from typing import AsyncIterable, List, Optional, Tuple

from quackamollie.model.meta.langchain.langchain_meta_model import MetaLangchainQuackamollieModel


def test_langchain_meta_model_issubclass_of_meta_model():
    """ Assert MetaLangchainQuackamollieModel model manager inherits from MetaQuackamollieModel """
    assert issubclass(MetaLangchainQuackamollieModel, MetaQuackamollieModel), \
        "Meta model should be a subclass of MetaQuackamollieModel."


def test_langchain_meta_model_inheritance():
    """ Assert a simple mock model inheriting MetaLangchainQuackamollieModel can be instantiated """

    class MockTestLangchainQuackamollieModel(MetaLangchainQuackamollieModel):
        model_families: List[ModelFamilyIcon] = [ModelFamilyIcon.DEFAULT]

        @classmethod
        async def astream_answer(cls, content: str, chat_history: List[Tuple[str, str]],
                                 model_config: Optional[str] = None, **kwargs) -> AsyncIterable[Tuple[str, bool]]:
            pass

    mock_test_model = MockTestLangchainQuackamollieModel(model_config="test_langchain_model")

    assert isinstance(mock_test_model, MetaLangchainQuackamollieModel), \
        "Mock test model should be an instance of MetaLangchainQuackamollieModel."
    assert ModelFamilyIcon.DEFAULT in mock_test_model.model_families and len(mock_test_model.model_families) == 1, \
        "Model family icons doesn't match what the mock test model defines"
    assert mock_test_model.model_config == "test_langchain_model", \
        "Model config doesn't match what is defined during instantiation"
