AlfMidi is a self-contained Python module that can translate code snippets representing musical thoughts into MIDI files.

See comments in AlfMidi.py for available methods.  There are low-level methods and higher-level methods.

## Examples

What follows are some self-contained examples.  You can cut and paste each of these
into a file then run python3 on that file.  Then import the .mid file into your DAW (digital audio workstation) app for playback.
I also show what you would see in Logic Pro X for the MIDI notes.

### Trivial - a few bass notes

<pre>
from AlfMidi import AlfMidi
m = AlfMidi()

m.t( 'bass', 'Fingered Bass' )
m.n( '[C2];::;;' )

m.write( 'bass1.mid' )
</pre>

Bob Alfieri<br>
Chapel Hill, NC
