from __future__ import print_function

import datetime

from castervoice.lib.merge.state.short import R

import pprint
import re

from dragonfly import (MappingRule, BringApp, Key, Function, Grammar, Playback,
                       IntegerRef, Dictation, Choice, WaitWindow)

import subprocess
from castervoice.lib.ctrl.rule_details import RuleDetails
from castervoice.lib.actions import Key, Text, Mouse
from castervoice.lib.merge.additions import IntegerRefST
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib import virtual_desktops
import logging
import time
import json
import os
logging.getLogger("engine").setLevel(logging.DEBUG)

def note_path(filename):
    fullpath = os.path.join("//wsl$/Ubuntu-20.04/home/lahwran/notes", filename)
    directory = os.path.dirname(fullpath)
    try:
        os.makedirs(directory)
    except OSError:
        pass
    with open(fullpath, "ab") as w:
        w.write("")
    return fullpath

def generic_take_note(filename, textnv):
    print("note:", textnv)
    fullpath = note_path(filename)
    with open(fullpath, "ab") as w:
        w.write(textnv+"\n")
    subprocess.Popen(["nircmd", "trayballoon", "New Note %s" %filename, textnv, "shell32.dll,22", "1500"])
    subprocess.Popen(["powershell", "-c", "(New-Object Media.SoundPlayer \"C:\\Windows\\Media\\notify.wav\").PlaySync();"])

def take_note(textnv):
    generic_take_note("inbox.txt", textnv)

def take_note_daily(textnv):
    generic_take_note(formatted_date(), textnv)


def formatted_date():
    return datetime.datetime.now().strftime("/daily-%Y/%m%B-%d%a.txt")


def generic_jump_to_notes(filename):
    fullpath = note_path(filename)
    subprocess.call(["pycharm.cmd", "\\\\wsl$\\Ubuntu-20.04\\home\\lahwran\\notes\\", fullpath.replace("/","\\")])
    time.sleep(0.5)
    subprocess.call(["nircmd", "win", "activate", "stitle", "notes ["])

def jump_to_notes():
    generic_jump_to_notes("inbox.txt")

def jump_to_notes_daily():
    generic_jump_to_notes(formatted_date())

def stop_grid():
    subprocess.call(["taskkill", "/F", "/IM", "GridOverlay.exe", "/T"])

def start_grid():
    subprocess.Popen(["C:/Users/Lauren/RiderProjects/GameOverlay.Net/source/Examples/bin/Release/GridOverlay.exe"], )

class MiscellaneousRule(MappingRule):

    mapping = {
        "grid overlay close":
            R(Function(stop_grid)),
        "grid overlay open":
            R(Function(start_grid)),
        #"hotel info":                  Text("These types of hospitality industry are not cheap."),

        #'(motel | lodging)':           Playback([(["hotel", "info"], 0.0)]),

        #"open natlink folder":         BringApp("explorer", r"C:\NatLink\NatLink\MacroSystem"),

        #"remax":                       Key("a-space/10,r/10,a-space/10,x"),
        #"remax":                       Key("a-space/10,r/10,a-space/10,x"),

        #"(show | open) documentation": BringApp('C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe') + WaitWindow(executable="chrome.exe") + Key('c-t') + WaitWindow(title="New Tab") + Text('https://dragonfly2.readthedocs.io/en/latest') + Key('enter'),

        #'reload taskbar': Function(reload),

        "(take note|techno) <textnv>":           Function(take_note),
        "bring me notes": Function(jump_to_notes),
        "daily note <textnv>": Function(take_note_daily),
        "bring me daily notes": Function(jump_to_notes_daily),

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
