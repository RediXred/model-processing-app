from abc import ABC, abstractmethod
from typing import Dict, List
from src.model.elements import ClassInfo, Attribute, Relation

class ModelBuilder(ABC):
    @abstractmethod
    def add_class(self, name: str, is_root: bool, documentation: str) -> 'ModelBuilder':
        raise NotImplementedError
    
    @abstractmethod
    def add_attribute(self, class_name: str, attr_name: str, attr_type: str) -> 'ModelBuilder':
        raise NotImplementedError
    
    @abstractmethod
    def add_relation(self, source: str, target: str, source_multiplicity: str, target_multiplicity: str) -> 'ModelBuilder':
        raise NotImplementedError
    
    @abstractmethod
    def build(self) -> Dict:
        raise NotImplementedError


class Builder(ModelBuilder):
    def __init__(self):
        self.classes: Dict[str, ClassInfo] = {}
        self.relations: List[Relation] = []

    def add_class(self, name: str, is_root: bool, documentation: str) -> 'Builder':
        if name not in self.classes:
            self.classes[name] = ClassInfo(
                name=name,
                is_root=is_root,
                documentation=documentation,
                attributes=[],
                source_relations=[],
                target_relations=[]
            )
        return self

    def add_attribute(self, class_name: str, attr_name: str, attr_type: str) -> 'Builder':
        if class_name in self.classes:
            self.classes[class_name].attributes.append(
                Attribute(name=attr_name, type=attr_type)
            )
        return self

    def add_relation(self, source: str, target: str, 
                    source_multiplicity: str, target_multiplicity: str) -> 'Builder':
        relation = Relation(
            source=source,
            target=target,
            source_multiplicity=source_multiplicity,
            target_multiplicity=target_multiplicity
        )
        self.relations.append(relation)
        
        if source in self.classes:
            self.classes[source].target_relations.append(relation)
        if target in self.classes:
            self.classes[target].source_relations.append(relation)
            
        return self

    def build(self) -> Dict:
        return {
            'classes': self.classes,
            'relations': self.relations
        }


class ModelDirector:
    def __init__(self, builder: ModelBuilder):
        self.builder = builder
    
    def construct(self, model_data: Dict) -> None:
        for class_name, class_info in model_data["classes"].items():
            self.builder.add_class(class_name, class_info["is_root"], class_info["documentation"])
            for attr in class_info["attributes"]:
                self.builder.add_attribute(class_name, attr["name"], attr["type"])
        for rel in model_data["relations"]:
            self.builder.add_relation(rel["source"], rel["target"], 
                                    rel["source_multiplicity"], rel["target_multiplicity"])
