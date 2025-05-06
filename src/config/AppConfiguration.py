from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AppConfiguration:
    input_model: str = "input/impulse_test_input.xml"
    input_config_paths: List[str] = None
    output_dir: str = "out"
    output_paths: Dict[str, str] = None
    output_config_paths: List[str] = None

    def __post_init__(self):
        if not isinstance(self.input_model, str):
            raise TypeError(f"input_model must be a string, got {type(self.input_model).__name__}")
        
        self.input_config_paths = self.input_config_paths or [
            "input/config.json",
            "input/patched_config.json"
        ]
        self.output_paths = self.output_paths or {
            "XmlConfigOutputGenerator": "out/config.xml",
            "MetaJsonOutputGenerator": "out/meta.json"
        }
        self.output_config_paths = self.output_config_paths or [
            "out/delta.json",
            "out/res_patched_config.json"
        ]

        if not isinstance(self.input_config_paths, list) or not all(isinstance(p, str) for p in self.input_config_paths):
            raise TypeError("input_config_paths must be a list of strings")
        if not isinstance(self.output_dir, str):
            raise TypeError(f"output_dir must be a string, got {type(self.output_dir).__name__}")
        if not isinstance(self.output_paths, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in self.output_paths.items()):
            raise TypeError("output_paths must be a dict mapping generator types to strings")
        if not isinstance(self.output_config_paths, list) or not all(isinstance(p, str) for p in self.output_config_paths):
            raise TypeError("output_config_paths must be a list of strings")