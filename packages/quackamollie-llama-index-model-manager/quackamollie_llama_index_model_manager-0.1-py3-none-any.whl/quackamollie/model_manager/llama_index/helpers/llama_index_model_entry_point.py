# -*- coding: utf-8 -*-
__all__ = ["get_llama_index_models_from_entrypoints"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

from importlib.metadata import entry_points
from typing import Dict, Type

from quackamollie.model.meta.llama_index.llama_index_meta_model import MetaLlamaIndexQuackamollieModel


def get_llama_index_models_from_entrypoints(entrypoint_group: str) -> Dict[str, Type[MetaLlamaIndexQuackamollieModel]]:
    """ Parse entry_points from a group in order to load and make dynamically available MetaLlamaIndexQuackamollieModels
        through the LlamaIndexQuackamollieModelManager

        :param entrypoint_group: The entry_point group to iterate over to dynamically find llama_index custom models
        :type entrypoint_group: str

        :return: A dictionary of MetaLlamaIndexQuackamollieModels indexed by entry_point name
        :rtype: dict
    """
    models: Dict[str, Type[MetaLlamaIndexQuackamollieModel]] = {}
    for script in entry_points(group=entrypoint_group):
        try:
            potential_model = script.load()
        except Exception as error:
            raise AttributeError(f"Error loading MetaLlamaIndexQuackamollieModel from entrypoint"
                                 f" with name '{script.name}' in group '{entrypoint_group}',"
                                 f" with exception:\n{error}")

        if issubclass(potential_model, MetaLlamaIndexQuackamollieModel):
            models[script.name] = potential_model
        else:
            raise AttributeError(f"Error loaded class '{potential_model.__name__}', from entrypoint"
                                 f" with name '{script.name}' in group '{entrypoint_group}',"
                                 f" doesn't inherit from MetaLlamaIndexQuackamollieModel.")

    return models
