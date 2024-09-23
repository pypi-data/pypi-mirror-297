# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from quackamollie.model_manager.llama_index.llama_index_model_manager import LlamaIndexQuackamollieModelManager
from quackamollie.model_manager.llama_index.helpers.llama_index_model_entry_point import (
    get_llama_index_models_from_entrypoints
)


def test_get_llama_index_models_from_entrypoints():
    """ Test if the function returns an empty dict. """
    result = get_llama_index_models_from_entrypoints(LlamaIndexQuackamollieModelManager.LLAMA_INDEX_ENTRYPOINT_GROUP)
    assert result == {}, "The function `get_llama_index_models_from_entrypoints` should have returned an empty dict"

# TODO: Add tests with mock entrypoint
