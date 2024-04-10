from enum import Enum
from typing import List


class DeclarationType(Enum):
    CLASS = "class"
    OBJECT = "object"
    FUNCTION = "function"
    PROPERTY = "property"
    TYPE = "type"


class Parameter:
    def __init__(self, name: str, type: str, value: str):
        self.name = name
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Parameter(name='{self.name}', type='{self.type}', value='{self.value}')"


class Declaration:
    def __init__(self, name: str, type: DeclarationType, declarations):
        self.name = name
        self.type = type
        self.declarations = declarations

    def add(self, declaration):
        self.declarations.append(declaration)

    def remove(self, declaration):
        self.declarations.remove(declaration)


class ObjectDeclaration(Declaration):
    def __init__(self, name: str):
        super().__init__(name, declarations=[], type=DeclarationType.OBJECT)


class ClassDeclaration(Declaration):
    def __init__(self, name: str):
        super().__init__(name, declarations=[], type=DeclarationType.CLASS)


class PropertyDeclaration(Declaration):
    def __init__(self, name: str):
        super().__init__(name, declarations=[], type=DeclarationType.PROPERTY)


class TypeDeclaration(Declaration):
    def __init__(self, name: str):
        super().__init__(name, declarations=[], type=DeclarationType.TYPE)


class FunctionDeclaration(Declaration):
    def __init__(self, name: str, parameters: List[Parameter], returnType: str, body: str):
        super().__init__(name, declarations=[], type="function") #TODO fix
        self.parameters = parameters
        self.returnType = returnType
        self.body = body

    def __repr__(self):
        parameters_repr = ', '.join(repr(param) for param in self.parameters)
        declarations_repr = ', '.join(repr(declaration) for declaration in self.declarations)
        return (f"FunctionDeclaration(type='{self.type}', name='{self.name}', "
                f"parameters=[{parameters_repr}], "
                f"returnType='{self.returnType}', body='{self.body}', declarations=[{declarations_repr}])")
