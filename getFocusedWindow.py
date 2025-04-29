import win32gui, win32process, psutil
def is_active_window_process_name(name):
    try:
        pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
        print(win32gui.GetForegroundWindow())
        return(psutil.Process(pid[-1]).name() == name)
    except:
        pass
