import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict


class ConfigParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> Dict:
        raise NotImplementedError

class JsonConfigParser(ConfigParser):
    def parse(self, file_path: str) -> Dict:
        with open(file_path, 'r') as f:
            return json.load(f)

class XmlConfigParser(ConfigParser):
    def parse(self, file_path: str) -> Dict:
        tree = ET.parse(file_path)
        root = tree.getroot()
        model = {"classes": {}, "relations": []}
        
        for class_elem in root.findall(".//Class"):
            class_name = class_elem.get("name")
            model["classes"][class_name] = {
                "is_root": class_elem.get("isRoot") == "true",
                "documentation": class_elem.get("documentation") or "",
                "attributes": [
                    {"name": attr.get("name"), "type": attr.get("type")}
                    for attr in class_elem.findall("Attribute")
                ],
                "source_relations": [],
                "target_relations": []
            }
        
        for agg_elem in root.findall(".//Aggregation"):
            relation = {
                "source": agg_elem.get("source"),
                "target": agg_elem.get("target"),
                "source_multiplicity": agg_elem.get("sourceMultiplicity"),
                "target_multiplicity": agg_elem.get("targetMultiplicity")
            }
            model["relations"].append(relation)
            model["classes"][relation["source"]]["target_relations"].append(relation)
            model["classes"][relation["target"]]["source_relations"].append(relation)
        
        return model