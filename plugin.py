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

import json
import requests

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
        """[<Root_QualityTensionBass>]
        Shows standard tuning guitar chords from <Root_QualityTensionBass>.
        """

        input = input.replace(" ", "")
        input = input.replace("(", "")
        input = input.replace(")", "")
        uber = requests.get('https://api.uberchord.com/v1/chords/' + input)

        chart = json.loads(uber.text)[0]
        strings = chart["strings"]
        name = chart["chordName"].replace(',', "")
        enharm = chart["enharmonicChordName"]
        tones = chart["tones"]
        strings = "\x0303" + strings
        name = "\x0308" + name
        tones = "\x0308" + tones
                
        output = name + "  " + strings + "  " + tones
        output = output.replace('b', "♭")
        output = output.replace('#', '♯')

        irc.reply(output)
    chord = wrap(chord, ['text'])

Class = Beestar

# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
