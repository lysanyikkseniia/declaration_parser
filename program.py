import json

from declaration import Declaration, FunctionDeclaration
from parsers import parse_from_tokens, declaration_from_dict


class Program:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
        self.declarations = []
        tokens = file_content.split()
        self.tokens = tokens
        self.process_token_list(tokens)

    def add_declaration(self, declaration: Declaration):
        self.declarations.append(declaration)

    def process_token_list(self, tokens):
        declarations_dictionary = parse_from_tokens(tokens)
        for declaration_raw in declarations_dictionary:
            declaration = declaration_from_dict(declaration_raw)  # some inner logic does everything right
            self.add_declaration(declaration)

    def to_dict(self):
        def declaration_to_dict(declaration):
            if isinstance(declaration, FunctionDeclaration):
                result = {'type': declaration.type, 'name': declaration.name, 'parameters': [
                    {'name': param.name, 'type': param.type, **({'value': param.value} if param.value else {})} for
                    param in declaration.parameters], 'returnType': declaration.returnType, 'body': declaration.body, }
                if declaration.declarations:
                    result['declarations'] = [declaration_to_dict(decl) for decl in declaration.declarations]
                return result
            # TODO ELSE (maybe move to declaration class methods??)

        return {"declarations": [declaration_to_dict(decl) for decl in self.declarations]}

    def to_json(self):
        return json.dumps(self.to_dict())

    def export_declarations_to_json(self, file_path):
        with open(file_path, "w") as outfile:
            outfile.write(self.to_json())
