import math
import subprocess
import time
from dragonfly import Function, Choice, MappingRule
from castervoice.lib.const import CCRType
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib import control, navigation
from castervoice.lib.actions import Mouse
from castervoice.lib.ctrl.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRef
from castervoice.lib.merge.state.short import R
from castervoice.rules.ccr.standard import SymbolSpecs


# Perform an action based on the passed in action number
# action - optional mouse action after movement
def perform_mouse_action(action):
    if action == 1:
        Mouse("left").execute()
    if action == 2:
        Mouse("left:2").execute()
    elif action == 3:
        Mouse("right").execute()

def win32_get():
    '''
    Get the primary windows display width and height
    '''
    import ctypes
    user32 = ctypes.windll.user32
    screensize = (
        user32.GetSystemMetrics(0),
        user32.GetSystemMetrics(1),
    )
    return screensize

def get_mouse_pos(xmajor, ymajor, minor):
    print("locals:", locals())
    screenWidth, screenHeight = win32_get()
    cellSize = 16
    cellCount = 4
    cellWidth  = cellSize * cellCount
    cellHeight = cellSize * cellCount
    grid_columns = math.ceil(screenWidth / cellWidth)
    grid_rows = math.ceil(screenHeight / cellHeight)
    xmajor = int(xmajor)
    ymajor = int(ymajor)
    if minor is not None:
        minor = int(minor)
        yminor = int(minor / cellCount)+0.5
        xminor = int(minor % cellCount)+0.5
    else:
        yminor = 2
        xminor = 2
    x = int(((xmajor * cellCount) + (xminor)) *cellSize)
    y = int(((ymajor * cellCount) + (yminor)) *cellSize)
    print("locals:", locals())
    return (x, y)

# Command to move the mouse
# n - square to move to]
# s - optional inner square to move to
# action - optional mouse action after movement
def move_mouse(xn, yn, hexdigit):
    x, y = get_mouse_pos(xn, yn, hexdigit)
    Mouse("[{}, {}]".format(x, y)).execute()
    #perform_mouse_action(int(action))


# Command to drag the mouse from the current position
# n0 - optional square to drag from
# s0 - optional inner square to drag from
# n  - square to drag to
# s  - optional inner square to drag to
# action - optional mouse action after movement
def drag_mouse(xn, yn, hexdigit):
    Mouse("left:down/10").execute()
    time.sleep(0.3)
    # Hold down click, move to drag destination, and release click
    x, y = get_mouse_pos(xn, yn, hexdigit)
    Mouse("[{}, {}]".format(x, y)).execute()
    time.sleep(0.3)
    Mouse("left:up/30").execute()
    #perform_mouse_action(int(action))



def stop_grid():
    subprocess.call(["taskkill", "/F", "/IM", "GridOverlay.exe", "/T"])





class SudokuGridRule(MergeRule):
    '''
    Rules for sudoku grid. We can either move the mouse or drag it.
    The number n is one of the numbered squares.
    The grid portion is a number from 1-9 referencing an inner unnumbered square.
    '''
    pronunciation = "sudoku grid"

    mapping = {
        "curse <xn> by <yn> [grid <hexdigit>]":
            R(Function(move_mouse)),

        "drag <xn> by <yn> [grid <hexdigit>]":
            R(Function(drag_mouse)),
        "stop grid overlay":
            R(Function(stop_grid)),
    }
    extras = [
        IntegerRef("yn", -1, 100),
        IntegerRef("xn", -1, 100),
        IntegerRef("sn", 0, 10),
        Choice("hexdigit", {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "arch": 10,
            "brov": 11,
            "char": 12,
            "delta": 13,
            "echo": 14,
            "foxy": 15,
        }),
        Choice("action", {
            "move": 0,
            "kick": 1,
            "kick (double | 2)": 2,
            "psychic": 3,
        }),
    ]
    defaults = {
        "xn": 0,
        "yn": 0,
        "hexdigit": None,
        "action": 0,
    }


def get_rule():
    Details = RuleDetails(ccrtype=CCRType.GLOBAL)
    return SudokuGridRule, Details
