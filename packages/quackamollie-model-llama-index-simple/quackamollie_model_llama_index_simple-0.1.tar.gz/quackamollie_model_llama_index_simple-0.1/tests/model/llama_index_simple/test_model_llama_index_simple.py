# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import pytest

from quackamollie.model.meta.llama_index.llama_index_meta_model import MetaLlamaIndexQuackamollieModel
from quackamollie.model_manager.llama_index.llama_index_model_manager import LlamaIndexQuackamollieModelManager
from quackamollie.model_manager.llama_index.helpers.llama_index_model_entry_point import (
    get_llama_index_models_from_entrypoints
)
from typing import Dict, Type

from quackamollie.model.llama_index_simple.model_llama_index_simple import SimpleLlamaIndexQuackamollieModel


def test_model_llama_index_simple_issubclass_of_meta_llama_index_model():
    """ Assert SimpleLlamaIndexQuackamollieModel model inherits from MetaLlamaIndexQuackamollieModel """
    assert issubclass(SimpleLlamaIndexQuackamollieModel, MetaLlamaIndexQuackamollieModel), \
        "Model should be a subclass of MetaLlamaIndexQuackamollieModel."


def test_model_llama_index_simple_is_referenced_in_llama_index_model_manager():
    """ Testing SimpleLlamaIndexQuackamollieModel integration in LlamaIndexQuackamollieModelManager

        Arrange/Act: Run `get_llama_index_models_from_entrypoints()` method to load model from entrypoint
        Assert: The model is correctly loaded with the expected entrypoint name
    """
    entrypoint_group = LlamaIndexQuackamollieModelManager.LLAMA_INDEX_ENTRYPOINT_GROUP
    result: Dict[str, Type[MetaLlamaIndexQuackamollieModel]] = get_llama_index_models_from_entrypoints(entrypoint_group)
    assert "simple-llama-index" in result, "The model 'simple-llama-index' should be listed in entrypoints"
    assert result["simple-llama-index"] is SimpleLlamaIndexQuackamollieModel, \
        "The entrypoint 'simple-llama-index' should point to the model class"


# TODO: Implement online tests using Ollama

# TODO: Implement QuackamollieSettings magic mock in conftest
def test_model_llama_index_simple_instantiation(ollama_url, ollama_base_model):
    """ Testing SimpleLlamaIndexQuackamollieModel instantiation

        Arrange/Act: Run `SimpleLlamaIndexQuackamollieModel()` method to instantiate the model
        Assert: The model is instantiated
    """
    if ollama_url is None:
        pytest.skip("Skipping tests that needs Ollama URL. Not implemented yet")

    model_config = "{'ollama_base_model': '%s'}" % ollama_base_model
    simple_model = SimpleLlamaIndexQuackamollieModel(model_config=model_config)
    assert simple_model.model_config == model_config, "The model config isn't as expected"
