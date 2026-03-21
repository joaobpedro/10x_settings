#------------------------------------------------------------------------
import uuid
import N10X

#------------------------------------------------------------------------
def SortLines():

    N10X.Editor.PushUndoGroup()

    selection_start = N10X.Editor.GetSelectionStart()
    selection_end = N10X.Editor.GetSelectionEnd()

    if selection_start != selection_end:
        start_line = min(selection_start[1], selection_end[1])
        end_line = max(selection_start[1], selection_end[1]) + 1
    else:
        start_line = 0
        end_line = N10X.Editor.GetLineCount()

    line_count = end_line - start_line

    lines = []

    for i in range(line_count):
        lines.append(N10X.Editor.GetLine(start_line + i))

    lines.sort()

    for i in range(line_count):
        N10X.Editor.SetLine(start_line + i, lines[i])

    N10X.Editor.SetSelection(selection_start, selection_end)

    N10X.Editor.PopUndoGroup()
    
#------------------------------------------------------------------------
def TrimLines():

    N10X.Editor.PushUndoGroup()
    N10X.Editor.BeginTextUpdate()

    line_count = N10X.Editor.GetLineCount()

    for i in range(line_count):
        line = N10X.Editor.GetLine(i)
        line = line.rstrip()
        N10X.Editor.SetLine(i, line)

    N10X.Editor.EndTextUpdate()
    N10X.Editor.PopUndoGroup()

#------------------------------------------------------------------------
def InsertGuid():
    N10X.Editor.InsertText(str(uuid.uuid4()).upper())

