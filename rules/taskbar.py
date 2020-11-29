# These lines that start with the # are called comments. They don't affect the way the code runs.
# In this tutorial file, I put comments above the relevant lines.

# You can skip down to the next comment, for now this is not important...
from __future__ import print_function

import pprint
import re

from dragonfly import (MappingRule, BringApp, Key, Function, Grammar, Playback,
                       IntegerRef, Dictation, Choice, WaitWindow)

from castervoice.lib.ctrl.rule_details import RuleDetails
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib import virtual_desktops
import logging
import time
import json
import os
import subprocess
logging.getLogger("engine").setLevel(logging.DEBUG)


def focus_action(name):
    print("create action to focus to :", name)
    def inner():
        lookup_args = load_context()["bindings"].get(name)
        if not lookup_args:
            print("missing binding for name", name)
            return
        command = ["nircmd", "win", "focus"] + lookup_args

        print("trigger action :", command)
        subprocess.call(command)
        command = ["nircmd", "win", "activate"] + lookup_args
        print("trigger action :", command)
        subprocess.call(command)

        command = ["nircmd", "win", "focus"] + lookup_args
        print("trigger action :", command)
        subprocess.call(command)
    return Function(inner)

def load_context():
    current_desktop = virtual_desktops.get_current_desktop()
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "context_%s.json" % current_desktop)
    print("filename:", filename)
    try:
        with open(filename) as r:
            contextstr = r.read()
    except:
        import traceback
        traceback.print_exc()
        contextstr = "{}"
    context = json.loads(contextstr)
    return context

context = load_context()

def get_context(force=False):
    global context
    import requests

    if  force:
        print("start request...")
        starttime = time.time()
        context = requests.get("http://localhost:9559/overview").json()
        endtime = time.time()
        print("end request: %s" % (starttime-endtime,))
    return context

def reload():
    with open("C:\Users\Lauren\PycharmProjects\py_inspect\update.trigger", "w") as w:
        w.write(str(time.time()))



def info():
    context = get_context()
    print("context", context)
    bindings = {"focus "+key: focus_action(key) for key in context["relevant"]+context["extra"] if "natlink" not in key}

    return bindings

number_names = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen".split()

class Taskbar(MappingRule):

    mapping = {
    #"hotel info":                  Text("These types of hospitality industry are not cheap."),

    #'(motel | lodging)':           Playback([(["hotel", "info"], 0.0)]),

    #"open natlink folder":         BringApp("explorer", r"C:\NatLink\NatLink\MacroSystem"),

    #"remax":                       Key("a-space/10,r/10,a-space/10,x"),
    #"remax":                       Key("a-space/10,r/10,a-space/10,x"),

    #"(show | open) documentation": BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('https://dragonfly2.readthedocs.io/en/latest') + Key('enter'),

    'reload taskbar': Function(reload),

    #"i choose <choice>":           Text("%(choice)s"),

    }
    mapping.update(info())




extras = [
    IntegerRefST("nnavi500", 1, 500),
    Dictation("textnv"),

    Choice("capitalization", {
        "capitalize": 1,  # THISISATEST
        "camelcaps": 2,  # ThisIsATest
        "camelcase": 3,  # thisIsATest
        # "caps": 4,
        "laws": 5,  # thisisatest
        "dragon say": 6,  # this is a test
        "single caps": 7,  # This is a test
        "(dragon slip|lowercase)": 8,  # this is a test
        "spongebob": 9,  # this is a test
    }),
]

defaults = {
    "nnavi500": 1,
    "nnavi50": 1,
    "nnavi10": 1,
    "nnavi3": 1,
    "textnv": "",
    "capitalization": 0,
    "spacing": 0,
    "mtn_mode": None,
    "mtn_dir": "right",
    "extreme": None,
    "big": False,
    "splatdir": "backspace",
    "modifier": "",
}


# This stuff is required too -- However you will learn more about how to change the rule types and contexts laterr
def get_rule():
    return Taskbar, RuleDetails(name="taskbar")
# lastupdate: 2020-11-20 23:12:46.798288
