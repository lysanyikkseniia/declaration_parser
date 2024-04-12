import re

from declaration import Parameter, FunctionDeclaration


def parse_functions_from_tokens(a):
    pass


def find_all_function_declarations(tokens):
    declarations_list = []
    for fun in parse_functions_from_tokens(tokens):
        parsed_function = parse_function_from_string(fun)
        name = parsed_function[0][1].split('(')[0]
        signature = parsed_function[0][1]
        parameters = extract_parameters_from_signature(signature)
        match_type = re.compile(r'\):\s*(\w+)\s*$').search(signature)
        if match_type:
            returntype = match_type.group(1)
        else:
            returntype = 'Unit'
        declaration = FunctionDeclaration(name=name, parameters=parameters, returnType=returntype, body=fun)
        insides = parsed_function[0][2].strip()[1:].strip() + '}'
        if insides:
            insides_declarations = find_all_function_declarations(insides.split())
            if insides_declarations:
                for dec in insides_declarations:
                    declaration.add(dec)
        declarations_list.append(declaration)
    return declarations_list


def extract_parameters_from_signature(signature):
    signature = signature.replace('\n', ' ')
    param_string = re.search(r'\((.*)\)', signature, re.DOTALL)
    if param_string:
        param_string = param_string.group(1)
    else:
        return []
    params = re.findall(r'(\w+)\s*:\s*(\w+)(?:\s*=\s*([^,]+))?', param_string)
    parameters = [Parameter(name, type_, default.strip() if default is not None else None) for name, type_, default in
                  params]
    return parameters


def parse_function_from_string(file_contents):
    pattern = r'fun\s+([^\{]+)(\{.*?\})'
    matches = re.findall(pattern, file_contents, re.DOTALL)
    tokens = []
    for match in matches:
        function_signature, function_body = match
        tokens.append(('fun', function_signature.strip(), function_body.strip()))
    return tokens
