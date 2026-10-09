import os

project_root = r"C:\Users\VEDANT\Documents\antigravity\hopeful-bose"
output_file = r"C:\Users\VEDANT\Documents\antigravity\hopeful-bose\project_context.md"

exclude_dirs = {'.git', 'venv', '__pycache__', 'node_modules', 'dist', '.pytest_cache', 'build', 'docs', 'screenshots', '.oxlintrc.json', 'data'}
include_extensions = {'.py', '.ts', '.tsx', '.css', '.html', '.md', '.json', '.toml', '.yaml', '.yml'}
exclude_files = {'package-lock.json'}

with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("# Project Context\n\n")
    outfile.write("This document contains all the code and features of the project.\n\n")
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file in exclude_files or file == "project_context.md":
                continue
            ext = os.path.splitext(file)[1]
            if ext in include_extensions:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_root)
                outfile.write(f"## File: {rel_path}\n\n")
                # map extension to markdown language
                lang = ext[1:]
                if lang == 'tsx' or lang == 'ts':
                    lang = 'typescript'
                elif lang == 'py':
                    lang = 'python'
                outfile.write(f"```{lang}\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"Error reading file: {e}\n")
                outfile.write(f"\n```\n\n")

print(f"Context written to {output_file}")
