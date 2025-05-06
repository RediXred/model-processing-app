import os
from typing import Dict
from src.parser import ConfigParserFactory
from src.model import Builder, ModelDirector

class ModelProcessor:
    def __init__(self):
        self.parser_factory = ConfigParserFactory()
        self.model_builder = Builder()
    
    def process_model(self, input_file: str) -> Dict:
        extension = os.path.splitext(input_file)[1]
        parser = self.parser_factory.create_parser(extension)
        model_data = parser.parse(input_file)
        director = ModelDirector(self.model_builder)
        director.construct(model_data)
        return self.model_builder.build()