import os
import shutil

def src_to_dest(src, dest):
    # ensure src exists
    src = os.path.abspath(src)
    print(f"Source dir: {src}")
    if not os.path.exists(src):
        raise ValueError(f"Source directory - {src} - do not exist.")
    
    # if dest do not exist, create it
    dest = os.path.abspath(dest)
    print(f"Dest dir: {dest}")
    if not os.path.exists(dest):
        print(f"Creating {dest} directory...")
        os.mkdir(dest)
        print(f"Directory '{dest}' created.")
    else:
        # delete all contents of dest, then create a fresh dest
        print(f"Directory '{dest}' exists.")
        try:
            shutil.rmtree(dest)
            print(f"Directory '{dest}' and its contents deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        os.mkdir(dest)
    
    # copy all contents of src to dest
    contents = os.listdir(src)
    files = []
    dirs = []
    for content in contents:
        if os.path.isfile(os.path.join(src, content)):
            files.append(content)
        else:
            dirs.append(content)
    
    for file in files:
        shutil.copy(os.path.join(src, file), dest)
    
    for d in dirs:
        src_to_dest(os.path.join(src, d), os.path.join(dest, d))