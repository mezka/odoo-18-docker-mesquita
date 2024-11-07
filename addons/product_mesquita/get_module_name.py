import ast
import os

manifest_path = os.path.join(os.path.dirname(__file__), "__manifest__.py")

def get_module_name():
    with open(manifest_path, 'r') as manifest_file:
        manifest_data = ast.literal_eval(manifest_file.read())
        return manifest_data.get('name', 'Unnamed Module')
