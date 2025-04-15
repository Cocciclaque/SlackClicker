import win32gui


def set_window_name(text):
    hwnd = win32gui.GetForegroundWindow()
    win32gui.SetWindowText(hwnd, text)
