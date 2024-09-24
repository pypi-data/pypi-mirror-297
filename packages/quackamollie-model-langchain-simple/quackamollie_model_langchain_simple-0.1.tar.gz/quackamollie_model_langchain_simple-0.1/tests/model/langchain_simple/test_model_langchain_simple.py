# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import pytest

from quackamollie.model.meta.langchain.langchain_meta_model import MetaLangchainQuackamollieModel
from quackamollie.model_manager.langchain.langchain_model_manager import LangchainQuackamollieModelManager
from quackamollie.model_manager.langchain.helpers.langchain_model_entry_point import (
    get_langchain_models_from_entrypoints
)
from typing import Dict, Type

from quackamollie.model.langchain_simple.model_langchain_simple import SimpleLangchainQuackamollieModel


def test_model_langchain_simple_issubclass_of_meta_langchain_model():
    """ Assert SimpleLangchainQuackamollieModel model inherits from MetaLangchainQuackamollieModel """
    assert issubclass(SimpleLangchainQuackamollieModel, MetaLangchainQuackamollieModel), \
        "Model should be a subclass of MetaLangchainQuackamollieModel."


def test_model_langchain_simple_is_referenced_in_langchain_model_manager():
    """ Testing SimpleLangchainQuackamollieModel integration in LangchainQuackamollieModelManager

        Arrange/Act: Run `get_langchain_models_from_entrypoints()` method to load model from entrypoint
        Assert: The model is correctly loaded with the expected entrypoint name
    """
    entrypoint_group = LangchainQuackamollieModelManager.LANGCHAIN_ENTRYPOINT_GROUP
    result: Dict[str, Type[MetaLangchainQuackamollieModel]] = get_langchain_models_from_entrypoints(entrypoint_group)
    assert "simple-langchain" in result, "The model 'simple-langchain' should be listed in entrypoints"
    assert result["simple-langchain"] is SimpleLangchainQuackamollieModel, \
        "The entrypoint 'simple-langchain' should point to the model class"


# TODO: Implement online tests using Ollama

# TODO: Implement QuackamollieSettings magic mock in conftest
def test_model_langchain_simple_instantiation(ollama_url, ollama_base_model):
    """ Testing SimpleLangchainQuackamollieModel instantiation

        Arrange/Act: Run `SimpleLangchainQuackamollieModel()` method to instantiate the model
        Assert: The model is instantiated
    """
    if ollama_url is None:
        pytest.skip("Skipping tests that needs Ollama URL. Not implemented yet")

    model_config = "{'ollama_base_model': '%s'}" % ollama_base_model
    simple_model = SimpleLangchainQuackamollieModel(model_config=model_config)
    assert simple_model.model_config == model_config, "The model config isn't as expected"
