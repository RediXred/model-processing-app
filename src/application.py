import os
from typing import Dict, List, Optional
from src.config import AppConfiguration
from src.processor import ModelProcessor, ConfigComparator, ConfigProcessor, JsonConfigProcessor
from src.output import OutputGenerator, XmlConfigOutputGenerator, MetaJsonOutputGenerator


class Application:
    def __init__(self, config: AppConfiguration = None, output_generators: Optional[List[OutputGenerator]] = None,
                 config_processor: Optional[ConfigProcessor] = None):
        self.config = config or AppConfiguration()
        self.model_processor = ModelProcessor()
        self.config_comparator = ConfigComparator()
        self.output_generators = output_generators or [
            XmlConfigOutputGenerator(),
            MetaJsonOutputGenerator()
        ]
        self.config_processor = config_processor or JsonConfigProcessor()
        os.makedirs(self.config.output_dir, exist_ok=True)
    
    def generate_output_files(self, model: Dict) -> None:
        try:
            for generator in self.output_generators:
                generator.generate(model, self.config)
        except IOError as e:
            raise IOError(f"Failed to generate output files: {e}") from e
        except KeyError as e:
            raise ValueError(f"Output path not defined for generator: {e}") from e
    
    def process_configs(self) -> None:
        self.config_processor.process(self.config, self.config_comparator)
    
    def run(self) -> None:
        try:
            model = self.model_processor.process_model(self.config.input_model)
            self.generate_output_files(model)
            self.process_configs()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Input model file not found: {e}") from e
        except Exception as e:
            raise Exception(f"Application execution failed: {e}") from e