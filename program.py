import json

from declaration import Declaration, FunctionDeclaration
from parsers import find_all_function_declarations


class Program:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()

        self.tokens = file_content.split()
        self.file_paths = file_path

        self.declarations = []
        self.declarations.extend(find_all_function_declarations(self.tokens))

    def add_declaration(self, declaration: Declaration):
        self.declarations.append(declaration)

    def to_dict(self):
        def declaration_to_dict(declaration):
            if isinstance(declaration, FunctionDeclaration):
                return {
                    'type': declaration.type,
                    'name': declaration.name,
                    'parameters': [param.__dict__ for param in declaration.parameters],
                    'returnType': declaration.returnType,
                    'body': declaration.body,
                    'declarations': [declaration_to_dict(decl) for decl in declaration.declarations]
                }
            else:
                return declaration.__dict__

        return [declaration_to_dict(decl) for decl in self.declarations]

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)
