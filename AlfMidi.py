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
    # Names are used in place of numbers in later methods.
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
        'Detuned Organ 1':	        { 'patch':  17, 'bank': 1 },
        '60\'s Organ 1':	        { 'patch':  17, 'bank': 2 },
        'Organ 4':	                { 'patch':  17, 'bank': 3 },
        'Percussive Organ':	        { 'patch':  18, 'bank': 0 },
        'Percussive B3 Organ':	        { 'patch':  18, 'bank': 0 },
        'Detuned Organ 2':	        { 'patch':  18, 'bank': 1 },
        'Organ 5':	                { 'patch':  18, 'bank': 2 },
        'Rock Organ':			{ 'patch':  19, 'bank': 0 },
        'Church Organ':                 { 'patch':  20, 'bank': 0 },
        'Church Organ 1':               { 'patch':  20, 'bank': 0 },
        'Church Organ 2':               { 'patch':  20, 'bank': 1 },
        'Church Organ 3':               { 'patch':  20, 'bank': 2 },
        'Reed Organ':			{ 'patch':  21, 'bank': 0 },
        'Puff Organ':			{ 'patch':  21, 'bank': 1 },
        'Accordion':			{ 'patch':  22, 'bank': 0 },
        'French Accordion':		{ 'patch':  22, 'bank': 0 },
        'Italian Accordion':		{ 'patch':  22, 'bank': 1 },
        'Harmonica':			{ 'patch':  23, 'bank': 0 },
        'Tango Accordion':		{ 'patch':  24, 'bank': 0 },
        'Bandoneon':		        { 'patch':  24, 'bank': 0 },

        # Guitar:
        'Nylon-String Guitar':	        { 'patch':  25, 'bank': 0 },
        'Ukulele':	                { 'patch':  25, 'bank': 1 },
        'Open Nylon Guitar':	        { 'patch':  25, 'bank': 2 },
        'Nylon Guitar 2':	        { 'patch':  25, 'bank': 3 },
        'Steel-String Guitar':          { 'patch':  26, 'bank': 0 },
        '12-String Guitar':             { 'patch':  26, 'bank': 1 },
        'Mandolin':                     { 'patch':  26, 'bank': 2 },
        'Steel + Body':                 { 'patch':  26, 'bank': 3 },
        'Jazz Guitar':                  { 'patch':  27, 'bank': 0 },
        'Hawaiian Guitar':              { 'patch':  27, 'bank': 1 },
        'Clean Electric Guitar':	{ 'patch':  28, 'bank': 0 },
        'Chorus Electric Guitar':	{ 'patch':  28, 'bank': 1 },
        'Mid Tone Guitar':	        { 'patch':  28, 'bank': 2 },
        'Muted Electric Guitar':	{ 'patch':  29, 'bank': 0 },
        'Funk Guitar':	                { 'patch':  29, 'bank': 1 },
        'Funk Guitar 2':	        { 'patch':  29, 'bank': 2 },
        'Jazz Man':	                { 'patch':  29, 'bank': 3 },
        'Overdriven Guitar':	        { 'patch':  30, 'bank': 0 },
        'Guitar Pinch':	                { 'patch':  30, 'bank': 1 },
        'Distortion Guitar':		{ 'patch':  31, 'bank': 0 },
        'Feedback Guitar':		{ 'patch':  31, 'bank': 1 },
        'Distortion Rtm Guitar':	{ 'patch':  31, 'bank': 2 },
        'Guitar Harmonics':		{ 'patch':  32, 'bank': 0 },
        'Guitar Feedback':		{ 'patch':  32, 'bank': 1 },

        # Bass:
        'Acoustic Bass':		{ 'patch':  33, 'bank': 0 },
        'Fingered Bass':	        { 'patch':  34, 'bank': 0 },
        'Finger Slap':	                { 'patch':  34, 'bank': 1 },
        'Picked Bass':		        { 'patch':  35, 'bank': 0 },
        'Fretless Bass':		{ 'patch':  36, 'bank': 0 },
        'Slap Bass 1':			{ 'patch':  37, 'bank': 0 },
        'Slap Bass 2':			{ 'patch':  38, 'bank': 0 },
        'Synth Bass 1':			{ 'patch':  39, 'bank': 0 },
        'Synth Bass 101':	        { 'patch':  39, 'bank': 1 },
        'Synth Bass 3':	                { 'patch':  39, 'bank': 2 },
        'Clavi Bass':	                { 'patch':  39, 'bank': 3 },
        'Hammer':	                { 'patch':  39, 'bank': 4 },
        'Synth Bass 2':                 { 'patch':  40, 'bank': 0 },
        'Synth Bass 4':                 { 'patch':  40, 'bank': 1 },
        'Rubber Bass':                  { 'patch':  40, 'bank': 2 },
        'Attack Pulse':                 { 'patch':  40, 'bank': 3 },

        # Strings:
        'Violin':			{ 'patch':  41, 'bank': 0 },
        'Slow Violin':			{ 'patch':  41, 'bank': 1 },
        'Viola':			{ 'patch':  42, 'bank': 0 },
        'Cello':			{ 'patch':  43, 'bank': 0 },
        'Contrabass':			{ 'patch':  44, 'bank': 0 },
        'Tremolo Strings':		{ 'patch':  45, 'bank': 0 },
        'Pizzicato Strings':		{ 'patch':  46, 'bank': 0 },
        'Harp':		                { 'patch':  47, 'bank': 0 },
        'Yang Qin':		        { 'patch':  47, 'bank': 1 },
        'Timpani':			{ 'patch':  48, 'bank': 0 },

        # Strings (continued):
        'String Ensemble':		{ 'patch':  49, 'bank': 0 },
        'Orchestra Strings':		{ 'patch':  49, 'bank': 1 },
        '60\'s Strings':		{ 'patch':  49, 'bank': 2 },
        'Slow String Ensemble':		{ 'patch':  50, 'bank': 0 },
        'Synth Strings 1':		{ 'patch':  51, 'bank': 0 },
        'Synth Strings 3':		{ 'patch':  51, 'bank': 1 },
        'Synth Strings 2':	        { 'patch':  52, 'bank': 0 },
        'Choir Aahs':                   { 'patch':  53, 'bank': 0 },
        'Choir Aahs 2':                 { 'patch':  53, 'bank': 1 },
        'Voice Oohs':			{ 'patch':  54, 'bank': 0 },
        'Humming':			{ 'patch':  54, 'bank': 1 },
        'Synth Voice':			{ 'patch':  55, 'bank': 0 },
        'Analog Voice':			{ 'patch':  55, 'bank': 1 },
        'Orchestra Hit':		{ 'patch':  56, 'bank': 0 },
        'Brass Hit':		        { 'patch':  56, 'bank': 1 },
        '6th Hit':		        { 'patch':  56, 'bank': 2 },
        'Euro Hit':		        { 'patch':  56, 'bank': 3 },

        # Brass:
        'Trumpet':			{ 'patch':  57, 'bank': 0 },
        'Dark Trumpet':			{ 'patch':  57, 'bank': 1 },
        'Trombone':			{ 'patch':  58, 'bank': 0 },
        'Trombone 2':			{ 'patch':  58, 'bank': 1 },
        'Bright Trombone':		{ 'patch':  58, 'bank': 2 },
        'Tuba':			        { 'patch':  59, 'bank': 0 },
        'Muted Trumpet':	        { 'patch':  60, 'bank': 0 },
        'Muted Trumpet 2':	        { 'patch':  60, 'bank': 1 },
        'French Horns':			{ 'patch':  61, 'bank': 0 },
        'French Horn 2':		{ 'patch':  61, 'bank': 1 },
        'Brass Section 1':		{ 'patch':  62, 'bank': 0 },
        'Brass Section 2':		{ 'patch':  62, 'bank': 1 },
        'Synth Brass 1':		{ 'patch':  63, 'bank': 0 },
        'Synth Brass 3':		{ 'patch':  63, 'bank': 1 },
        'Analog Brass':		        { 'patch':  63, 'bank': 2 },
        'Jump Brass':		        { 'patch':  63, 'bank': 3 },
        'Synth Brass 2':	        { 'patch':  64, 'bank': 0 },
        'Synth Brass 4':	        { 'patch':  64, 'bank': 1 },
        'Analog Brass 2':	        { 'patch':  64, 'bank': 2 },

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
        'Square Lead':		        { 'patch':  81, 'bank': 0 },
        'Square Wave':		        { 'patch':  81, 'bank': 1 },
        'Sine Wave':		        { 'patch':  81, 'bank': 2 },
        'Saw Lead':	                { 'patch':  82, 'bank': 0 },
        'Saw Wave':	                { 'patch':  82, 'bank': 1 },
        'Doctor Solo':	                { 'patch':  82, 'bank': 2 },
        'Natural Lead':	                { 'patch':  82, 'bank': 3 },
        'Sequenced Saw':	        { 'patch':  82, 'bank': 4 },
        'Synth Calliope':	        { 'patch':  83, 'bank': 0 },
        'Chiffer Lead':		        { 'patch':  84, 'bank': 0 },
        'Charang':		        { 'patch':  85, 'bank': 0 },
        'Wire Lead':		        { 'patch':  85, 'bank': 1 },
        'Solo Synth Vox':		{ 'patch':  86, 'bank': 0 },
        '5th Saw Wave':		        { 'patch':  87, 'bank': 0 },
        'Bass & Lead':		        { 'patch':  88, 'bank': 0 },
        'Delayed Lead':		        { 'patch':  88, 'bank': 1 },

        # Synth Pad:
        'Fantasia Pad':		        { 'patch':  89, 'bank': 0 },
        'Warm Pad':			{ 'patch':  90, 'bank': 0 },
        'Sine Pad':			{ 'patch':  90, 'bank': 1 },
        'Polysynth Pad':		{ 'patch':  91, 'bank': 0 },
        'Space Voice Pad':		{ 'patch':  92, 'bank': 0 },
        'Itopia':		        { 'patch':  92, 'bank': 1 },
        'Bowed Glass Pad':		{ 'patch':  93, 'bank': 0 },
        'Metal Pad':		        { 'patch':  94, 'bank': 0 },
        'Halo Pad':			{ 'patch':  95, 'bank': 0 },
        'Sweep Pad':		        { 'patch':  96, 'bank': 0 },

        # Synth Effects:
        'Ice Rain':			{ 'patch':  97, 'bank': 0 },
        'Soundtrack':		        { 'patch':  98, 'bank': 0 },
        'Crystal':		        { 'patch':  99, 'bank': 0 },
        'Synth Mallet':		        { 'patch':  99, 'bank': 1 },
        'Atmosphere':		        { 'patch': 100, 'bank': 0 },
        'Brightness':		        { 'patch': 101, 'bank': 0 },
        'Goblin':		        { 'patch': 102, 'bank': 0 },
        'Echo Drops':		        { 'patch': 103, 'bank': 0 },
        'Echo Bell':		        { 'patch': 103, 'bank': 1 },
        'Echo Pan':		        { 'patch': 103, 'bank': 2 },
        'Star Theme':		        { 'patch': 104, 'bank': 0 },

        # Ethnic:
        'Sitar':			{ 'patch': 105, 'bank': 0 },
        'Sitar 2':			{ 'patch': 105, 'bank': 1 },
        'Banjo':			{ 'patch': 106, 'bank': 0 },
        'Shamisen':			{ 'patch': 107, 'bank': 0 },
        'Koto':			        { 'patch': 108, 'bank': 0 },
        'Taisho Koto':			{ 'patch': 108, 'bank': 1 },
        'Kalimba':			{ 'patch': 109, 'bank': 0 },
        'Bagpipe':			{ 'patch': 110, 'bank': 0 },
        'Fiddle':			{ 'patch': 111, 'bank': 0 },
        'Shanai':			{ 'patch': 112, 'bank': 0 },

        # Percussive:
        'Tinkle Bell':			{ 'patch': 113, 'bank': 0 },
        'Agogo':			{ 'patch': 114, 'bank': 0 },
        'Steel Drums':			{ 'patch': 115, 'bank': 0 },
        'Woodblock':			{ 'patch': 116, 'bank': 0 },
        'Taiko':			{ 'patch': 117, 'bank': 0 },
        'Concert Bass Drum':		{ 'patch': 117, 'bank': 1 },
        'Melodic Tom 1':		{ 'patch': 118, 'bank': 0 },
        'Melodic Tom 2':		{ 'patch': 118, 'bank': 1 },
        'Synth Drum':			{ 'patch': 119, 'bank': 0 },
        '808 Tom':			{ 'patch': 119, 'bank': 1 },
        'Electric Percussion':		{ 'patch': 119, 'bank': 2 },

        # Sound effects:
        'Reverse Cymbal':		{ 'patch': 120, 'bank': 0 },
        'Guitar Fret Noise':		{ 'patch': 121, 'bank': 0 },
        'Guitar Cut Noise':		{ 'patch': 121, 'bank': 1 },
        'String Slap':		        { 'patch': 121, 'bank': 2 },
        'Breath Noise':			{ 'patch': 122, 'bank': 0 },
        'Flute Key Click':		{ 'patch': 122, 'bank': 1 },
        'Seashore':			{ 'patch': 123, 'bank': 0 },
        'Rain':			        { 'patch': 123, 'bank': 1 },
        'Thunder':		        { 'patch': 123, 'bank': 2 },
        'Wind':		                { 'patch': 123, 'bank': 3 },
        'Stream':		        { 'patch': 123, 'bank': 4 },
        'Bubble':		        { 'patch': 123, 'bank': 5 },
        'Bird':			        { 'patch': 124, 'bank': 0 },
        'Dog':			        { 'patch': 124, 'bank': 1 },
        'Horse-Gallup':		        { 'patch': 124, 'bank': 2 },
        'Bird 2':		        { 'patch': 124, 'bank': 3 },
        'Telephone 1':		        { 'patch': 125, 'bank': 0 },
        'Telephone 2':		        { 'patch': 125, 'bank': 1 },
        'Door Creaking':	        { 'patch': 125, 'bank': 2 },
        'Door Closing':	                { 'patch': 125, 'bank': 3 },
        'Scratch':	                { 'patch': 125, 'bank': 4 },
        'Wind Chimes':	                { 'patch': 125, 'bank': 5 },
        'Helicopter':			{ 'patch': 126, 'bank': 0 },
        'Car-Engine':			{ 'patch': 126, 'bank': 1 },
        'Car-Stop':			{ 'patch': 126, 'bank': 2 },
        'Car-Pass':			{ 'patch': 126, 'bank': 3 },
        'Car-Crash':			{ 'patch': 126, 'bank': 4 },
        'Siren':			{ 'patch': 126, 'bank': 5 },
        'Train':			{ 'patch': 126, 'bank': 6 },
        'Jetplane':			{ 'patch': 126, 'bank': 7 },
        'Starship':			{ 'patch': 126, 'bank': 8 },
        'Burst Noise':			{ 'patch': 126, 'bank': 9 },
        'Applause':			{ 'patch': 127, 'bank': 0 },
        'Laughing':			{ 'patch': 127, 'bank': 1 },
        'Screaming':			{ 'patch': 127, 'bank': 2 },
        'Punch':			{ 'patch': 127, 'bank': 3 },
        'Heart Beat':			{ 'patch': 127, 'bank': 4 },
        'Footsteps':			{ 'patch': 127, 'bank': 5 },
        'Gun Shot':			{ 'patch': 128, 'bank': 0 },
        'Machine Gun':			{ 'patch': 128, 'bank': 1 },
        'Lasergun':			{ 'patch': 128, 'bank': 2 },
        'Explosion':			{ 'patch': 128, 'bank': 2 },
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

    # TODO: lots more methods to lay down notes

    # write buffer to <prefix>.mid file
    #
    def write( self, prefix ):
        pass
        
