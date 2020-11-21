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


def focus_action(title):
    print("create action to focus to :", title)
    def inner():
        command = ["nircmd", "win", "activate", "stitle", title["name"].rpartition(" -")[0][:30]]
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


class rp(object):
    def __init__(self, pattern, replacement, offset=1, final=False, cost=None):
        self.pattern = pattern
        self.replacement = replacement
        self.offset = offset
        if cost is not None:
            self.cost = cost
        elif final:
            self.cost = lambda m: len(m)*10
        else:
            self.cost = lambda m: len(m)
        self.final = final

replacements = [
    rp(r"^.*terminus[^/\\]*$", r"terminus", final=True),
    rp(r"^.*pycharm[^/\\]*$", r"pycharm", final=True),
    rp(r"^.*clion[^/\\]*$", r"sea lion", final=True),
    rp(r"^MINGW.*", r"min (gee double you|goof whiskey) ", final=True),
    rp(r"^.*VCV\\Rack\\Rack[^/\\]*$", r"(vcv rack|rack|vcv)", final=True),
    rp(r" ?-? ?[0-9]+ running windows? *", r"", offset=1),
    rp(r"^(?:[a-zA-Z]:|[{]).*[/\\]([^/\\]*)(?:.exe)$", r"\1", offset=1),
    rp(r"^cmd$", r"command prompt", final=True),
    rp(r"[-/:_]", r" ", offset=1, cost=lambda m: len(m) * 10),
    rp(r"py ", r"pie ", offset=1),
    rp(r"[^a-zA-Z' ].*", r"", offset=3),
    rp(r"^ *((?:[a-zA-Z']+ ){4}).*$", r"\1", offset=1),
    rp(r"^ *((?:[a-zA-Z']+ ){3}).*$", r"\1", offset=1),
    rp(r"^ *((?:[a-zA-Z']+ ){2}).*$", r"\1", offset=1),
    rp(r"^ *((?:[a-zA-Z']+ ){1).*$", r"\1", offset=1),
    rp(r" [^ ]+$", r"", offset=1),
    rp(r"^.{30,}$", None, cost=lambda m: sum(len(x) for x in m))
]
targets = set(x.replacement.strip() for x in replacements if x.replacement)

def rating(x):
    cost = 0
    debug = True

    for r in replacements:
        matches = re.findall(r.pattern, x)
        if not matches:
            continue
        #print("matches:", matches)

        cost += r.cost(matches)
    return cost
def extract(x):
    results  = [x]
    for r in replacements:
        if r.replacement is None:
            continue
        for previous in set(results[-r.offset:]):
            a = re.sub(r.pattern,r.replacement,previous)
            if r.final and re.match(r.pattern,previous):
                return [a]
            if a:
                results.append(a.strip())
    #print(results)
    rated = sorted([(rating(a), a) for a in set(results)])
    #pprint.pprint(rated)
    return [" ".join(y.split()) for cost, y in rated if cost <10]

def info():
    context = get_context()
    by_automation_id = {}
    taken = set()
    for task in context["taskbar"]:
        index,this_program = by_automation_id.setdefault(task["automation_id"],(len(by_automation_id)+1, []))
        updated = {}
        updated.update(task)
        program_words = extract(task["automation_id"].encode(encoding='ascii', errors="replace"))
        window_words = extract(task["name"].encode(encoding='ascii', errors="replace"))
        updated.update({
            "program_words": program_words,
            "window_words": window_words

        })
        this_program.append(updated)
    bindings = {}
    template = "focus %s"
    num_template = "focus %s %s"
    for index, tasks in sorted(by_automation_id.values()):
        for taskindex, task in enumerate(tasks):
            action = focus_action(task)
            if taskindex > 0 and taskindex < len(number_names):
                for word in task["program_words"]:
                    bindings.setdefault(num_template%(word.lower(), number_names[taskindex]),action)
            if taskindex == 0:
                for word in task["program_words"]:
                    bindings.setdefault(template%word.lower(), action)
            for word in task["window_words"]:
                bindings.setdefault(template%word.lower(),action)
    pprint.pprint(bindings)
    #print(json.dumps(sorted(by_automation_id.values()), indent=4))

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
