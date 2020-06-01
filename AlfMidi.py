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
        'Gunshot':			{ 'patch': 128, 'bank': 0 },
        'Machine Gun':			{ 'patch': 128, 'bank': 1 },
        'Lasergun':			{ 'patch': 128, 'bank': 2 },
        'Explosion':			{ 'patch': 128, 'bank': 2 },
        }

    # Conventional non-percussion notes 
    # 
    BASE = 20  # MIDI base note number for A0
    notes = {
        'A0':                           BASE+1,
        'A#0':                          BASE+2,
        'Bb0':                          BASE+2,
        'B0':                           BASE+3,

        'C1':                           BASE+4,
        'C#1':                          BASE+5,
        'Db1':                          BASE+5,
        'D1':                           BASE+6,
        'D#1':                          BASE+7,
        'Eb1':                          BASE+7,
        'E1':                           BASE+8,
        'F1':                           BASE+9,
        'F#1':                          BASE+10,
        'Gb1':                          BASE+10,
        'G1':                           BASE+11,
        'G#1':                          BASE+12,
        'Ab1':                          BASE+12,
        'A1':                           BASE+13,
        'A#1':                          BASE+14,
        'Bb1':                          BASE+14,
        'B1':                           BASE+15,

        'C2':                           BASE+16,
        'C#2':                          BASE+17,
        'Db2':                          BASE+17,
        'D2':                           BASE+18,
        'D#2':                          BASE+19,
        'Eb2':                          BASE+19,
        'E2':                           BASE+20,
        'F2':                           BASE+21,
        'F#2':                          BASE+22,
        'Gb2':                          BASE+22,
        'G2':                           BASE+23,
        'G#2':                          BASE+24,
        'Ab2':                          BASE+24,
        'A2':                           BASE+25,
        'A#2':                          BASE+26,
        'Bb2':                          BASE+26,
        'B2':                           BASE+27,

        'C3':                           BASE+28,
        'C#3':                          BASE+29,
        'Db3':                          BASE+29,
        'D3':                           BASE+30,
        'D#3':                          BASE+31,
        'Eb3':                          BASE+31,
        'E3':                           BASE+32,
        'F3':                           BASE+33,
        'F#3':                          BASE+34,
        'Gb3':                          BASE+34,
        'G3':                           BASE+35,
        'G#3':                          BASE+36,
        'Ab3':                          BASE+36,
        'A3':                           BASE+37,
        'A#3':                          BASE+38,
        'Bb3':                          BASE+38,
        'B3':                           BASE+39,

        'C4':                           BASE+40,
        'C#4':                          BASE+41,
        'Db4':                          BASE+41,
        'D4':                           BASE+42,
        'D#4':                          BASE+43,
        'Eb4':                          BASE+43,
        'E4':                           BASE+44,
        'F4':                           BASE+45,
        'F#4':                          BASE+46,
        'Gb4':                          BASE+46,
        'G4':                           BASE+47,
        'G#4':                          BASE+48,
        'Ab4':                          BASE+48,
        'A4':                           BASE+49,
        'A#4':                          BASE+50,
        'Bb4':                          BASE+50,
        'B4':                           BASE+51,

        'C5':                           BASE+52,
        'C#5':                          BASE+53,
        'Db5':                          BASE+53,
        'D5':                           BASE+54,
        'D#5':                          BASE+55,
        'Eb5':                          BASE+55,
        'E5':                           BASE+56,
        'F5':                           BASE+57,
        'F#5':                          BASE+58,
        'Gb5':                          BASE+58,
        'G5':                           BASE+59,
        'G#5':                          BASE+60,
        'Ab5':                          BASE+60,
        'A5':                           BASE+61,
        'A#5':                          BASE+62,
        'Bb5':                          BASE+62,
        'B5':                           BASE+63,

        'C6':                           BASE+64,
        'C#6':                          BASE+65,
        'Db6':                          BASE+65,
        'D6':                           BASE+66,
        'D#6':                          BASE+67,
        'Eb6':                          BASE+67,
        'E6':                           BASE+68,
        'F6':                           BASE+69,
        'F#6':                          BASE+70,
        'Gb6':                          BASE+70,
        'G6':                           BASE+71,
        'G#6':                          BASE+72,
        'Ab6':                          BASE+72,
        'A6':                           BASE+73,
        'A#6':                          BASE+74,
        'Bb6':                          BASE+74,
        'B6':                           BASE+75,

        'C7':                           BASE+76,
        'C#7':                          BASE+77,
        'Db7':                          BASE+77,
        'D7':                           BASE+78,
        'D#7':                          BASE+79,
        'Eb7':                          BASE+79,
        'E7':                           BASE+80,
        'F7':                           BASE+81,
        'F#7':                          BASE+82,
        'Gb7':                          BASE+82,
        'G7':                           BASE+83,
        'G#7':                          BASE+84,
        'Ab7':                          BASE+84,
        'A7':                           BASE+85,
        'A#7':                          BASE+86,
        'Bb7':                          BASE+86,
        'B7':                           BASE+87,

        'C8':                           BASE+88,
        'C#8':                          BASE+89,
        'Db8':                          BASE+89,
        'D8':                           BASE+90,
        'D#8':                          BASE+91,
        'Eb8':                          BASE+91,
        'E8':                           BASE+92,
        'F8':                           BASE+93,
        'F#8':                          BASE+94,
        'Gb8':                          BASE+94,
        'G8':                           BASE+95,
        'G#8':                          BASE+96,
        'Ab8':                          BASE+96,
        'A8':                           BASE+97,
        'A#8':                          BASE+98,
        'Bb8':                          BASE+98,
        'B8':                           BASE+99,

        'C9':                           BASE+100,
        'C#9':                          BASE+101,
        'Db9':                          BASE+101,
        'D9':                           BASE+102,
        'D#9':                          BASE+103,
        'Eb9':                          BASE+103,
        'E9':                           BASE+104,
        'F9':                           BASE+105,
        'F#9':                          BASE+106,
        'Gb9':                          BASE+106,
        'G9':                           BASE+107,
        'G#9':                          BASE+108,
        'Ab9':                          BASE+108,
    }

    # Conventional percussion notes on MIDI channel 10 only (GM2==level2).
    # Some shorthands have been added.
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
        'ABD':                          35,
        'Bass Drum 1':		        36,
        'BD1':                          36,
        'Side Stick':		        37,
        'SS':                           37,
        'Acoustic Snare':		38,
        'AS':                           38,
        'Hand Clap':		        39,
        'HC':                           39,
        'Electric Snare':		40,
        'ES':                           40,
        'Low Floor Tom':		41,
        'LFT':                          41,
        'Closed Hi Hat':		42,
        'CHH':                          42,
        'High Floor Tom':		43,
        'HFT':                          43,
        'Pedal Hi-Hat':		        44,
        'PHH':                          44,
        'Low Tom':		        45,
        'LT':                           45,
        'Open Hi-Hat':		        46,
        'OHH':                          46,
        'Low-Mid Tom':		        47,
        'LMT':	                        47,
        'Hi-Mid Tom':		        48,
        'HMT':                          48,
        'Crash Cymbal 1':		49,
        'CC1':                          49,
        'High Tom':		        50,
        'HT':                           51,
        'Ride Cymbal 1':		51,
        'RC1':                          51,
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

    # shorthands for laying down notes:
    # 
    # n( ‘[AS]xx x’ )   - switch to snare, then quarter-quarter-rest-quarter
    # n( ‘..x  .’ )     - 16th-16th-1/4-rest1/2-sixteenth
    #
    # hits:
    #   ,               - 1/32 note  (maybe use 3)
    #   .               - 1/16 note  (maybe use 6)
    #   e               - 1/8  note  (maybe use 8)     
    #   x               - 1/4  note  (maybe use 4)
    # 	X               - 1/2  note  (maybe use 2)
    #   W               - whole note (maybe use 1)
    # 
    # space             - rest for amount of last hit
    #
    # embedded commands are in []:
    #   [v45]           - change default velocity-on to 45  
    #   [0.75]          - skip to time 0.75 within the bar.  0 .. 1 is allowed range.
    #
    def n( s ):
        # TODO
        pass

    # write buffer to <prefix>.mid file
    #
    def write( self, prefix ):
        # TODO
        pass
    
    # TODO: higher-level methods will be added after the above basics are done
