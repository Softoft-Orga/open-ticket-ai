import logging

import yaml
from pydantic import BaseModel
from rich.console import Console
from rich.syntax import Syntax

logger = logging.getLogger(__name__)


def prettify_dict(config: BaseModel | dict):
    # turn your BaseModel into a dict

    cfg_dict = config.model_dump() if isinstance(config, BaseModel) else config

    # render YAML
    try:
        yaml_str = yaml.safe_dump(cfg_dict, sort_keys=False)
    except Exception as e:
        logger.warning(f"Failed to prettify config: {e}")
        return str(cfg_dict)
    return yaml_str
