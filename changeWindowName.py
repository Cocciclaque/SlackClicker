import win32gui


def set_window_name(text):
    try:
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetWindowText(hwnd, text)
    except:
        pass