# -*- coding: utf-8 -*-
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from llama_index.core.base.llms.types import ChatMessage
from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.core.meta.model.meta_quackamollie_model import MetaQuackamollieModel
from typing import AsyncIterable, List, Optional, Tuple

from quackamollie.model.meta.llama_index.llama_index_meta_model import MetaLlamaIndexQuackamollieModel


def test_llama_index_meta_model_issubclass_of_meta_model():
    """ Assert MetaLlamaIndexQuackamollieModel model manager inherits from MetaQuackamollieModel """
    assert issubclass(MetaLlamaIndexQuackamollieModel, MetaQuackamollieModel), \
        "Meta model should be a subclass of MetaQuackamollieModel."


def test_llama_index_meta_model_inheritance():
    """ Assert a simple mock model inheriting MetaLlamaIndexQuackamollieModel can be instantiated """

    class MockTestLlamaIndexQuackamollieModel(MetaLlamaIndexQuackamollieModel):
        model_families: List[ModelFamilyIcon] = [ModelFamilyIcon.DEFAULT]

        @classmethod
        async def astream_answer(cls, content: str, chat_history: List[ChatMessage],
                                 model_config: Optional[str] = None, **kwargs) -> AsyncIterable[Tuple[str, bool]]:
            pass

    mock_test_model = MockTestLlamaIndexQuackamollieModel(model_config="test_llama_index_model")

    assert isinstance(mock_test_model, MetaLlamaIndexQuackamollieModel), \
        "Mock test model should be an instance of MetaLlamaIndexQuackamollieModel."
    assert ModelFamilyIcon.DEFAULT in mock_test_model.model_families and len(mock_test_model.model_families) == 1, \
        "Model family icons doesn't match what the mock test model defines"
    assert mock_test_model.model_config == "test_llama_index_model", \
        "Model config doesn't match what is defined during instantiation"
