import re

from declaration import FunctionDeclaration
from declaration import Parameter


def find_all_class_declarations(tokens):
    # Flags to keep track of whether 'class' has been found and if we are within the class definition
    found_class = False
    within_class_definition = False
    # Counter to manage nested curly braces
    curly_brace_count = 0

    class_definition_tokens = []

    for token in tokens:
        if token == 'class' and not found_class:
            # Mark that 'class' has been found and we are now within the class definition
            found_class = True
            within_class_definition = True
            class_definition_tokens.append(token)
        elif within_class_definition:
            class_definition_tokens.append(token)
            if token == '{':
                curly_brace_count += 1
            elif token == '}':
                curly_brace_count -= 1
                if curly_brace_count == 0:
                    within_class_definition = False
                    break

    # Join the tokens to form the class definition string
    class_definition_str = ' '.join(class_definition_tokens)

    # Optionally, you can format the string to look more like Kotlin code if desired
    # This is a basic approach and might need adjustments based on the actual tokenization and requirements

    return class_definition_str


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

    # Extract the parameter list from the signature
    param_string = re.search(r'\((.*)\)', signature, re.DOTALL)
    if param_string:
        param_string = param_string.group(1)
    else:
        return []

    # Regex to match parameter names, types, and optional default values
    params = re.findall(r'([\w]+)\s*:\s*([\w]+)(?:\s*=\s*([^,]+))?', param_string)

    # Create Parameter objects
    parameters = [Parameter(name, type_, default.strip() if default is not None else None) for name, type_, default in
                  params]
    return parameters


def parse_function_from_string(file_contents):
    # Regular expression to match Kotlin functions
    # Explanation:
    # - `fun\s+`: Matches the 'fun' keyword followed by one or more whitespace characters.
    # - `([^\{]+)`: Captures the function name and parameters, stopping before the opening brace.
    # - `(\{.*?\})`: Lazily captures the function body enclosed in braces, ignoring nested functions.
    # The `re.DOTALL` flag allows the dot `.` to match newline characters as well.
    pattern = r'fun\s+([^\{]+)(\{.*?\})'

    # Find all matches of Kotlin functions in the file
    matches = re.findall(pattern, file_contents, re.DOTALL)

    # Generate tokens for each match
    tokens = []
    for match in matches:
        function_signature, function_body = match
        tokens.append(('fun', function_signature.strip(), function_body.strip()))

    return tokens


def parse_functions_from_tokens(tokens):
    sections = []
    inside_fun = False
    brace_balance = 0
    current_section = []

    for token in tokens:
        if token == "fun" and (not inside_fun or brace_balance == 0):
            # If we're not already tracking a section or if we've closed the previous section, start a new one
            if inside_fun:  # Close the previous section before starting a new one
                sections.append(" ".join(current_section))
                current_section = []
            inside_fun = True
            brace_balance = 0
            current_section.append(token)
        elif inside_fun:
            current_section.append(token)
            if token == "{":
                brace_balance += 1
            elif token == "}":
                brace_balance -= 1
                if brace_balance == 0:
                    # End of the current section, append it if it's not going to be immediately followed by another 'fun'
                    if not (len(tokens) > tokens.index(token) + 1 and tokens[tokens.index(token) + 1] == "fun"):
                        sections.append(" ".join(current_section))
                        inside_fun = False
                        current_section = []

    # Append the last section if not already done
    if current_section:
        sections.append(" ".join(current_section))

    return sections
