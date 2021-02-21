# 0: Morse code saying ("flip"), turn box to see a call to action
# 1: Open up the box
# 2: Decode a Messagee
# 3: Tilt to make a circle
# 4: Tilt to say which direction a note went
# 5: Tilt to play a song
# 6: Close box up, motor run

import music
from microbit import *

# Morse Code Letters
morseTuneF = ["c5:2","c5:2","c5:6","c5:2","r:4"]
morseTuneL = ["c5:2","c5:6","c5:2","c5:2","r:4"]
morseTuneI = ["c5:2","c5:2","r:4"]
morseTuneP = ["c5:2","c5:6","c5:6","c5:2","r:8"]

# Array of Tunes
morseTune = [morseTuneF,morseTuneL,morseTuneI,morseTuneP]

# Win Jingle
winTune = ["f5","g5","A#5"]

# Image for the start
mainImage = Image()

           
# Round 0: Morse   
def morse():
    morseToPlay = 0
    while True:
        if accelerometer.current_gesture() == "face down" or button_a.is_pressed():
            break
        sleep(100)
        music.play(morseTune[morseToPlay])
        morseToPlay += 1
        morseToPlay = morseToPlay % 4
    win(count)
    
# Morse Win
def morseW():
    music.play(winTune)
    mainImage.fill(1)
    display.show(mainImage)

# Round 1: Open the box
def openUp():
    while True:
        if(display.read_light_level() > 25):
            break
    win(count)

# Open up Win
def openUpW():
    mainImage.fill(5)
    music.play(winTune)
    mainImage.fill(0)

# Round 2: Show Ceasar Cipher, put in up postion
def welcome():
    display.show("ujmu vq 1 ^",delay=1000)
    while True:
        if accelerometer.current_gesture() == "up":
            break
    win(count)

def welcomeW():
    music.play(winTune)

# Shows a piece of cirlce and asks the player which part it is?
def circleRun(bigPic,smallPic,hor,vert):
    display.show(Image(bigPic))
    sleep(2000)
    display.show(Image("99000:99000:99000:99000:99000"))
    sleep(500)
    display.show(Image("00099:00099:00099:00099:00099"))
    sleep(500)
    display.show("?")
    while True:
        if(accelerometer.current_gesture() == hor):
            break
    display.show(Image(bigPic))
    sleep(2000)
    display.show(Image("99999:99999:00000:00000:00000"))
    sleep(500)
    display.show(Image("00000:00000:00000:99999:99999"))
    sleep(500)
    display.show("?")
    while True:
        if(accelerometer.current_gesture() == vert):
            break
    display.show(Image(smallPic))
    sleep(600)

# Round 3: Shows parts of a circle, cryptic tilt puzzle
def circle():
    circleRun("00099:09900:09000:90000:90000","09900:90000:90000:00000:00000","left","down")
    circleRun("90000:90000:09000:09900:00099","00000:00000:90000:90000:09900","left","up")
    circleRun("99000:00990:00090:00009:00009","00990:00009:00009:00000:00000","right","down")
    circleRun("00009:00009:00090:00990:99000","00000:00000:00009:00009:00990","right","up")
    display.show(Image("09990:90009:90009:90009:09990"))
    win(count)
    
    
def circleW():
    music.play(winTune)

# Plays two notes, and is correct if in the right direction
def tiltRun(note1,note2,direction,showDir=""):
    music.play(note1)
    sleep(500)
    music.play(note2)
    sleep(500)
    if(showDir):
        display.show(showDir)
    while True:
        if accelerometer.current_gesture() == direction:
            break
    while True:
        if accelerometer.current_gesture() == "face up":
            break

# Round 4: Pitch Quiz, tilt which direection the pitch is going
def tilt():
    display.scroll("Pitch Quiz")
    tiltRun("c5","c4","left",showDir="<")
    tiltRun("c3","c4","right",showDir=">")
    display.clear()
    tiltRun("a4","b5","right")
    tiltRun("g3","a2","left")
    tiltRun("a3","g3","right")
    win(count)

def tiltW():
    music.play(winTune)
    
# Round 5: Play a song, no puzzle just a play a good song
def song():
    display.scroll("Play a Song")
    e = 0
    while e < 50:
        music.pitch((accelerometer.get_x() + 1000)//2)
        sleep(300)
        e += 1

    win(count)
    
def songW():
    music.stop();
    music.play(winTune)
    display.scroll("Nice Song!")
    pass

# Round 6: Close the box to open the treeasure 
def closeBox():
    display.scroll("Goodnight")
    display.show("99999:99999:09990:09990:09990")
    while True:
        if read_light_level() < 25:
            break
    win(count)
    
# Runs the motor from pin 1 
def closeBoxW():
    pin1.set_analog_period(20)
    pin1.write_analog(178)
    sleep(10000)
    pin1.write_analog(1)
    music.play(winTune)
    music.play(winTune)


# Runs the win value, and prints to the cosnle
def win(value):
    print("Won Round " + str(value))
    wins[value]()
    print("Going to next Round")

# List of rounds and the win function
rounds = [morse,openUp,welcome,circle,tilt,song,closeBox]
wins = [morseW,openUpW,welcomeW,circleW,tiltW,songW,closeBoxW]

# Counts the rounds
count = 0

# Runs the rounds
if __name__ == "__main__":
    display.show(mainImage)
    pin1.write_analog(1)
    
    while count < len(rounds) - 1:
        print("Beginning Round: " + str(count))
        rounds[count]()
        count += 1
    
    display.scroll("You won the puzzle box!")