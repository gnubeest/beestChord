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

    def chord(self, irc, msg, args, ch, vo):
        """[<chord> <voicings>]
        Displays EADGBE guitar fingerings from a <chord> in an optional
number of maximum <voicings>. (Slash chords \
        and omits are currently unsupported.)
        """

        # silly user asks for nothing
        if vo == 0:
            irc.reply('error 03: Success')
            sys.exit()

        # db stolen from https://gist.github.com/gschoppe/9e48f9d1a9bcb72651c2e318bf45522b
        chordJSON = open("{0}/chordlibrary.json".format(os.path.dirname(os.path.abspath(__file__))))
        chordLib=json.load(chordJSON)
       
        # yes this should be an array/list instead
        userChord = ch
        userChord = userChord.capitalize()
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
        userChord = userChord.replace('Aug', 'aug')
        userChord = userChord.replace('Δ', 'Maj') # doesn't work, thx python
        userChord = userChord.replace('♭', "b")
        userChord = userChord.replace('♯', '#')
      
        chart = " 🎸"
        bullet = " \x0303•\x0f "
        slinky = "\x0314|\x0f"
        
        if vo is None:
            vo = 3 # default voicings
        # someone explain to me how this works without an adjusted index
        for voiceIndex in range(0, vo):
            try:
                newChart = (chordLib["EADGBE"][userChord][voiceIndex]["p"])
            except KeyError: # what is this chord I don't even
                irc.reply('error 02: Invalid or unsupported chord')
                sys.exit()
            except IndexError: # ran out of voicings
                break
            # unpretty code makes pretty charts
            chart = chart + bullet + newChart + slinky     
        chart = chart.replace(',', slinky) + bullet
        
        output = "\x0303" + userChord + chart
        # bemolle all teh things
        output = output.replace('b', "♭")
        output = output.replace('#', '♯')
        irc.reply(output)

    chord = wrap(chord, ['somethingWithoutSpaces', optional('int')])

Class = BeestChord

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
