import json
from abc import ABC, abstractmethod
from src.config import AppConfiguration
from src.processor.comparator import ConfigComparator


class ConfigProcessor(ABC):
    @abstractmethod
    def process(self, config: AppConfiguration, comparator: ConfigComparator) -> None:
        raise NotImplementedError

class JsonConfigProcessor(ConfigProcessor):
    def process(self, config: AppConfiguration, comparator: ConfigComparator) -> None:
        try:
            configs = []
            for input_path in config.input_config_paths:
                with open(input_path, "r") as f:
                    configs.append(json.load(f))
            
            delta = comparator.compare_configs(configs[0], configs[1])
            with open(config.output_config_paths[0], "w") as f:
                json.dump(delta, f, indent=4)
            
            res_patched_config = comparator.apply_delta(configs[0], delta)
            with open(config.output_config_paths[1], "w") as f:
                json.dump(res_patched_config, f, indent=4)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file not found: {e}") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in configuration file: {e}", e.doc, e.pos) from e
        except IOError as e:
            raise IOError(f"Failed to process configuration files: {e}") from e