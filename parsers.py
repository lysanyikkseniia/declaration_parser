from declaration import FunctionDeclaration, PropertyDeclaration, ObjectDeclaration, ClassDeclaration, TypeDeclaration
from util_enums import DeclarationKeyword, ModifiersKeyword


def parse_from_tokens(tokens):  # returns rough list of dictionaries of first-level declarations
    declarations = []
    i = 0
    n = len(tokens)
    declaration_keywords = [kw.value for kw in DeclarationKeyword]

    while i < n:
        if tokens[i] in declaration_keywords:
            declaration_keyword = tokens[i]
            j = i - 1

            # Collect modifiers that are just before the declaration keyword
            modifiers = []
            while j >= 0 and tokens[j] in [mk.value for mk in ModifiersKeyword]:
                modifiers.insert(0, tokens[j])
                j -= 1

            # Start collecting the body tokens from the declaration keyword itself
            body_tokens = []
            brace_count = 0
            has_brace_started = False
            body_end = i
            is_parent = False
            while body_end < n:
                token = tokens[body_end]
                if '{' in token:
                    brace_count += token.count('{')
                    has_brace_started = True
                if '}' in token:
                    brace_count -= token.count('}')

                if token in declaration_keywords and body_end != i:
                    is_parent = True

                body_tokens.append(token)

                if has_brace_started and brace_count == 0:
                    break
                body_end += 1

            s = body_tokens[1]
            name = s[:min([s.find(b) for b in '([{<' if b in s] + [len(s)])]

            # Store the collected information
            declarations.append({"DeclarationKeyword": declaration_keyword, "modifiers": modifiers, "name": name,
                                 "body_tokens": body_tokens, "is_parent": is_parent})

            # Move index past the body end
            i = body_end + 1
        else:
            i += 1

    return declarations


def declaration_from_dict(declaration_raw):  # takes a dictionary and creates a declaration object
    key_to_class_map = {"class": ClassDeclaration, "object": ObjectDeclaration, "fun": FunctionDeclaration,
                        "val": PropertyDeclaration, "var": PropertyDeclaration, "typealias": TypeDeclaration}
    declaration = key_to_class_map[declaration_raw["DeclarationKeyword"]](name=declaration_raw["name"],
                                                                          body_tokens=declaration_raw["body_tokens"],
                                                                          modifiers=declaration_raw["modifiers"])
    if declaration_raw["is_parent"]:
        children_dict_list = parse_from_tokens(
            declaration_raw["body_tokens"][1:])  # returns rough list of dictionaries of inside declarations
        for child_dictionary in children_dict_list:
            child_declaration = declaration_from_dict(child_dictionary)
            declaration.add_declaration(child_declaration)

    return declaration
