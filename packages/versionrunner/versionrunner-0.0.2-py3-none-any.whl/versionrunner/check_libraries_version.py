import ast
import importlib
import pkg_resources
import re

def extract_imports_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
        
    imports = set()
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])  # import ...
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module.split('.')[0])  # from ... import ...
    return imports

def get_module_version(module_name):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, '__version__'):
            version = module.__version__
        elif hasattr(module, 'version'):
            version = module.version
        
        if isinstance(version, str):
            version_number = re.match(r'^\d+(\.\d+)*', version)  # extract the version. ex : 2.3.1
            if version_number:
                return version_number.group(0)

    except Exception as ex:
        return None 

def search_version(file_path, output_file='requirements.txt'):
    imported_modules = extract_imports_from_file(file_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for module_name in imported_modules:
            version = get_module_version(module_name)
            if version:
                f.write(f"{module_name}=={version}\n")
            else:
                try:
                    pkg_version = pkg_resources.get_distribution(module_name).version
                    f.write(f"{module_name}=={pkg_version}\n")
                except Exception as ex:
                    pass 
    
    print(f"'{output_file}' generated.")