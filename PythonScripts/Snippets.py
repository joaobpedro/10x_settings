#------------------------------------------------------------------------
import N10X
import time
import os

#------------------------------------------------------------------------
def IsWhitespace(c):
    return c == ' ' or c == '\r' or c == '\n' or c == '\t'

#------------------------------------------------------------------------
def IsStartOfLine(char_index, line_index):
    line = N10X.Editor.GetLine(line_index)
    for i in range(char_index):
        if not IsWhitespace(line[i]):
            return False;
    return True;

#------------------------------------------------------------------------
def GetTime():
    return int(round(time.time() * 1000))

#------------------------------------------------------------------------
sequence = "   "
key_times = [0, 0, 0]
prev_pos = (-1, -1)

#------------------------------------------------------------------------
# when typing the chars //- in sequence replace with //----------------------
# when typing the chars #-- in Python scripts replace with #----------------------
def CommentSeparatorSnippet(c):
    global sequence
    global key_times
    global prev_pos

    (x, y) = N10X.Editor.GetCursorPos()
    if prev_pos != (-1, -1) and (x - 1, y) != prev_pos:
        sequence = "   "
    prev_pos = (x, y)

    sequence = sequence[1:] + c[0]
    key_times = key_times[1:] + [GetTime()]

    filename = N10X.Editor.GetCurrentFilename()
    ext = os.path.splitext(filename)[1]

    if ext == ".py" and sequence == "#--" and GetTime() - key_times[0] < 1000 and IsStartOfLine(x - 3, y):
        N10X.Editor.InsertText("----------------------------------------------------------------------")
    elif ext != ".py" and sequence == "//-" and GetTime() - key_times[0] < 1000 and IsStartOfLine(x - 3, y):
        N10X.Editor.InsertText("-----------------------------------------------------------------------")

#------------------------------------------------------------------------
def OnCharKey(c):
    CommentSeparatorSnippet(c)

#------------------------------------------------------------------------
N10X.Editor.AddOnCharKeyFunction(OnCharKey)

