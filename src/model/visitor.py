from abc import ABC, abstractmethod
from typing import Dict, List
import xml.etree.ElementTree as ET
from src.model.elements import ClassInfo, Attribute, Relation

class ModelVisitor(ABC):
    @abstractmethod
    def visit_class(self, class_info: ClassInfo) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def visit_attribute(self, attribute: Attribute) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def visit_relation(self, relation: Relation) -> None:
        raise NotImplementedError


class XmlConfigVisitor(ModelVisitor):
    def __init__(self):
        self.root_element = None
        self.current_element = self.root_element
        self.element_stack = []
        self.visited_classes = set()
        self.model = None
        self.temp_class_element = None
    
    def visit_class(self, class_info: 'ClassInfo') -> None:
        if class_info.name in self.visited_classes:
            return
        self.visited_classes.add(class_info.name)
        
        if class_info.is_root:
            self.root_element = ET.Element(class_info.name)
            self.current_element = self.root_element
        else:
            new_element = ET.SubElement(self.current_element, class_info.name)
            self.element_stack.append(self.current_element)
            self.current_element = new_element
        
        for attr in class_info.attributes:
            attr.accept(self)
        
        if self.model:
            for rel in class_info.source_relations:
                source_class = rel.source
                if source_class in self.model['classes'] and source_class not in self.visited_classes:
                    source_class_info = self.model['classes'][source_class]
                    source_class_info.accept(self)
        
        if self.element_stack and not class_info.is_root:
            self.current_element = self.element_stack.pop()
    
    def visit_attribute(self, attribute: 'Attribute') -> None:
        attr_elem = ET.SubElement(self.current_element, attribute.name)
        attr_elem.text = attribute.type
    
    def visit_relation(self, relation: 'Relation') -> None:
        pass
    
    def generate(self, model: Dict) -> ET.Element:
        self.visited_classes.clear()
        self.model = model
        for class_info in model["classes"].values():
            if class_info.is_root:
                class_info.accept(self)
                break
        if self.root_element is None:
            raise ValueError("No root class found in the model")
        return self.root_element

class MetaJsonVisitor(ModelVisitor):
    def __init__(self):
        self.meta_data = []
        self.current_class = None
    
    def visit_class(self, class_info: ClassInfo) -> None:
        min_max = self._get_multiplicity(class_info)
        self.current_class = {
            "class": class_info.name,
            "documentation": class_info.documentation,
            "isRoot": class_info.is_root,
            "max": min_max["max"],
            "min": min_max["min"],
            "parameters": []
        }
        self.meta_data.append(self.current_class)
        for attr in class_info.attributes:
            self.visit_attribute(attr)
    
    def visit_attribute(self, attribute: Attribute) -> None:
        self.current_class["parameters"].append({"name": attribute.name, "type": attribute.type})
    
    def visit_relation(self, relation: Relation) -> None:
        self.current_class["parameters"].append({"name": relation.source, "type": "class"})
    
    def _get_multiplicity(self, class_info: ClassInfo) -> Dict:
        if class_info.is_root:
            return {"min": "1", "max": "1"}
        for rel in class_info.target_relations:
            mult = rel.source_multiplicity
            if ".." in mult:
                min_val, max_val = mult.split("..")
            else:
                min_val = max_val = mult
            return {"min": min_val, "max": max_val}
        return {"min": "1", "max": "1"}
    
    def generate(self, model: Dict) -> List:
        for class_info in model["classes"].values():
            class_info.accept(self)
        return self.meta_data