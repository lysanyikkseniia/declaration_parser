from enum import Enum
from typing import List


class DeclarationType(Enum):
    CLASS = "class"
    OBJECT = "object"
    FUNCTION = "function"
    PROPERTY = "property"
    TYPE = "type"


class Parameter:
    def __init__(self, name: str, dtype: str, value: str = None):
        self.name = name
        self.dtype = dtype
        self.value = value

    def __repr__(self):
        return f"Parameter(name='{self.name}', type='{self.dtype}', value='{self.value}')"


class Declaration:
    def __init__(self, name: str, type: DeclarationType, modifiers=None, body_tokens=None):
        self.name = name
        self.type = type

        self.modifiers = modifiers
        self.declarations = []

        self.body = ' '.join(modifiers) + ' '.join(body_tokens)

    def add_declaration(self, declaration):
        self.declarations.append(declaration)


class ObjectDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.OBJECT.value, modifiers=modifiers, body_tokens=body_tokens)


class ClassDeclaration(Declaration):  # TODO interface classes
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.CLASS.value, modifiers=modifiers, body_tokens=body_tokens)
        self.primary_constructor = ''  # TODO
        self.supertype_specifiers = ''  # TODO


class PropertyDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.PROPERTY.value, modifiers=modifiers, body_tokens=body_tokens)


class TypeDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.TYPE.value, modifiers=modifiers, body_tokens=body_tokens)


class FunctionDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.FUNCTION.value, modifiers=modifiers, body_tokens=body_tokens)

        self.parameters = ''  # TODO
        self.returnType = ''  # TODO

    def __repr__(self):
        parameters_repr = ', '.join(repr(param) for param in self.parameters)
        modifiers_repr = ', '.join(repr(mod) for mod in self.modifiers)
        declarations_repr = ', '.join(repr(decl) for decl in self.declarations)
        return (f"FunctionDeclaration(type='{self.type}', name='{self.name}', "
                f"parameters=[{parameters_repr}], "
                f"returnType='{self.returnType}', body='{self.body}', modifiers=['{modifiers_repr}'], declarations=[{declarations_repr}])")
