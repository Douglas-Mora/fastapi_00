import os
import ast
from openpyxl import Workbook

def extract_info(file_path):
    """
    Extracts information about classes, functions, and imports from a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        dict: A dictionary containing information about classes, functions, and imports.
    """
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read(), filename=file_path)
        
    classes = []
    functions = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.extend(alias.name for alias in node.names)
    
    return {'classes': classes, 'functions': functions, 'imports': imports}

def map_current_directory():
    """
    Maps the current directory and all its subdirectories, extracting information from Python files.

    Returns:
        dict: A dictionary mapping file paths to their corresponding information.
    """
    current_directory = os.getcwd()
    mapping = {}

    for root, dirs, files in os.walk(current_directory):
        for file_name in files:
            if file_name.endswith('.py'):  # Process only Python files
                file_path = os.path.join(root, file_name)
                mapping[file_path] = extract_info(file_path)
    
    return mapping

def save_to_excel(mapping):
    """
    Saves mapping data to an Excel file.

    Args:
        mapping (dict): A dictionary mapping file paths to their corresponding information.
    """
    wb = Workbook()
    ws = wb.active
    ws.append(['File', 'Classes', 'Functions', 'Imports'])

    for file_path, info in mapping.items():
        ws.append([file_path, ', '.join(info['classes']), ', '.join(info['functions']), ', '.join(info['imports'])])

    wb.save('mapping_data.xlsx')

if __name__ == "__main__":
    # Map current directory and save data to Excel
    mapping = map_current_directory()
    save_to_excel(mapping)
