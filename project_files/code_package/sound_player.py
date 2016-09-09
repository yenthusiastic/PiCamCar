from os import system as s

def play_sound(file, volume=0):
    s('omxplayer --vol ' + str(volume) + ' sound-files/' + str(file))


play_sound('hello.wav','80')
play_sound('applause3.mp3','-800')
