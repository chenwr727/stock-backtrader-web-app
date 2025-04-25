from typing import Any, Dict

import yaml

from .logs import logger


def load_strategy(yaml_file: str) -> Dict[str, Any]:
    """加载策略配置

    Args:
        yaml_file (str): 策略配置文件路径

    Returns:
        Dict[str, Any]: 策略配置
    """
    try:
        with open(yaml_file, "r", encoding="utf-8") as f:
            strategy = yaml.safe_load(f)
        return strategy
    except (FileNotFoundError, yaml.YAMLError) as e:
        logger.error(f"加载策略配置失败: {e}")
        raise
