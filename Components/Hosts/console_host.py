import subprocess
import threading
import queue
import platform
import os
import shutil

class cmdHost:
    """
    Eine Klasse, die eine interaktive Shell-Session (CMD, PowerShell, Bash oder sh) verwaltet.
    - Unterstützt Windows (CMD, PowerShell) sowie Linux/macOS (Bash, sh).
    - Hält die Session dauerhaft offen, sodass Variablen und Verzeichnisse persistent bleiben.
    - Fallback-Mechanismus: wenn gewünschte Shell nicht verfügbar ist, wird automatisch auf eine andere gewechselt.
    """

    def __init__(self, shell: str = None):
        """
        Erstellt eine neue Shell-Session.

        Parameter:
        ----------
        shell : str | None
            - None        -> automatische Auswahl (Windows = CMD, Linux/macOS = Bash)
            - "cmd"       -> Windows CMD
            - "powershell"-> Windows PowerShell (Fallback: CMD, falls nicht installiert)
            - "bash"      -> Linux/macOS Bash (Fallback: sh, falls nicht installiert)
        """
        system = platform.system()

        # Automatische Auswahl: Windows = CMD, Linux/macOS = Bash
        if shell is None:
            shell = "cmd" if system == "Windows" else "bash"

        self.shell = shell
        self.end_marker = "__CMDHOST_END__"  # Marker, um Ende einer Befehlsausgabe zu erkennen

        # -------------------------
        # Windows CMD
        # -------------------------
        if shell == "cmd":
            self.exec_end = f"echo {self.end_marker}"
            program = ["cmd.exe"]

        # -------------------------
        # Windows PowerShell
        # -------------------------
        elif shell == "powershell":
            if shutil.which("powershell.exe"):
                # PowerShell verfügbar
                self.exec_end = f"echo {self.end_marker}"
                program = ["powershell.exe", "-NoLogo", "-NoProfile"]
            else:
                # Fallback auf CMD
                print("[WARN] PowerShell nicht gefunden, wechsle zu CMD.")
                self.exec_end = f"echo {self.end_marker}"
                program = ["cmd.exe"]
                self.shell = "cmd"

        # -------------------------
        # Linux/macOS Bash
        # -------------------------
        elif shell == "bash":
            if shutil.which("bash"):
                # Bash verfügbar
                self.exec_end = f"echo {self.end_marker}"
                program = ["bash"]
            elif shutil.which("sh"):
                # Fallback auf sh
                print("[WARN] Bash nicht gefunden, wechsle zu sh.")
                self.exec_end = f"echo {self.end_marker}"
                program = ["sh"]
                self.shell = "sh"
            else:
                raise EnvironmentError("Keine geeignete Shell (bash oder sh) gefunden!")

            # Prompt deaktivieren, damit die Ausgabe sauberer ist
            os.environ["PS1"] = ""

        else:
            raise ValueError(f"Unbekannte Shell: {shell}")

        # -------------------------
        # Prozess starten
        # -------------------------
        self.output_queue = queue.Queue()  # Thread-sichere Queue für stdout-Zeilen
        self.process = subprocess.Popen(
            program,
            stdin=subprocess.PIPE,   # Eingaben an die Shell
            stdout=subprocess.PIPE,  # Ausgabe der Shell
            stderr=subprocess.STDOUT, # Fehlerausgabe -> stdout
            text=True,
            bufsize=1
        )

        # Separater Thread zum Lesen der Shell-Ausgabe
        self.reader_thread = threading.Thread(target=self._reader, daemon=True)
        self.reader_thread.start()

    def _reader(self):
        """
        Liest kontinuierlich alle Ausgaben der Shell und speichert sie in der Queue.
        Wird in einem eigenen Thread ausgeführt.
        """
        for line in self.process.stdout:
            self.output_queue.put(line)

    def exec(self, command: str) -> str:
        """
        Führt einen Befehl in der aktiven Shell-Session aus und gibt die Ausgabe zurück.

        Parameter:
        ----------
        command : str
            Der auszuführende Befehl (z. B. "echo Hallo").

        Rückgabe:
        ---------
        str : Gesamte Ausgabe des Befehls (ohne Marker).
        """
        # Unterschiedliche Syntax für CMD (&) vs. Bash/PowerShell (;)
        if self.shell in ["bash", "sh", "powershell"]:
            full_command = f"{command} ; {self.exec_end}\n"
        else:  # CMD
            full_command = f"{command} & {self.exec_end}\n"

        # Befehl an die Shell senden
        self.process.stdin.write(full_command)
        self.process.stdin.flush()

        # Ausgabezeilen sammeln, bis der Marker erreicht wird
        output_lines = []
        while True:
            line = self.output_queue.get()
            if self.end_marker in line:
                break
            output_lines.append(line.rstrip())

        return "\n".join(output_lines)

    def close(self):
        """
        Beendet die Shell-Session sauber.
        """
        try:
            self.exec("exit")
        except Exception:
            pass
        self.process.terminate()

if __name__ == "__main__":
    # Automatische Shell-Wahl (Windows = CMD, Linux/macOS = Bash)
    host = cmdHost()
    print(host.exec("echo Hallo Welt"))
    host.close()

    # Windows mit PowerShell (Fallback auf CMD falls PowerShell fehlt)
    host = cmdHost("powershell")
    print(host.exec("Write-Output 'Hallo aus PowerShell oder CMD'"))
    host.close()
