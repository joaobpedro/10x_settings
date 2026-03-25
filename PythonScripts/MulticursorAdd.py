import N10X

# Boolean to toggle this behavior (so you can turn it off/on)
_multicursor_mode = True 

def OnMouseClickAddCursor(pos):
    """
    pos is a tuple (x, y) provided by the 10x API.
    """
    if _multicursor_mode:
        # ControlKeyHeld() is a handy 10x function 
        # so you only add a cursor if holding Ctrl while clicking
        if N10X.Editor.ControlKeyHeld():
            N10X.Editor.AddCursor(pos)
            # Return True to tell 10x we handled the click
            # and it shouldn't clear other cursors.
            return True 
    return False

def ToggleMultiClickMode():
    global _multicursor_mode
    _multicursor_mode = not _multicursor_mode
    state = "Enabled" if _multicursor_mode else "Disabled"
    N10X.Editor.SetStatusBarText(f"Multi-Cursor Click: {state}")

# --- Registration ---
# This tells 10x to run our function whenever the mouse clicks in the editor
N10X.Editor.AddMouseSelectStartedFunction(OnMouseClickAddCursor)