import os


def get_files_info(working_directory, directory="."):
    
    full_path = os.path.join(working_directory, directory)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_path)
    
    
    if not abs_target.startswith(abs_working):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if not os.path.isdir(abs_target):
        return (f'Error: "{directory}" is not a directory')
    
    items = os.listdir(abs_target)
    lines = []

    for name in items:
        item_path = os.path.join(abs_target, name)
        is_dir = os.path.isdir(item_path)
        size = os.path.getsize(item_path)
        line = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
        lines.append(line)
        
    return "\n".join(lines)