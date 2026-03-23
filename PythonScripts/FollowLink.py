import N10X
import re
import os


# the external links need to be absolute paths
# Stack to keep track of previous locations for "jump back"
_jump_stack = []

def JumpToMarkdownLink():
    global _jump_stack
    line_text = N10X.Editor.GetCurrentLine()
    current_file = N10X.Editor.GetCurrentFilename()
    cursor_pos = N10X.Editor.GetCursorPos()

    # 1. Try to find a Markdown link: [text](path_or_heading)
    # Matches [label](target)
    match = re.search(r'\[.*\]\((.*)\)', line_text)
    
    if match:
        target = match.group(1).strip()
        
        # Save current position before jumping
        _jump_stack.append((current_file, cursor_pos))

        # Handle Internal (#my-heading)
        if target.startswith('#'):
            header_text = target[1:].replace('-', ' ') 
            _JumpToHeader(header_text)
        
        # Handle External
        else:
            full_path = target
            full_path = full_path.strip("<>")
            print(full_path)
            if os.path.exists(full_path):
                N10X.Editor.OpenFile(full_path)
            else:
                N10X.Editor.SetStatusBarText(f"File not found: {target}")
        return

    N10X.Editor.SetStatusBarText("No link found on current line.")

def _JumpToHeader(header_name):
    """Helper to find a header in the current file."""
    line_count = N10X.Editor.GetLineCount()
    # Search for a line starting with # that contains the header name
    for i in range(line_count):
        line = N10X.Editor.GetLine(i).lower()
        if line.strip().startswith('#') and header_name.lower() in line:
            N10X.Editor.SetCursorPos((0, i))
            N10X.Editor.CenterViewAtLinePos(i)
            return
    N10X.Editor.SetStatusBarText(f"Header '{header_name}' not found.")

def JumpBack():
    global _jump_stack
    if _jump_stack:
        file_path, pos = _jump_stack.pop()
        N10X.Editor.OpenFile(file_path)
        N10X.Editor.SetCursorPos(pos)
        N10X.Editor.CenterViewAtLinePos(pos[1])
    else:
        N10X.Editor.SetStatusBarText("No jump history.")