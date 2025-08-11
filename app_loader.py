import os
import shutil

apps = []

def check_for_Apps(path):
    #print(f"#################\n{os.listdir()}\n#################")
    os.chdir(path)
    for item in os.listdir(path):
        if item.endswith(".py"):
            if item =="Definds.py":
                continue
            with open(item,"r") as f:
                draw = False
                handel = False
                setup = False
                for line in f.readlines():
                    if line.startswith(f"def {item.removesuffix(".py")}_Drawer"): draw = True
                    if line.startswith(f"def {item.removesuffix(".py")}_Handler"): handel = True
                    if line.startswith(f"def Window_SetUp"): setup = True
            
                if draw and handel and setup:
                    setup_file_to_run_on_gui(path, item)
                    print(f"A app named: {item.removesuffix(".py")} was found :)")
                else:
                    print(f"A file named: {item.removesuffix(".py")} was found :(")

def setup_file_to_run_on_gui(path, item):
    shutil.copy(f"{path}\\{item}", f"C:\\MOS\\TMP\\{item}")
    lines = []
    with open(f"C:\\MOS\\TMP\\{item}","r") as file:
        for line in file.readlines():
            if line.find("from .Definds import *") != -1: pass
            else:
                lines.append(line)
    
    with open(f"C:\\MOS\\TMP\\{item}","w") as file:
        file.write("")
        for line in lines:
            file.write(line)
    
    pass


if __name__ == "__main__":
    os.chdir("C:\\MOS\\TMP\\")
    for file in os.listdir():
        os.remove(file)
    check_for_Apps("D:\\OoBExp\\src\\GUI\\Apps")
    os.chdir("C:\\MOS\\TMP\\")
    print(f"#################\n{os.listdir()}\n#################")
