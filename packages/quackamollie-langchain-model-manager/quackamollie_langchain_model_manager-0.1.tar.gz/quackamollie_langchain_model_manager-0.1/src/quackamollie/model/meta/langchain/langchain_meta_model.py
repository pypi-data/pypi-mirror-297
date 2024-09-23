# -*- coding: utf-8 -*-
__all__ = ["MetaLangchainQuackamollieModel"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from abc import ABCMeta
from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.core.meta.model.meta_quackamollie_model import MetaQuackamollieModel
from typing import List, Optional


class MetaLangchainQuackamollieModel(MetaQuackamollieModel, metaclass=ABCMeta):
    """ Metaclass for models managed by `LangchainQuackamollieModelManager` """

    model_families: List[ModelFamilyIcon]

    def __init__(self, model_config: Optional[str] = None):
        """ Initialize the model with model additional configuration retrieved from the database

            :param model_config: Additional configuration given as a string through CLI or Telegram `App Settings`
                                 and retrieved from the database
            :type model_config: Optional[str]
        """
        self.model_config: Optional[str] = model_config
