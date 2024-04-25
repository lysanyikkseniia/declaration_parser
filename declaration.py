import re
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

    def to_dict(self):
        result = {'name': self.name, 'type': self.dtype}
        if self.value:
            result['value'] = self.value
        return result


class Declaration:
    def __init__(self, name: str, type: DeclarationType, modifiers=None, body_tokens=None):
        self.name = name
        self.type = type

        self.modifiers = modifiers
        self.declarations = []

        self.body = ' '.join(modifiers + body_tokens)

    def add_declaration(self, declaration):
        self.declarations.append(declaration)

    def to_dict(self):
        result = {'type': self.type, 'name': self.name}
        return result


class ObjectDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.OBJECT.value, modifiers=modifiers, body_tokens=body_tokens)


class ClassDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: List[str], modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.CLASS.value, modifiers=modifiers, body_tokens=body_tokens)
        self.primary_constructor = self.parse_primary_constructor(body_tokens)
        self.supertype_specifiers = self.parse_supertype_specifiers(body_tokens)

    def parse_primary_constructor(self, tokens: List[str]) -> str:
        constructor_start = False
        constructor_params = ""
        for token in tokens:
            if "constructor" in token:
                constructor_start = True
                # Extract constructor parameters, assuming they may start in the same token
                start_index = token.find("(")
                if start_index != -1:
                    constructor_params = token[start_index + 1:]
                    break
        if constructor_start and constructor_params:
            # Find the closing parenthesis index
            end_index = constructor_params.find(")")
            if end_index != -1:
                return constructor_params[:end_index]
        return ""

    def parse_supertype_specifiers(self, tokens: List[str]) -> str:
        colon_seen = False
        for i, token in enumerate(tokens):
            if colon_seen and "()" in token:
                # Remove "()" and return the word
                return token.replace("()", "")
            if token == ":":
                colon_seen = True
        return ""

    def to_dict(self):
        result = super().to_dict()
        if self.primary_constructor:
            result['primary_constructor'] = self.primary_constructor
        if self.supertype_specifiers:
            result['supertype_specifiers'] = self.supertype_specifiers
        if self.declarations:
            result['declarations'] = [decl.to_dict() for decl in self.declarations]
        result['body'] = self.body
        return result


class PropertyDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.PROPERTY.value, modifiers=modifiers, body_tokens=body_tokens)


class TypeDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.TYPE.value, modifiers=modifiers, body_tokens=body_tokens)


class FunctionDeclaration(Declaration):
    def __init__(self, name: str, body_tokens: str = '', modifiers: List[str] = None):
        super().__init__(name, type=DeclarationType.FUNCTION.value, modifiers=modifiers, body_tokens=body_tokens)

        parameters, returnType = self.parse_function()
        self.parameters = parameters
        self.returnType = returnType

    def parse_function(self):
        match = re.search(r"fun (\w+)\((.*?)\)(?:: (\w+))?", self.body)
        params_str = match.group(2)
        return_type = match.group(3) if match.group(3) else "Unit"

        parameters = []
        params_list = params_str.split(',')
        for param in params_list:
            param = param.strip()
            if not param:
                continue
            param_match = re.match(r"(\w+): (\w+)(?: = (.+))?", param)
            if param_match:
                name = param_match.group(1)
                dtype = param_match.group(2)
                value = param_match.group(3) if param_match.group(3) else None
                parameters.append(Parameter(name, dtype, value))
        return parameters, return_type

    def to_dict(self):
        result = super().to_dict()
        result['parameters'] = [p.to_dict() for p in self.parameters]
        result['returnType'] = self.returnType
        result['body'] = self.body
        if self.declarations:
            result['declarations'] = [decl.to_dict() for decl in self.declarations]
        return result
