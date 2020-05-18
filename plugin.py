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
        number of maximum <voicings>. (Slash chords and omits are currently \
        unsupported.)
        """

        # db stolen from https://gist.github.com/gschoppe/9e48f9d1a9bcb72651c2e318bf45522b
        chord_lib = \
        json.load(open("{0}/chordlibrary.json".format(os.path.dirname(os.path.abspath(__file__)))))

        # silly user asks for nothing
        if voice_no == 0:
            irc.reply('error 03: Success')
            sys.exit()

        # yes this should be an array/list instead
        chord_output = chord_input
        chord_output = chord_output.capitalize()
        chord_output = chord_output.replace('minor', 'm')
        chord_output = chord_output.replace('Minor', 'm')
        chord_output = chord_output.replace('min', 'm')
        chord_output = chord_output.replace('Min', 'm')
        chord_output = chord_output.replace('-', 'm')
        chord_output = chord_output.replace('major', 'Maj')
        chord_output = chord_output.replace('Major', 'Maj')
        chord_output = chord_output.replace('maj7', 'Maj7')
        chord_output = chord_output.replace('maj9', 'Maj9')
        chord_output = chord_output.replace('maj13', 'Maj13')
        chord_output = chord_output.replace('Aug', 'aug')
        chord_output = chord_output.replace('δ', 'Maj')
        chord_output = chord_output.replace('Δ', 'Maj') # yes, it's superfluous
        chord_output = chord_output.replace('♭', "b")
        chord_output = chord_output.replace('♯', '#')

        chart_base = " 🎸"
        bullet = " \x039•\x0f "
        slinky = "\x036|\x0f"

        if voice_no is None:
            voice_no = self.registryValue("defaultVoicings") # read from config
        # someone explain to me how this works without an adjusted index
        try:
            chord_lookup = (chord_lib["EADGBE"][chord_output])
        except KeyError: # what is this chord I don't even
            irc.reply('error 02: Invalid or unsupported chord: ' + 
                        chord_input)
            sys.exit()
        for voice_index in range(0, voice_no):
            try:
                new_chart = (chord_lookup[voice_index]["p"])
            except IndexError: # ran out of voicings
                break
            # unpretty code makes pretty charts
            chart_base = chart_base + bullet + new_chart + slinky
            chart_base = chart_base.replace(',', slinky)

        chord_print = "\x036" + chord_output + chart_base
        # bemolle all teh things
        chord_print = chord_print.replace('b', "♭")
        chord_print = chord_print.replace('#', '♯')
        irc.reply(chord_print)

    chord = wrap(chord, ['somethingWithoutSpaces', optional('int')])

Class = BeestChord

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
