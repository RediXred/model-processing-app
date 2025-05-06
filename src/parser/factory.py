from src.parser.parser import ConfigParser, JsonConfigParser, XmlConfigParser

class ConfigParserFactory:
    def __init__(self):
        self.parsers = {
            ".xml": XmlConfigParser(),
            ".json": JsonConfigParser()
        }
    
    def create_parser(self, extension: str) -> ConfigParser:
        return self.parsers.get(extension, XmlConfigParser())