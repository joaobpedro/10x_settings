import N10X
import re

def ToggleCheckbox():
    """
    Adds [ ] if none exists.
    Changes [ ] to [x] if complete.
    Changes [x] to [ ] if imcomplete.
    """
    line_index = N10X.Editor.GetCursorPos()[1]
    line_text = N10X.Editor.GetLine(line_index)
    
    # Patterns
    is_empty_check = re.match(r"^(\s*)-\s\[\s\]\s(.*)", line_text)
    is_full_check = re.match(r"^(\s*)-\s\[x\]\s(.*)", line_text)
    is_bullet = re.match(r"^(\s*)-\s(.*)", line_text)

    if is_empty_check:
        # Mark Complete
        new_line = line_text.replace("[ ]", "[x]", 1)
    elif is_full_check:
        # Mark Incomplete
        new_line = line_text.replace("[x]", "[ ]", 1)
    elif is_bullet:
        # Convert bullet to checkbox
        new_line = line_text.replace("- ", "- [ ] ", 1)
    else:
        # Add checkbox to plain text
        # Finding leading whitespace to preserve indentation
        whitespace = re.match(r"^\s*", line_text).group(0)
        content = line_text.lstrip()
        new_line = f"{whitespace}- [ ] {content}"

    N10X.Editor.SetLine(line_index, new_line)

def RemoveCheckbox():
    """
    Removes any markdown checkbox or bullet from the start of the line.
    """
    line_index = N10X.Editor.GetCursorPos()[1]
    line_text = N10X.Editor.GetLine(line_index)
    
    # Regex to strip '- [ ] ', '- [x] ', or just '- ' while keeping indentation
    new_line = re.sub(r"^(\s*)-\s(\[[\sx]\]\s)?", r"\1", line_text)
    
    N10X.Editor.SetLine(line_index, new_line)