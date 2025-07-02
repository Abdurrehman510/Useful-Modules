import re
import os
from pathlib import Path

def parse_project_structure(content):
    # Extract project structure
    structure_pattern = r"Project Structure\ntext\n([\s\S]+?)File Contents"
    structure_match = re.search(structure_pattern, content)
    if not structure_match:
        raise ValueError("Could not find project structure in the content")
    
    structure_text = structure_match.group(1)
    
    # Extract file contents
    file_pattern = r"(\d+\. .+?)\n([\s\S]+?)(?=\d+\. |$)"
    file_matches = re.finditer(file_pattern, content[len(structure_text):])
    
    # Parse structure into directory tree
    dir_tree = {}
    for line in structure_text.split('\n'):
        if line.strip():
            depth = len(re.match(r'^[├│└─ ]+', line).group()) if re.match(r'^[├│└─ ]+', line) else 0
            name = line.strip().replace('├── ', '').replace('│   ', '').replace('└── ', '')
            if depth == 0:
                current_path = [name]
                dir_tree[name] = {}
            else:
                parent = '/'.join(current_path[:depth//4])
                if name.endswith('.py') or name.endswith('.txt') or name.endswith('.md'):
                    dir_tree.setdefault(parent, {})[name] = None
                else:
                    current_path = current_path[:depth//4] + [name]
                    dir_tree['/'.join(current_path)] = {}
    
    # Parse file contents
    files = {}
    for match in file_matches:
        title = match.group(1)
        file_content = match.group(2).strip()
        
        # Extract file path from title
        if 'config/' in title:
            file_path = title.split('config/')[-1].strip()
            file_path = f"config/{file_path}"
        elif 'src/' in title:
            file_path = title.split('src/')[-1].strip()
            file_path = f"src/{file_path}"
        elif 'tests/' in title:
            file_path = title.split('tests/')[-1].strip()
            file_path = f"tests/{file_path}"
        elif title.endswith('requirements.txt'):
            file_path = 'requirements.txt'
        elif title.endswith('Dockerfile'):
            file_path = 'Dockerfile'
        elif title.endswith('README.md'):
            file_path = 'README.md'
        else:
            # Handle numbered items that don't have paths in title
            if '1.' in title:
                file_path = 'config/settings.py'
            elif '2.' in title:
                file_path = 'src/core/data/collectors/yahoo_finance.py'
            # Add more mappings as needed
            
        files[file_path] = file_content
    
    return dir_tree, files

def create_project_structure(dir_tree, files):
    # Create directories and files
    for path, children in dir_tree.items():
        # Create directory
        dir_path = Path(path)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create files in this directory
        for filename, _ in children.items():
            file_path = dir_path / filename
            file_content = files.get(str(file_path), "")
            
            # Handle special cases for empty __init__.py files
            if filename == '__init__.py' and not file_content:
                file_content = ''
            
            with open(file_path, 'w') as f:
                f.write(file_content)
    
    # Create files not in the directory tree (like requirements.txt)
    for file_path, content in files.items():
        if not Path(file_path).exists():
            with open(file_path, 'w') as f:
                f.write(content)

def main():
    # Read the input file
    with open('project.txt', 'r',encoding='utf-8') as f:
        content = f.read()
    
    # Parse the structure and files
    dir_tree, files = parse_project_structure(content)
    
    # Create the project structure
    create_project_structure(dir_tree, files)
    
    print("Project structure created successfully!")

if __name__ == "__main__":
    main()