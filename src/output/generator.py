import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict
from src.config import AppConfiguration
from src.model import ModelVisitor, XmlConfigVisitor, MetaJsonVisitor


class OutputGenerator(ABC):
    @abstractmethod
    def generate(self, model: Dict, config: AppConfiguration) -> None:
        raise NotImplementedError

class XmlConfigOutputGenerator(OutputGenerator):
    def __init__(self, visitor: ModelVisitor = None):
        self.visitor = visitor or XmlConfigVisitor()
    
    def generate(self, model: Dict, config: AppConfiguration) -> None:
        config_xml = self.visitor.generate(model)
        self.indent(config_xml)
        
        tree = ET.ElementTree(config_xml)
        with open(config.output_paths[self.key()], "wb") as f:
            tree.write(f, encoding='utf-8', xml_declaration=False, method='xml')
    
    def indent(self, elem: ET.Element, level: int = 0, indent_str: str = "  ") -> None:
        i = "\n" + level * indent_str
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + indent_str
            last_idx = len(elem) - 1
            for idx, subelem in enumerate(elem):
                self.indent(subelem, level + 1, indent_str)
                if idx == last_idx:
                    subelem.tail = i
                else:
                    subelem.tail = i + indent_str
            if not elem.tail:
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    @classmethod
    def key(cls) -> str:
        return "XmlConfigOutputGenerator"

class MetaJsonOutputGenerator(OutputGenerator):
    def __init__(self, visitor: ModelVisitor = None):
        self.visitor = visitor or MetaJsonVisitor()
    
    def generate(self, model: Dict, config: AppConfiguration) -> None:
        meta_json = self.visitor.generate(model)
        with open(config.output_paths[self.key()], "w") as f:
            json.dump(meta_json, f, indent=4)
    
    @classmethod
    def key(cls) -> str:
        return "MetaJsonOutputGenerator"