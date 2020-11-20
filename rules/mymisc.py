# These lines that start with the # are called comments. They don't affect the way the code runs.
# In this tutorial file, I put comments above the relevant lines.

# You can skip down to the next comment, for now this is not important...
from __future__ import print_function

import pprint
import re

from dragonfly import (MappingRule, BringApp, Key, Function, Grammar, Playback,
                       IntegerRef, Dictation, Choice, WaitWindow)

import subprocess
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib import virtual_desktops
import logging
import time
import json
import os
logging.getLogger("engine").setLevel(logging.DEBUG)

def take_note(textnv):
    print("note:", textnv)
    with open("//wsl$/Ubuntu-20.04/home/lahwran/notes/inbox.txt", "ab") as w:
        w.write(textnv+"\n")
    subprocess.Popen(["nircmd", "trayballoon", "New Note", textnv, "shell32.dll,22", "1500"])
    pass

def jump_to_notes():
    subprocess.call(["pycharm.cmd", "\\\\wsl$\\Ubuntu-20.04\\home\\lahwran\\notes\\", "\\\\wsl$\\Ubuntu-20.04\\home\\lahwran\\notes\\inbox.txt"])
    time.sleep(0.5)
    subprocess.call(["nircmd", "win", "activate", "stitle", "notes ["])

class MiscellaneousRule(MappingRule):

    mapping = {
        #"hotel info":                  Text("These types of hospitality industry are not cheap."),

        #'(motel | lodging)':           Playback([(["hotel", "info"], 0.0)]),

        #"open natlink folder":         BringApp("explorer", r"C:\NatLink\NatLink\MacroSystem"),

        #"remax":                       Key("a-space/10,r/10,a-space/10,x"),
        #"remax":                       Key("a-space/10,r/10,a-space/10,x"),

        #"(show | open) documentation": BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('https://dragonfly2.readthedocs.io/en/latest') + Key('enter'),

        #'reload taskbar': Function(reload),

        "(take note|techno) <textnv>":           Function(take_note),
        "bring me notes": Function(jump_to_notes),

    }




    extras = [
        #IntegerRefST("nnavi500", 1, 500),
        Dictation("textnv"),

        #Choice("capitalization", {
        #    "capitalize": 1,  # THISISATEST
        #    "camelcaps": 2,  # ThisIsATest
        #    "camelcase": 3,  # thisIsATest
        #    # "caps": 4,
        #    "laws": 5,  # thisisatest
        #    "dragon say": 6,  # this is a test
        #    "single caps": 7,  # This is a test
        #    "(dragon slip|lowercase)": 8,  # this is a test
        #    "spongebob": 9,  # this is a test
        #}),
    ]

    defaults = {
        "textnv": "",
    }


# This stuff is required too -- However you will learn more about how to change the rule types and contexts laterr
def get_rule():
    return MiscellaneousRule, RuleDetails(name="miscellaneous")
# lastupdate: 2020-11-06 23:50:50.078131
