###
# Copyright (c) 2020, Brian McCord
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import sys
import os
import json

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('BeestChord')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class BeestChord(callbacks.Plugin):
    """guitar chord finder"""
    threaded = True

    def chord(self, irc, msg, args, chord_input, voice_no):
        """[<chord> <voicings>]
        Displays EADGBE guitar fingerings from a <chord> in an optional \
        number of maximum <voicings>."""

# open json library
        chord_lib = \
        json.load(open("{0}/guitar.json".format(os.path.dirname(os.path.abspath(__file__)))))

# silly user asks for nothing
        if voice_no == 0:
            irc.reply('error 03: Success')
            sys.exit()

# match weird user input with weird database
        chord_output = chord_input.capitalize()
        #chord_output = chord_output.replace('minor', 'm')
        #chord_output = chord_output.replace('min', 'm')
        chord_output = chord_output.replace('-', 'm')
        #chord_output = chord_output.replace('major', 'maj')
        chord_output = chord_output.replace('δ', 'maj')
        chord_output = chord_output.replace('♭', "b")
        chord_output = chord_output.replace('♯', '#')
        try:
            if chord_output[1] == "#" or chord_output[1] == "b":
                if chord_output[0:2] == "Db" or chord_output[0:2] == "C#":
                    chord_key = "Csharp"
                elif chord_output[0:2] == "D#" or chord_output[0:2] == "Eb":
                    chord_key = "Eb"
                elif chord_output[0:2] == "Gb" or chord_output[0:2] == "F#":
                    chord_key = "Fsharp"
                elif chord_output[0:2] == "G#" or chord_output[0:2] == "Ab":
                    chord_key = "Ab"
                elif chord_output[0:2] == "A#" or chord_output[0:2] == "Bb":
                    chord_key = "Bb"
                chord_suffix = chord_output[2:]
            else:
                chord_key = chord_output[0]
                chord_suffix = chord_output[1:]
        except IndexError:
            chord_key = chord_output[0]
            chord_suffix = chord_output[1:]
        if chord_suffix == "" or chord_suffix == "maj":
            chord_suffix = "major"
        if chord_suffix == "m" or chord_suffix == "min":
            chord_suffix = "minor"

# search for matching suffix
        chord_lookup = chord_key + chord_suffix
        for suffix_index in range(0,100):
            chart = (chord_lib['chords'][chord_key][suffix_index])
            if (chart['suffix']) == chord_suffix:
                chord_db = (chart['positions'])
                break

# build fingerings
        chart_base = " 🎸"
        bullet = " \x039•\x0f "
        slinky = "\x036|\x0f"
        if voice_no is None:
            voice_no = self.registryValue("defaultVoicings") # read from config
        for voice_index in range(0, voice_no):
            try:
                string_list = []
                voice_db = (chord_db[voice_index]['frets'])
                for string in range(0, 6):
                    if voice_db[string] == -1:
                        string_chr = "X"
                    else:
                        string_adj = (voice_db[string]) + ((
                                    chord_db[voice_index]['baseFret']) - 1)
                        string_chr = str(string_adj)
                    string_list.insert(string, string_chr)
                E_st = (string_list[0])
                A_st = (string_list[1])
                D_st = (string_list[2])
                G_st = (string_list[3])
                B_st = (string_list[4])
                EE_st = (string_list[5])
                chart_base = (chart_base + bullet + E_st + slinky + A_st +
                                slinky + D_st + slinky + G_st + slinky + B_st + 
                                slinky + EE_st + slinky)
            except IndexError:
                break

# build final output
        chord_print = chord_key + chord_suffix + chart_base
        chord_print = chord_print.replace('b', "♭")
        chord_print = chord_print.replace('#', '♯')
        irc.reply(chord_print)

    chord = wrap(chord, ['somethingWithoutSpaces', optional('int')])

Class = BeestChord

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
