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
    _ = PluginInternationalization('Beestar')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x

class Beestar(callbacks.Plugin):
    """guitar chord finder"""
    threaded = True

    def chord(self, irc, msg, args, input):
        """[<chordname>]
        Displays an EADGBE guitar chord from <chordname>. (Slash chords \
        and omits are currently unsupported.)
        """
        
        chordJSON = open("{0}/chordlibrary.json".format(os.path.dirname(os.path.abspath(__file__))))
        chordLib=json.load(chordJSON)
       
        userChord = input
        userChord = userChord.replace(' ', '')
        userChord = userChord.replace('minor', 'm')
        userChord = userChord.replace('Minor', 'm')
        userChord = userChord.replace('min', 'm')
        userChord = userChord.replace('Min', 'm')
        userChord = userChord.replace('-', 'm')
        userChord = userChord.replace('major', 'Maj')
        userChord = userChord.replace('Major', 'Maj')
        userChord = userChord.replace('maj7', 'Maj7')
        userChord = userChord.replace('maj9', 'Maj9')
        userChord = userChord.replace('maj13', 'Maj13')
        userChord = userChord.replace('Δ', 'Maj')
        userChord = userChord.replace('aug', '+')
        userChord = userChord.replace('♭', "b")
        userChord = userChord.replace('♯', '#')
        try:
            chart = (chordLib["EADGBE"][userChord][0]["p"])
        except KeyError:
            irc.reply('Error 48a3e5: Invalid or unsupported chord')
            sys.exit()

        strings = chart.replace(',', '|')
        strings = "\x0303 🎸 |" + strings + "|"
        chordName = userChord
        chordName = "\x0308" + chordName                
        output = chordName + strings
        output = output.replace('b', "♭")
        output = output.replace('#', '♯')

        irc.reply(output)
    chord = wrap(chord, ['text'])

Class = Beestar

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
