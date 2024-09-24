import re
import os


class CodeProcessor:
    DEFINE_PATTERN = re.compile(r"^\s*#DEFINE\s+(\w+)\s*=\s*(.+)")
    IF_PATTERN = re.compile(r"^\s*#IF\s+(.+)")
    ENDIF_PATTERN = re.compile(r"^\s*#ENDIF")

    @staticmethod
    def evaluate_condition(condition, variables):
        try:
            return eval(condition, {}, variables)
        except NameError as e:
            print(f"Error: {e}")
            return False

    @classmethod
    def process_code(cls, code, global_variables=None):
        if global_variables is None:
            global_variables = {}

        variables = global_variables
        execute = True
        processed_lines = []

        for line in code.splitlines():
            if define_match := cls.DEFINE_PATTERN.match(line):
                var_name = define_match.group(1).strip()
                var_value = eval(define_match.group(2).strip(), {}, variables)
                variables[var_name] = var_value

            elif if_match := cls.IF_PATTERN.match(line):
                condition = if_match.group(1).strip()
                execute = cls.evaluate_condition(condition, variables)
            elif cls.ENDIF_PATTERN.match(line):
                execute = True
            elif execute:
                processed_lines.append(line)

        return '\n'.join(processed_lines)


def build(global_variables, allowed_extensions, src_directory='src', output_directory='build/odoo{ODOO_VERSION}'):
    assert global_variables is not None, ValueError('Please provide all the global variables using the parameter "global_variables"')

    output_directory = output_directory.format(**global_variables)
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(src_directory):
        if filename.split('.')[-1] in allowed_extensions:
            with open(os.path.join(src_directory, filename), 'r') as file:
                code = file.read()
            processed_code = CodeProcessor.process_code(code, global_variables)

            # Write processed code to a new file
            output_file_path = os.path.join(output_directory, filename)
            with open(output_file_path, 'w') as output_file:
                output_file.write(processed_code)


if __name__ == '__main__':
    build({'ODOO_VERSION': 17}, ['py', 'css'], 'src', 'build/odoo{ODOO_VERSION}')
