from midiutil.MidiFile import MIDIFile


def create_midi_file(name, bass, snare, hihat):
    assert(type(bass) == str)
    assert(type(snare) == str)
    assert(type(hihat) == str)
    # create your MIDI object
    mf = MIDIFile(1)     #1 track creation
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 240) #bpm=60

    output_bass=bass*4
    output_snare=snare*4
    output_hihat=hihat*4
    firstchannel=0
    secondchannel=1
    thirdchannel=2

    for i in range(len(output_bass)):
        if (int(output_bass[i])==1):
            volume=100
            pitch=55
            time=i
            duration=1
            mf.addProgramChange(track, firstchannel, time, 118)
            mf.addNote(track,firstchannel,pitch,time,duration,volume)
            

    for i in range(len(output_snare)):
        if (int(output_snare[i])==1):
            volume=50
            pitch=60
            time=i
            duration=1
            mf.addProgramChange(track,secondchannel,time,118)
            mf.addNote(track,secondchannel,pitch,time,duration,volume)
            
            
    percussionchannel=9
            
    for i in range(len(output_hihat)):
        if (int(output_hihat[i])==1):
            volume=70
            pitch=68
            time=i
            duration=1
            mf.addProgramChange(track, percussionchannel, time, 118)
            mf.addNote(track,percussionchannel,pitch,time,duration,volume)
    # add some notes

    # write it to disk
    with open(f"beatqraft/static/assets/output{name}.mid", 'wb') as outf:
        mf.writeFile(outf)
