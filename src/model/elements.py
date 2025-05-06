from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .visitor import ModelVisitor

class ModelElement(ABC):
    @abstractmethod
    def accept(self, visitor: 'ModelVisitor') -> None:
        raise NotImplementedError

@dataclass
class Attribute(ModelElement):
    name: str
    type: str
    
    def accept(self, visitor: 'ModelVisitor') -> None:
        visitor.visit_attribute(self)

@dataclass
class Relation(ModelElement):
    source: str
    target: str
    source_multiplicity: str
    target_multiplicity: str
    
    def accept(self, visitor: 'ModelVisitor') -> None:
        visitor.visit_relation(self)

@dataclass
class ClassInfo(ModelElement):
    name: str
    is_root: bool
    documentation: str
    attributes: List[Attribute]
    source_relations: List[Relation]
    target_relations: List[Relation]
    
    def accept(self, visitor: 'ModelVisitor') -> None:
        visitor.visit_class(self)
        for rel in self.source_relations:
            rel.accept(visitor)