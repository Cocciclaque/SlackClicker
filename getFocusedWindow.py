import win32gui, win32process, psutil, win32com.client
import urllib.parse
def is_active_window_process_name(name):
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        return(psutil.Process(pid[-1]).name() == name)
    except:
        pass

def get_active_explorer_folder():
    """If the foreground window is an Explorer window, return its folder path, else None."""
    fg_hwnd = win32gui.GetForegroundWindow()
    shell = win32com.client.Dispatch("Shell.Application")
    for window in shell.Windows():
        try:
            # Match on window handle
            if int(window.HWND) == fg_hwnd:
                # Only handle filesystem explorers
                # window.LocationURL is like 'file:///C:/Users/...'
                url = window.LocationURL
                if url.startswith('file:///'):
                    # decode URL to normal path
                    path = urllib.parse.unquote(url[8:]).replace('/', '\\')
                    return path
        except Exception:
            continue
    return None
