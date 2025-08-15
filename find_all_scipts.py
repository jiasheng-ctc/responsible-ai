import os

def print_python_docker_structure_and_code(root_dir=".", exclude_dirs=None, exclude_files=None, output_file="python_docker_files1.txt"):
    """
    Saves the directory structure and content of Python scripts, Docker files, 
    Docker Compose files, requirements files, and environment files (.env).

    Args:
        root_dir (str): The root directory to start scanning. Defaults to the current directory.
        exclude_dirs (list): List of directories to exclude from scanning.
        exclude_files (list): List of files to exclude from scanning.
        output_file (str): The file to save the output.
    """
    if exclude_dirs is None:
        exclude_dirs = ["node_modules", "dist", "build", "venv", "__pycache__", ".git", ".next", "out", ".venv", "env"]
    if exclude_files is None:
        exclude_files = [os.path.basename(__file__)]

    # Python file extensions
    python_extensions = {".py", ".pyw"}
    
    # Specific target files to include (case-insensitive matching)
    target_files = {
        "dockerfile", "dockerfile.dev", "dockerfile.prod", "dockerfile.test",
        "docker-compose.yml", "docker-compose.yaml", 
        "docker-compose.dev.yml", "docker-compose.prod.yml",
        "docker-compose.test.yml", "docker-compose.override.yml",
        "requirements.txt", "requirements-dev.txt", "requirements-prod.txt", "requirements-test.txt",
        "pyproject.toml", "setup.py", "setup.cfg",
        "pipfile", "pipfile.lock", "poetry.lock",
        "conda.yml", "environment.yml", "environment.yaml",
        ".env", ".env.local", ".env.dev", ".env.development", ".env.prod", ".env.production",
        ".env.test", ".env.testing", ".env.staging", ".env.example", ".env.template"
    }

    with open(output_file, "w", encoding="utf-8") as out_file:
        out_file.write("Python Scripts, Docker Files, Dependencies, and Environment Files Structure and Code:\n")
        out_file.write("=" * 80 + "\n\n")

        total_files = 0
        included_files = 0

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

            # Only show directories that contain target files
            has_target_files = False
            target_files_in_dir = []
            
            for filename in filenames:
                if filename in exclude_files:
                    continue
                    
                total_files += 1
                file_ext = os.path.splitext(filename)[1].lower()
                filename_lower = filename.lower()
                
                # Check if file should be included
                should_include = (
                    file_ext in python_extensions or 
                    filename_lower in target_files or
                    filename_lower.startswith('dockerfile') or
                    filename_lower.startswith('.env')
                )
                
                if should_include:
                    has_target_files = True
                    target_files_in_dir.append(filename)
                    included_files += 1

            # Only write directory info if it contains target files
            if has_target_files:
                indent_level = dirpath.count(os.sep)
                relative_path = os.path.relpath(dirpath, root_dir)
                out_file.write("  " * indent_level + f"📁 [{relative_path}]\n")

                for filename in target_files_in_dir:
                    filepath = os.path.join(dirpath, filename)
                    file_type = get_file_type(filename, os.path.splitext(filename)[1].lower())
                    
                    out_file.write("  " * (indent_level + 1) + f"📄 {filename} ({file_type})\n")
                    
                    try:
                        with open(filepath, "r", encoding="utf-8") as file:
                            out_file.write("  " * (indent_level + 2) + "=" * 50 + " [CODE START] " + "=" * 50 + "\n")
                            line_number = 1
                            for line in file:
                                out_file.write("  " * (indent_level + 2) + f"{line_number:4d}: {line}")
                                line_number += 1
                            out_file.write("  " * (indent_level + 2) + "=" * 50 + " [CODE END] " + "=" * 52 + "\n\n")
                    except Exception as e:
                        out_file.write("  " * (indent_level + 2) + f"❌ [Error reading file: {e}]\n\n")

        # Write summary
        out_file.write("\n" + "=" * 80 + "\n")
        out_file.write("SUMMARY\n")
        out_file.write("=" * 80 + "\n")
        out_file.write(f"Total files scanned: {total_files}\n")
        out_file.write(f"Target files with content included: {included_files}\n")
        
        # Count by file type
        type_counts = {}
        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
            for filename in filenames:
                if filename in exclude_files:
                    continue
                file_ext = os.path.splitext(filename)[1].lower()
                filename_lower = filename.lower()
                
                if (file_ext in python_extensions or 
                    filename_lower in target_files or
                    filename_lower.startswith('dockerfile') or
                    filename_lower.startswith('.env')):
                    
                    file_type = get_file_type(filename, file_ext)
                    type_counts[file_type] = type_counts.get(file_type, 0) + 1
        
        out_file.write("\nFiles by type:\n")
        for file_type, count in sorted(type_counts.items()):
            out_file.write(f"  {file_type}: {count} files\n")

    print(f"✓ Repository structure saved to {output_file}")
    print(f"✓ Total files scanned: {total_files}")
    print(f"✓ Target files with content included: {included_files}")
    
    # Print type summary
    print("\nFiles found by type:")
    type_counts = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for filename in filenames:
            if filename in exclude_files:
                continue
            file_ext = os.path.splitext(filename)[1].lower()
            filename_lower = filename.lower()
            
            if (file_ext in python_extensions or 
                filename_lower in target_files or
                filename_lower.startswith('dockerfile') or
                filename_lower.startswith('.env')):
                
                file_type = get_file_type(filename, file_ext)
                type_counts[file_type] = type_counts.get(file_type, 0) + 1
    
    for file_type, count in sorted(type_counts.items()):
        print(f"  {file_type}: {count} files")

def get_file_type(filename, file_ext):
    """Determine the type of file based on name and extension."""
    filename_lower = filename.lower()
    
    if file_ext in [".py", ".pyw"]:
        return "Python Scripts"
    elif filename_lower.startswith('dockerfile'):
        return "Docker Files"
    elif 'docker-compose' in filename_lower:
        return "Docker Compose Files"
    elif 'requirements' in filename_lower and filename_lower.endswith('.txt'):
        return "Requirements Files"
    elif filename_lower in ['pyproject.toml', 'setup.py', 'setup.cfg']:
        return "Python Package Config"
    elif filename_lower in ['pipfile', 'pipfile.lock', 'poetry.lock']:
        return "Python Dependencies"
    elif filename_lower in ['conda.yml', 'environment.yml', 'environment.yaml']:
        return "Conda Environment Files"
    elif filename_lower.startswith('.env'):
        return "Environment Files"
    else:
        return "Other Config Files"

if __name__ == "__main__":
    print("Saving Python scripts, Docker files, dependencies, and environment files structure with code...")
    print_python_docker_structure_and_code()
    print("Done! Check python_docker_files.txt for output.")