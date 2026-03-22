import N10X

def FormatMarkdownTables():
    # Get the current filename to check extension
    filename = N10X.Editor.GetCurrentFilename()
    if not filename or not filename.lower().endswith((".md", ".markdown")):
        return

    # Use GetFileText/SetFileText as per 10x Documentation
    text = N10X.Editor.GetFileText()
    if not text:
        return

    lines = text.splitlines()
    formatted_lines = []
    i = 0

    while i < len(lines):
        line_strip = lines[i].strip()
        # Basic check for a markdown table line
        if line_strip.startswith('|') and line_strip.endswith('|') and len(line) > 1 :
            table_rows = []
            # Gather all consecutive table lines
            while i < len(lines) and lines[i].strip().startswith('|'):
                raw_cells = lines[i].split('|')
                # 10x split will have empty strings at index 0 and -1 due to leading/trailing pipes
                cells = [c.strip() for c in raw_cells[1:-1]]
                table_rows.append(cells)
                i += 1
            
            if not table_rows:
                continue

            # Calculate column widths
            num_cols = max(len(row) for row in table_rows)
            widths = [0] * num_cols
            for row in table_rows:
                for idx, cell in enumerate(row):
                    if idx < num_cols:
                        widths[idx] = max(widths[idx], len(cell))

            # Build the aligned table
            for row in table_rows:
                # Detect if it's a separator line (contains only -, :, and space)
                is_sep = all(all(c in '-: ' for c in cell) for cell in row)
                
                formatted_row = "|"
                for idx in range(num_cols):
                    val = row[idx] if idx < len(row) else ""
                    if is_sep:
                        # Standardize separator to match width
                        formatted_row += "-" * (widths[idx] + 2) + "|"
                    else:
                        formatted_row += f" {val.ljust(widths[idx])} |"
                formatted_lines.append(formatted_row)
        else:
            formatted_lines.append(lines[i])
            i += 1

    new_text = "\n".join(formatted_lines)

    if new_text != text:
        # 10x API uses BeginTextUpdate/EndTextUpdate for performance
        N10X.Editor.BeginTextUpdate()
        N10X.Editor.SetFileText(new_text)
        N10X.Editor.EndTextUpdate()
        N10X.Editor.LogTo10XOutput("Markdown tables formatted.")

# To make it run automatically on save, use AddPreFileSaveFunction
def OnPreSave(filename):
    FormatMarkdownTables()

# Register the callback
# N10X.AddPreFileSaveFunction(OnPreSave)
N10X.Editor.AddPreFileSaveFunction(OnPreSave)
# Also expose it as a command you can run via Ctrl+Shift+X
# Just defining the function at top level makes it a command in 10x