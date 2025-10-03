import argparse
import code
import os
import re
import sys
import gzip

defs = """
import multiprocessing
sender_queue : multiprocessing.Queue
return_queue : multiprocessing.Queue
pid: int
args: list
process_name: str

"""

entry = """
def entry(args, sys_queue, proc_queue, epid):
    global args, sys_queue, proc_queue, pid
    args = args
    ssender_queue = sys_queue
    return_queue = proc_queue
    pid = epid
    main()

"""

def compile_file(input_file: str, output_file: str = None):
    if not os.path.isfile(input_file):
        print(f"[Error] File not found: {input_file}")
        sys.exit(1)

    if not input_file.endswith(".py"):
        print("[Error] Only .py files are supported")
        sys.exit(1)

    # Ziel-Dateiname setzen
    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = base + ".mpy"

    # Inhalt laden
    with open(input_file, "r", encoding="utf-8") as f:
        code = f.read()

    # Prüfen ob main() vorhanden ist
    if "def main(" not in code:
        print("[Error] No main Function found")
        sys.exit(1)
    
    comp_code = replace_calls(code)

    file_code = add_header(comp_code, input_file)

    # Datei speichern
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(file_code)
    print(f"[OK] Compiled {input_file} → {output_file}")

def replace_calls(text:str):
    txt = ""
    for line in text.splitlines():
        if "from .system import *" in line:
            with open("imple\\system.py", "r")as f:
                        imp = ""
                        tet = f.read()
                        for l in tet.splitlines():
                             if tet.splitlines().index(l) > 8:
                                  imp = imp + l + "\n"
            line = f"{imp} \n"
        if "from .windows import *" in line:
            with open("imple\\windows.py", "r")as f:
                    imp = f.read()
            line = f"\n{imp} \n"
        txt = txt + line + "\n"
    


    return txt
            


def add_header(text:str,input_file):
    base, _ = os.path.splitext(input_file)
    type_id = 4 if "set_exec_prio(0)" not in text else 0
    includes = []
    exports = []
    procces_name = base if re.match("set_proc_name([a-z])", text) else base
    fsize = str(len(text)).encode().hex()
    HEADER = f"#{type_id}\n#{includes}\n#{exports}\n#{procces_name}\n#{fsize}"
    return HEADER + "\n" + text
        

def main():
    parser = argparse.ArgumentParser(
        description="Custom Python Compiler to .mpy format"
    )
    parser.add_argument(
        "file",
        help="Input Python file (.py) to compile"
    )
    parser.add_argument(
        "-o", "--output",
        help="Optional output file (.mpy)"
    )

    args = parser.parse_args()
    compile_file(args.file, args.output)



if __name__ == "__main__":
    main()