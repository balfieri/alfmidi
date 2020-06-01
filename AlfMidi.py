# AlfMidi.py - python3 module for converting musical thoughts in the form of Python snippets into MIDI files
#
# Supported MIDI Standards:
#    - MIDI 1.0
#    - General MIDI Level 2
#
import os

P = print

# Abort with message.
#
def die( msg ):
    P( f'ERROR: {msg}' )
    sys.exit( 1 )

class AlfMidi( object ):
    # Conventional general midi instrument names and assigned patch+bank numbers.
    # Bank != 0 means level 2 instrument.
    # Names are used in place of numbers in methods below.
    # In some cases, multiple names map to the same numbers (Level 1 vs. Level 2 names, etc.).
    #
    instruments = {
        # Piano:
        'Acoustic Grand Piano':         { 'patch':   1, 'bank': 0 },
        'Wide Acoustic Grand Piano':    { 'patch':   1, 'bank': 1 },
        'Dark Acoustic Grand Piano':    { 'patch':   1, 'bank': 2 },
        'Bright Acoustic Piano':        { 'patch':   2, 'bank': 0 },
        'Wide Bright Acoustic Piano':   { 'patch':   2, 'bank': 1 },
        'Electric Grand Piano':         { 'patch':   3, 'bank': 0 },
        'Wide Electric Grand Piano':    { 'patch':   3, 'bank': 1 },
        'Honky-tonk Piano':             { 'patch':   4, 'bank': 0 },
        'Wide Honky-tonk Piano':        { 'patch':   4, 'bank': 1 },
        'Rhodes Piano':                 { 'patch':   5, 'bank': 0 },
        'Electric Piano 1':             { 'patch':   5, 'bank': 0 },
        'Detuned Electric Piano 1':     { 'patch':   5, 'bank': 1 },
        'Electric Piano 1 Variation':   { 'patch':   5, 'bank': 2 },
        '60\'s Electric Piano':         { 'patch':   5, 'bank': 3 },
        'Chorused Electric Piano':      { 'patch':   6, 'bank': 0 },
        'Electric Piano 2':             { 'patch':   6, 'bank': 0 },
        'Detuned Electric Piano 2':     { 'patch':   6, 'bank': 1 },
        'Electric Piano 2 Variation':   { 'patch':   6, 'bank': 2 },
        'Electric Piano Legend':        { 'patch':   6, 'bank': 3 },
        'Electric Piano Phase':         { 'patch':   6, 'bank': 4 },
        'Harpsichord':                  { 'patch':   7, 'bank': 0 },
        'Coupled Harpsichord':          { 'patch':   7, 'bank': 1 },
        'Wide Harpsichord':             { 'patch':   7, 'bank': 2 },
        'Open Harpsichord':             { 'patch':   7, 'bank': 3 },
        'Clavinet':                     { 'patch':   8, 'bank': 0 },
        'Pulse Clavinet':               { 'patch':   8, 'bank': 1 },

        # Chromatic Percussion:
        'Celesta':			{ 'patch':   9, 'bank': 0 },
        'Glockenspiel':			{ 'patch':  10, 'bank': 0 },
        'Music Box':			{ 'patch':  11, 'bank': 0 },
        'Vibraphone':			{ 'patch':  12, 'bank': 0 }, 
        'Wet Vibraphone':		{ 'patch':  12, 'bank': 1 }, 
        'Marimba':			{ 'patch':  13, 'bank': 0 },
        'Wide Marimba':			{ 'patch':  13, 'bank': 1 },
        'Xylophone':			{ 'patch':  14, 'bank': 0 },
        'Tubular Bell':		        { 'patch':  15, 'bank': 0 },
        'Church Bell':		        { 'patch':  15, 'bank': 1 },
        'Carillon':		        { 'patch':  15, 'bank': 2 },
        'Dulcimer':			{ 'patch':  16, 'bank': 0 },
        'Santur':			{ 'patch':  16, 'bank': 0 },

        # Organ:
        'Drawbar Organ':	        { 'patch':  17, 'bank': 0 },
        'Percussive Organ':	        { 'patch':  18, 'bank': 0 },
        'Rock Organ':			{ 'patch':  19, 'bank': 0 },
        'Church Organ':                 { 'patch':  20, 'bank': 0 },
        'Reed Organ':			{ 'patch':  21, 'bank': 0 },
        'Accordion':			{ 'patch':  22, 'bank': 0 },
        'Harmonica':			{ 'patch':  23, 'bank': 0 },
        'Tango Accordion':		{ 'patch':  24, 'bank': 0 },

        # Guitar:
        'Acoustic Guitar (nylon)':	{ 'patch':  25, 'bank': 0 },
        'Acoustic Guitar (steel)':      { 'patch':  26, 'bank': 0 },
        'Electric Guitar (jazz)':       { 'patch':  27, 'bank': 0 },
        'Electric Guitar (clean)':	{ 'patch':  28, 'bank': 0 },
        'Electric Guitar (muted)':	{ 'patch':  29, 'bank': 0 },
        'Overdriven Guitar':	        { 'patch':  30, 'bank': 0 },
        'Distortion Guitar':		{ 'patch':  31, 'bank': 0 },
        'Guitar harmonics':		{ 'patch':  32, 'bank': 0 },

        # Bass:
        'Acoustic Bass':		{ 'patch':  33, 'bank': 0 },
        'Electric Bass (finger)':	{ 'patch':  34, 'bank': 0 },
        'Electric Bass (pick)':		{ 'patch':  35, 'bank': 0 },
        'Fretless Bass':		{ 'patch':  36, 'bank': 0 },
        'Slap Bass 1':			{ 'patch':  37, 'bank': 0 },
        'Slap Bass 2':			{ 'patch':  38, 'bank': 0 },
        'Synth Bass 1':			{ 'patch':  39, 'bank': 0 },
        'Synth Bass 2':                 { 'patch':  40, 'bank': 0 },

        # Strings:
        'Violin':			{ 'patch':  41, 'bank': 0 },
        'Viola':			{ 'patch':  42, 'bank': 0 },
        'Cello':			{ 'patch':  43, 'bank': 0 },
        'Contrabass':			{ 'patch':  44, 'bank': 0 },
        'Tremolo Strings':		{ 'patch':  45, 'bank': 0 },
        'Pizzicato Strings':		{ 'patch':  46, 'bank': 0 },
        'Orchestral Harp':		{ 'patch':  47, 'bank': 0 },
        'Timpani':			{ 'patch':  48, 'bank': 0 },

        # Strings (continued):
        'String Ensemble 1':		{ 'patch':  49, 'bank': 0 },
        'String Ensemble 2':		{ 'patch':  50, 'bank': 0 },
        'Synth Strings 1':		{ 'patch':  51, 'bank': 0 },
        'Synth Strings 2':	        { 'patch':  52, 'bank': 0 },
        'Choir Aahs':                   { 'patch':  53, 'bank': 0 },
        'Voice Oohs':			{ 'patch':  54, 'bank': 0 },
        'Synth Voice':			{ 'patch':  55, 'bank': 0 },
        'Orchestra Hit':		{ 'patch':  56, 'bank': 0 },

        # Brass:
        'Trumpet':			{ 'patch':  57, 'bank': 0 },
        'Trombone':			{ 'patch':  58, 'bank': 0 },
        'Tuba':			        { 'patch':  59, 'bank': 0 },
        'Muted Trumpet':	        { 'patch':  60, 'bank': 0 },
        'French Horn':			{ 'patch':  61, 'bank': 0 },
        'Brass Section':		{ 'patch':  62, 'bank': 0 },
        'Synth Brass 1':		{ 'patch':  63, 'bank': 0 },
        'Synth Brass 2':	        { 'patch':  64, 'bank': 0 },

        # Reed:
        'Soprano Sax':			{ 'patch':  65, 'bank': 0 },
        'Alto Sax':			{ 'patch':  66, 'bank': 0 },
        'Tenor Sax':			{ 'patch':  67, 'bank': 0 },
        'Baritone Sax':			{ 'patch':  68, 'bank': 0 },
        'Oboe':			        { 'patch':  69, 'bank': 0 },
        'English Horn':			{ 'patch':  70, 'bank': 0 },
        'Bassoon':			{ 'patch':  71, 'bank': 0 },
        'Clarinet':			{ 'patch':  72, 'bank': 0 },

        # Pipe:
        'Piccolo':			{ 'patch':  73, 'bank': 0 },
        'Flute':			{ 'patch':  74, 'bank': 0 },
        'Recorder':			{ 'patch':  75, 'bank': 0 },
        'Pan Flute':			{ 'patch':  76, 'bank': 0 },
        'Blown Bottle':			{ 'patch':  77, 'bank': 0 },
        'Shakuhachi':			{ 'patch':  78, 'bank': 0 },
        'Whistle':			{ 'patch':  79, 'bank': 0 },
        'Ocarina':			{ 'patch':  80, 'bank': 0 },

        # Synth Lead:
        'Lead 1 (square)':		{ 'patch':  81, 'bank': 0 },
        'Lead 2 (sawtooth)':	        { 'patch':  82, 'bank': 0 },
        'Lead 3 (calliope)':	        { 'patch':  83, 'bank': 0 },
        'Lead 4 (chiff)':		{ 'patch':  84, 'bank': 0 },
        'Lead 5 (charang)':		{ 'patch':  85, 'bank': 0 },
        'Lead 6 (voice)':		{ 'patch':  86, 'bank': 0 },
        'Lead 7 (fifths)':		{ 'patch':  87, 'bank': 0 },
        'Lead 8 (bass + lead)':		{ 'patch':  88, 'bank': 0 },

        # Synth Pad:
        'Pad 1 (new age)':		{ 'patch':  89, 'bank': 0 },
        'Pad 2 (warm)':			{ 'patch':  90, 'bank': 0 },
        'Pad 3 (polysynth)':		{ 'patch':  91, 'bank': 0 },
        'Pad 4 (choir)':		{ 'patch':  92, 'bank': 0 },
        'Pad 5 (bowed)':		{ 'patch':  93, 'bank': 0 },
        'Pad 6 (metallic)':		{ 'patch':  94, 'bank': 0 },
        'Pad 7 (halo)':			{ 'patch':  95, 'bank': 0 },
        'Pad 8 (sweep)':		{ 'patch':  96, 'bank': 0 },

        # Synth Effects:
        'FX 1 (rain)':			{ 'patch':  97, 'bank': 0 },
        'FX 2 (soundtrack)':		{ 'patch':  98, 'bank': 0 },
        'FX 3 (crystal)':		{ 'patch':  99, 'bank': 0 },
        'FX 4 (atmosphere)':		{ 'patch': 100, 'bank': 0 },
        'FX 5 (brightness)':		{ 'patch': 101, 'bank': 0 },
        'FX 6 (goblins)':		{ 'patch': 102, 'bank': 0 },
        'FX 7 (echoes)':		{ 'patch': 103, 'bank': 0 },
        'FX 8 (sci-fi)':		{ 'patch': 104, 'bank': 0 },

        # Ethnic:
        'Sitar':			{ 'patch': 105, 'bank': 0 },
        'Banjo':			{ 'patch': 106, 'bank': 0 },
        'Shamisen':			{ 'patch': 107, 'bank': 0 },
        'Koto':			        { 'patch': 108, 'bank': 0 },
        'Kalimba':			{ 'patch': 109, 'bank': 0 },
        'Bag pipe':			{ 'patch': 110, 'bank': 0 },
        'Fiddle':			{ 'patch': 111, 'bank': 0 },
        'Shanai':			{ 'patch': 112, 'bank': 0 },

        # Percussive:
        'Tinkle Bell':			{ 'patch': 113, 'bank': 0 },
        'Agogo':			{ 'patch': 114, 'bank': 0 },
        'Steel Drums':			{ 'patch': 115, 'bank': 0 },
        'Woodblock':			{ 'patch': 116, 'bank': 0 },
        'Taiko Drum':			{ 'patch': 117, 'bank': 0 },
        'Melodic Tom':			{ 'patch': 118, 'bank': 0 },
        'Synth Drum':			{ 'patch': 119, 'bank': 0 },

        # Sound effects:
        'Reverse Cymbal':		{ 'patch': 120, 'bank': 0 },
        'Guitar Fret Noise':		{ 'patch': 121, 'bank': 0 },
        'Breath Noise':			{ 'patch': 122, 'bank': 0 },
        'Seashore':			{ 'patch': 123, 'bank': 0 },
        'Bird Tweet':			{ 'patch': 124, 'bank': 0 },
        'Telephone Ring':		{ 'patch': 125, 'bank': 0 },
        'Helicopter':			{ 'patch': 126, 'bank': 0 },
        'Applause':			{ 'patch': 127, 'bank': 0 },
        'Gunshot':			{ 'patch': 128, 'bank': 0 },
        }

    # Conventional percussion notes on MIDI channel 10 (GM2==level2).
    # 
    percussion_notes = {
        'High Q':                       27,     # GM2
        'Slap':                         28,     # GM2
        'Scratch Push':                 29,     # GM2
        'Scratch Pull':                 30,     # GM2
        'Sticks':                       31,     # GM2
        'Square Click':                 32,     # GM2
        'Metronome Click':              33,     # GM2
        'Metronome Bell':               34,     # GM2
        'Acoustic Bass Drum':		35,
        'Bass Drum 1':		        36,
        'Side Stick':		        37,
        'Acoustic Snare':		38,
        'Hand Clap':		        39,
        'Electric Snare':		40,
        'Low Floor Tom':		41,
        'Closed Hi Hat':		42,
        'High Floor Tom':		43,
        'Pedal Hi-Hat':		        44,
        'Low Tom':		        45,
        'Open Hi-Hat':		        46,
        'Low-Mid Tom':		        47,
        'Hi-Mid Tom':		        48,
        'Crash Cymbal 1':		49,
        'High Tom':		        50,
        'Ride Cymbal 1':		51,
        'Chinese Cymbal':		52,
        'Ride Bell':		        53,
        'Tambourine':		        54,
        'Splash Cymbal':		55,
        'Cowbell':		        56,
        'Crash Cymbal 2':		57,
        'Vibraslap':		        58,
        'Ride Cymbal 2':		59,
        'Hi Bongo':		        60,
        'Low Bongo':		        61,
        'Mute Hi Conga':		62,
        'Open Hi Conga':		63,
        'Low Conga':		        64,
        'High Timbale':		        65,
        'Low Timbale':		        66,
        'High Agogo':		        67,
        'Low Agogo':		        68,
        'Cabasa':		        69,
        'Maracas':		        70,
        'Short Whistle':		71,
        'Long Whistle':		        72,
        'Short Guiro':		        73,
        'Long Guiro':		        74,
        'Claves':		        75,
        'Hi Wood Block':		76,
        'Low Wood Block':		77,
        'Mute Cuica':		        78,
        'Open Cuica':		        79,
        'Mute Triangle':		80,
        'Open Triangle':		81,
        'Shaker':                       82,     # GM2
        'Jingle Bell':                  83,     # GM2
        'Belltree':                     84,     # GM2
        'Castanets':                    85,     # GM2
        'Mute Surdo':                   86,     # GM2
        'Open Surdo':                   87,     # GM2
        }

    # constructor
    #
    def __init__( self ):
        # per-instance variables
        #
        self.time_sig = '4/4'   # time signature
        self.clocks_per_mtick = 24
        self.crotchets_per_32nd_note = 8
        self.tracks = {}        # track names to MIDI instrument numbers
        self.BA = 0             # current bar
        self.TR = 1             # current track_number
        self.CH = 1             # current channel_number within track
        self.buff = []          # music buffer

    # change time signature, etc.
    #
    def time( self, time_sig, clocks_per_mtick, crotchets_per_32nd_note ):
        self.time_sig = time_sig
        self.clocks_per_mtick = clocks_per_mtick
        self.crotchets_per_32nd_note = crotchets_per_32nd_note

    # track and channel meta data
    #
    def track( name, midi_instrument ): 
        if not midi_instrument in instruments: die( f'no MIDI instrument called {midi_instrument}' )
        tracks[name] = instruments[midi_instrument]

    # write buffer to <prefix>.mid file
    #
    def write( self, prefix ):
        # 
