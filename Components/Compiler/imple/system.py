import multiprocessing
sender_queue : multiprocessing.Queue
return_queue : multiprocessing.Queue
pid: int
args: list
process_name: str

#
# Imports:
#

# Basic Handle
type Handle = int
# Window Class Handle
type WCH = Handle
# Window Handle
type WH = Handle
# Process ID
type PID = int
# File Handle
type FH = Handle
# Library Handle
type LH = Handle
# Service Handle
type SH = Handle
# Hook Handle
type HKH = Handle
# Process Handle
type PH = Handle

# Basic process information functions
def get_args()->list:return args
def get_pid()->int:return pid
def get_process_name()->str:return process_name
def get_parent_pid()->int:
    sender_queue.put(("GET_PARENT_PID",pid))
    ret = return_queue.get()
    return ret[1] if ret[1]<pid else None

# Window management functions
def create_window_class(name, **kwargs)->WCH:
    sender_queue.put(("CREATE_WINDOW_CLASS", name, kwargs))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def delete_window_class(wch:WCH)->bool:
    sender_queue.put(("DELETE_WINDOW_CLASS", wch))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def create_window(wch: WCH, **kwargs) -> WH | None:
    sender_queue.put(("CREATE_WINDOW", wch, kwargs))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def open_window(wh: WH) -> bool:
    sender_queue.put(("OPEN_WINDOW", wh))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def close_window(handle: WH) -> bool:
    sender_queue.put(("CLOSE_WINDOW", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def destroy_window(handle: WH) -> bool:
    sender_queue.put(("DESTROY_WINDOW", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_window_info(handle: WH) -> dict | None:
    sender_queue.put(("GET_WINDOW_INFO", handle))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def list_windows(arg=None) -> list:
    sender_queue.put(("LIST_WINDOWS", arg))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def focus_window(handle: WH) -> bool:
    sender_queue.put(("FOCUS_WINDOW", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def minimize_window(handle: WH) -> bool:
    sender_queue.put(("MINIMIZE_WINDOW", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def maximize_window(handle: WH) -> bool:
    sender_queue.put(("MAXIMIZE_WINDOW", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def restore_window(handle: WH) -> bool:
    sender_queue.put(("RESTORE_WINDOW", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def move_window(handle: WH, x: int, y: int) -> bool:
    sender_queue.put(("MOVE_WINDOW", handle, x, y))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def resize_window(handle: WH, width: int, height: int) -> bool:
    sender_queue.put(("RESIZE_WINDOW", handle, width, height))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def set_window_title(handle: WH, title: str) -> bool:
    sender_queue.put(("SET_WINDOW_TITLE", handle, title))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_window_title(handle: WH) -> str | None:
    sender_queue.put(("GET_WINDOW_TITLE", handle))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def set_window_zlayer(handle: WH, zlayer: int) -> bool:
    sender_queue.put(("SET_WINDOW_ZLAYER", handle, zlayer))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_window_zlayer(handle: WH) -> int | None:
    sender_queue.put(("GET_WINDOW_ZLAYER", handle))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def set_window_icon(handle: WH, icon_path: str) -> bool:
    sender_queue.put(("SET_WINDOW_ICON", handle, icon_path))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_window_icon(handle: WH) -> str | None:
    sender_queue.put(("GET_WINDOW_ICON", handle))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def draw_window(handle: WH) -> bool:
    sender_queue.put(("DRAW_WINDOW", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_window_events(handle: WH) -> list:
    sender_queue.put(("GET_WINDOW_EVENTS", handle))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []


# ---------------- Process management ----------------
def create_process(file: str, args: list) -> PID | None:
    sender_queue.put(("CREATE_PROCESS", file, args))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def kill_process(pid: PID) -> bool:
    sender_queue.put(("KILL_PROCESS", pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def list_processes() -> list:
    sender_queue.put(("LIST_PROCESSES",))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def get_process_info(pid: PID) -> dict | None:
    sender_queue.put(("GET_PROCESS_INFO", pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def wait_process(pid: PID, timeout: int = None) -> int | None:
    sender_queue.put(("WAIT_PROCESS", pid, timeout))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def send_signal(pid: PID, signal: int) -> bool:
    sender_queue.put(("SEND_SIGNAL", pid, signal))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def receive_signal() -> tuple | None:
    sender_queue.put(("RECEIVE_SIGNAL",))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def expand_permissions() -> bool:
    sender_queue.put(("EXPAND_PERMISSIONS",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]


# ---------------- File management ----------------
def open_file(path: str, mode: str) -> FH | None:
    sender_queue.put(("OPEN_FILE", path, mode))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def read_file(handle: FH) -> bytes | None:
    sender_queue.put(("READ_FILE", handle))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def write_file(handle: FH, data: bytes) -> int | None:
    sender_queue.put(("WRITE_FILE", handle, data))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def close_file(handle: FH) -> bool:
    sender_queue.put(("CLOSE_FILE", handle))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_file_info(handle: FH) -> dict | None:
    sender_queue.put(("GET_FILE_INFO", handle))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def list_files(directory: str) -> list:
    sender_queue.put(("LIST_FILES", directory))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def delete_file(path: str) -> bool:
    sender_queue.put(("DELETE_FILE", path))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def move_file(src: str, dest: str) -> bool:
    sender_queue.put(("MOVE_FILE", src, dest))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def copy_file(src: str, dest: str) -> bool:
    sender_queue.put(("COPY_FILE", src, dest))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def create_directory(path: str) -> bool:
    sender_queue.put(("CREATE_DIRECTORY", path))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def delete_directory(path: str) -> bool:
    sender_queue.put(("DELETE_DIRECTORY", path))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def list_directories(path: str) -> list:
    sender_queue.put(("LIST_DIRECTORIES", path))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def get_current_directory() -> str | None:
    sender_queue.put(("GET_CURRENT_DIRECTORY",))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def change_directory(path: str) -> bool:
    sender_queue.put(("CHANGE_DIRECTORY", path))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def file_exists(path: str) -> bool:
    sender_queue.put(("FILE_EXISTS", path))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else False

def directory_exists(path: str) -> bool:
    sender_queue.put(("DIRECTORY_EXISTS", path))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else False

def get_file_size(path: str) -> int | None:
    sender_queue.put(("GET_FILE_SIZE", path))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

# ---------------- System information ----------------
def get_system_info() -> dict | None:
    sender_queue.put(("GET_SYSTEM_INFO",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def get_uptime() -> int | None:
    sender_queue.put(("GET_UPTIME",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def get_memory_info() -> dict | None:
    sender_queue.put(("GET_MEMORY_INFO",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def get_cpu_info() -> dict | None:
    sender_queue.put(("GET_CPU_INFO",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def get_disk_info() -> dict | None:
    sender_queue.put(("GET_DISK_INFO",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def get_network_info() -> dict | None:
    sender_queue.put(("GET_NETWORK_INFO",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None


# ---------------- Miscellaneous ----------------
def sleep(seconds: int) :
    import time
    time.sleep(seconds)

def execute_command(command: str) -> str | None:
    sender_queue.put(("EXECUTE_COMMAND", command,pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def log(message: str, level: str = "INFO") -> bool:
    sender_queue.put(("LOG", message, level,pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def set_env_variable(key: str, value: str) -> bool:
    sender_queue.put(("SET_ENV_VARIABLE", key, value,pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_env_variable(key: str) -> str | None:
    sender_queue.put(("GET_ENV_VARIABLE", key,pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def list_env_variables() -> dict:
    sender_queue.put(("LIST_ENV_VARIABLES",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else {}

def clear_env_variables() -> bool:
    sender_queue.put(("CLEAR_ENV_VARIABLES",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]


# ---------------- Event handling ----------------
def wait_event(event_type: str, timeout: int = None) -> dict | None:
    sender_queue.put(("WAIT_EVENT", event_type, timeout))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def send_event(event: dict) -> bool:
    sender_queue.put(("SEND_EVENT", event))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def list_events() -> list:
    sender_queue.put(("LIST_EVENTS",))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def clear_events() -> bool:
    sender_queue.put(("CLEAR_EVENTS",))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def register_event_handler(event_type: str, handler) -> bool:
    sender_queue.put(("REGISTER_EVENT_HANDLER", event_type, handler))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def unregister_event_handler(event_type: str, handler) -> bool:
    sender_queue.put(("UNREGISTER_EVENT_HANDLER", event_type, handler))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_event_handlers(event_type: str) -> list:
    sender_queue.put(("GET_EVENT_HANDLERS", event_type))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def clear_event_handlers(event_type: str) -> bool:
    sender_queue.put(("CLEAR_EVENT_HANDLERS", event_type))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def clear_all_event_handlers() -> bool:
    sender_queue.put(("CLEAR_ALL_EVENT_HANDLERS",))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]


# ---------------- System control ----------------
def shutdown() -> bool:
    sender_queue.put(("SHUTDOWN",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def reboot() -> bool:
    sender_queue.put(("REBOOT",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def suspend() -> bool:
    sender_queue.put(("SUSPEND",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def resume() -> bool:
    sender_queue.put(("RESUME",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def lock() -> bool:
    sender_queue.put(("LOCK",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def unlock() -> bool:
    sender_queue.put(("UNLOCK",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]


# ---------------- Debugging ----------------
def enable_debugging() -> bool:
    sender_queue.put(("ENABLE_DEBUGGING",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def disable_debugging() -> bool:
    sender_queue.put(("DISABLE_DEBUGGING",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def is_debugging_enabled() -> bool:
    sender_queue.put(("IS_DEBUGGING_ENABLED",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else False

def log_debug(message: str) -> bool:
    sender_queue.put(("LOG_DEBUG", message,pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_debug_logs() -> list:
    sender_queue.put(("GET_DEBUG_LOGS",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def clear_debug_logs() -> bool:
    sender_queue.put(("CLEAR_DEBUG_LOGS",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def set_debug_level(level: str) -> bool:
    sender_queue.put(("SET_DEBUG_LEVEL", level,pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_debug_level() -> str | None:
    sender_queue.put(("GET_DEBUG_LEVEL",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None


# ---------------- Services ----------------
def start_service(name: str) -> bool:
    sender_queue.put(("START_SERVICE", name))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def stop_service(name: str) -> bool:
    sender_queue.put(("STOP_SERVICE", name))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def restart_service(name: str) -> bool:
    sender_queue.put(("RESTART_SERVICE", name))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_service_status(name: str) -> str | None:
    sender_queue.put(("GET_SERVICE_STATUS", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def list_services() -> list:
    sender_queue.put(("LIST_SERVICES",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def enable_service(name: str) -> bool:
    sender_queue.put(("ENABLE_SERVICE", name))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def disable_service(name: str) -> bool:
    sender_queue.put(("DISABLE_SERVICE", name))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def is_service_enabled(name: str) -> bool:
    sender_queue.put(("IS_SERVICE_ENABLED", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else False

def get_service_info(name: str) -> dict | None:
    sender_queue.put(("GET_SERVICE_INFO", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def set_service_config(name: str, config: dict) -> bool:
    sender_queue.put(("SET_SERVICE_CONFIG", name, config))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_service_config(name: str) -> dict | None:
    sender_queue.put(("GET_SERVICE_CONFIG", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def list_service_configs() -> dict:
    sender_queue.put(("LIST_SERVICE_CONFIGS",pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else {}

def register_service(name: str, handler) -> bool:
    sender_queue.put(("REGISTER_SERVICE", name, handler))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def unregister_service(name: str) -> bool:
    sender_queue.put(("UNREGISTER_SERVICE", name))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]


# ---------------- System hooks ----------------
def register_hook(hook_type: str, handler) -> bool:
    sender_queue.put(("REGISTER_HOOK", hook_type, handler,pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def unregister_hook(hook_type: str, handler) -> bool:
    sender_queue.put(("UNREGISTER_HOOK", hook_type, handler,pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def get_hooks(hook_type: str) -> list:
    sender_queue.put(("GET_HOOKS", hook_type,pid))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def clear_hooks(hook_type: str) -> bool:
    sender_queue.put(("CLEAR_HOOKS", hook_type, pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def clear_all_hooks() -> bool:
    sender_queue.put(("CLEAR_ALL_HOOKS",pid))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]


# ---------------- Library management ----------------
def load_library(name: str) -> LH | None:
    sender_queue.put(("LOAD_LIBRARY", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def unload_library(lh: LH) -> bool:
    sender_queue.put(("UNLOAD_LIBRARY", lh))
    ret = return_queue.get()
    return True if ret[0] == 0 else ret[1]

def is_library_loaded_local(name: str) -> bool:
    sender_queue.put(("IS_LIBRARY_LOADED_LOCAL", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else False

def is_library_loaded_global(name: str) -> bool:
    sender_queue.put(("IS_LIBRARY_LOADED_GLOBAL", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else False

def list_global_loaded_libraries() -> list:
    sender_queue.put(("LIST_GLOBAL_LOADED_LIBRARIES",))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def get_library_info(name: str) -> dict | None:
    sender_queue.put(("GET_LIBRARY_INFO", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def get_library_functions(lh: LH) -> list:
    sender_queue.put(("GET_LIBRARY_FUNCTIONS", lh))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else []

def call_library_function(name: str, func: str, *args, **kwargs):
    sender_queue.put(("CALL_LIBRARY_FUNCTION", name, func, args, kwargs))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

def get_library_version(name: str) -> str | None:
    sender_queue.put(("GET_LIBRARY_VERSION", name))
    ret = return_queue.get()
    return ret[1] if ret[0] == 0 else None

# Extented Later
# ...