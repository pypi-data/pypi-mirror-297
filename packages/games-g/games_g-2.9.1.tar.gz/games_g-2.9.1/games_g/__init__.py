import random
import pyttsx3
import pyaudio

#set text to speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

##############################Guess The Number Console Game#########################################################
def GuessTheNumber() :
        print("Welcome in Number Guessing Game \n")
        try:    
            speak("Welcome in Number Guessing Game")
        except:
            pass
        print("Application Type : Console Game")
        try:    
            speak("Application Type : Console Game")
        except:
            pass
        print("Version : 2.0.1 LTS")
        try:    
            speak("Version : 2.0.1 LTS")
        except:
            pass
        print("Developer : GHANSHYAM VAJA","\n")
        try:    
            speak("Developer : GHANSHYAM vaja")
        except:
            pass
        rand = 0
        randomNumber = 0
        userNumber = 0
        chooseLevel = 0
        easyCount = 5
        mediumCount = 7
        hardCount = 10
        ultrahardCount = 15
        leftCount = 0

        print("    Level         Range       Turns")
        print("1 - Easy       (1 to 100)       5\n2 - Medium     (1 to 1000)      7\n3 - Hard       (1 to 10000)     10\n4 - Ultra Hard (1 to 100000)    15")
        try:    
            speak("1 for Easy       Range = 1 to 100       turns = 5\n")
        except:
            pass
        try:    
            speak("2 for Medium     Range = 1 to 1000      turns=7\n")
        except:
            pass
        try:    
            speak("3 for Hard       Range=1 to 10000     turns=10\n")
        except:
            pass
        try:    
            speak("4 for Ultra Hard Range=1 to 100000    turns=15")
        except:
            pass
        print(" \nChoose Level(1 | 2 | 3 | 4 ) : ", end ="")
        try:    
            speak("Choose Level between 1 to 4")
        except:
            pass
        try:
            chooseLevel = int(input())
        except:
            print("Enter Level between 1 to 4")
        while (chooseLevel <= 0 or chooseLevel > 4) :
            print("Choose Level(1 | 2 | 3 | 4) : ", end ="")
            try:    
                speak("Choose Level")
            except:
                pass
            try:
                chooseLevel = int(input())
            except:
                print("Enter Level between 1 to 4")
        if (chooseLevel == 1) :
            randomNumber = random.randint(0, 101)
        elif(chooseLevel == 2) :
            randomNumber = random.randint(0, 1001)
        elif(chooseLevel == 3) :
            randomNumber = random.randint(0, 10001)
        else :
            randomNumber = random.randint(0,100001)
        while True :
            if (easyCount == 0 or mediumCount == 0 or hardCount == 0 or ultrahardCount == 0) :
                print("\n---------------------------------------------")
                print("GAME OVER", end ="")
                try:    
                    speak("GAME OVER")
                except:
                    pass
                break
            print(" \nGuess A Number Between 1 To ", end ="")
            try:    
                speak(" \nGuess A Number Between 1 To")
            except:
                pass
            if (chooseLevel == 1) :
                easyCount -= 1
                leftCount = easyCount
                print("100", end ="")
                try:    
                    speak("100")
                except:
                    pass
            elif(chooseLevel == 2) :
                mediumCount -= 1
                leftCount = mediumCount
                print("1000", end ="")
                try:    
                    speak("1000")
                except:
                    pass
            elif(chooseLevel == 3) :
                hardCount -= 1
                leftCount = hardCount
                print("10000", end ="")
                try:    
                    speak("10000")
                except:
                    pass
            else :
                ultrahardCount -= 1
                leftCount = ultrahardCount
                print("100000", end ="")
                try:    
                    speak("100000")
                except:
                    pass
            print(" : ", end ="")
            try:
                userNumber = int(input())
            except:
                print("Enter valid Value : ")
            if (userNumber == randomNumber) :
                print("\n---------------------------------------------")
                print(" \nCongratulations, Your Guess Is Correct, YOU WON.....")
                try:    
                    speak("Congratulations, Your Guess Is Correct, YOU WON.....")
                except:
                    pass
            elif(userNumber > randomNumber) :
                print("Your Guess Is Large     Available Turn : " + str(leftCount))
                try:    
                    speak("Your Guess Is Large")
                except:
                    pass
                try:    
                    speak("Available Turn : " + str(leftCount))
                except:
                    pass
            elif(userNumber > 0) :
                print("Your Guess Is Small     Available Turn : " + str(leftCount))
                try:    
                    speak("Your Guess Is Small")
                except:
                    pass
                try:    
                    speak("Available Turn : " + str(leftCount))
                except:
                    pass
            if((userNumber > 0) == False) :
                    break
        print(" \n---------------------------------------------")
        print("Your Answer Is : ")
        print(randomNumber)
        try:    
            speak("Your Answer Is ")
        except:
            pass
        try:
            speak(randomNumber)
        except:
            pass
        print("---------------------------------------------")
###################################################################################################################

####################################Snake and Ladder Console Game##################################################
class Play_With_Computer :
    WONPOINT = 100
    rand =  random.randint(1, 7)
    rollDice = ' '
    playerPosition = 0
    computerPosition = 0
    playerDice = 0
    computerDice = 0
    Name = None
    Snake_Mouth_Position = [0] * (8)
    Snake_Tail_Position = [0] * (8)
    Ladder_Up_Position = [0] * (8)
    Ladder_Down_Position = [0] * (8)
    flag = 0
    Level = ' '
    ctr = 0
    def PlayerAndComputerPosition(self) :
                if (Play_With_Computer.playerPosition > Play_With_Computer.WONPOINT) :
                    Play_With_Computer.playerPosition -= Play_With_Computer.playerDice
                if (Play_With_Computer.computerPosition > Play_With_Computer.WONPOINT) :
                    Play_With_Computer.computerPosition -= Play_With_Computer.computerDice
                # playerPosition With Snake_Tail_Position
                i = 0
                while (i < 8) :
                    if (self.Level == '1' and i < 3) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Snake_Tail_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Snake_Tail_Position[i]
                    elif(self.Level == '2' and i < 5) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Snake_Tail_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Snake_Tail_Position[i]
                    else :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Snake_Tail_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Snake_Tail_Position[i]
                    i += 1
                # playerPosition With Ladder
                i = 0
                while (i < 8) :
                    if (self.Level == '1' and i < 3) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Ladder_Up_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Ladder_Up_Position[i]
                    elif(self.Level == '2' and i < 5) :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Ladder_Up_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Ladder_Up_Position[i]
                    else :
                        if (Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.playerPosition = Play_With_Computer.Ladder_Up_Position[i]
                        elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[i]) :
                            Play_With_Computer.computerPosition = Play_With_Computer.Ladder_Up_Position[i]
                    i += 1
                # player position display
                print("\n--------------------->Player\'s Position<---------------------------")
                try:    
                    speak("Player\'s Position")
                except:
                    pass
                i = 0
                while (i < 2) :
                    if (i == 0) :
                        print(f" \n                         YOU -> {Play_With_Computer.Name}  = {Play_With_Computer.playerPosition}")
                        try:
                            speak(f" \n                         YOU -> {Play_With_Computer.Name}  = {Play_With_Computer.playerPosition}")
                        except:
                            pass
                    else :
                        print(f"                         COMPUTER = {Play_With_Computer.computerPosition}")
                        try:
                            speak(f"                         COMPUTER = {Play_With_Computer.computerPosition}")
                        except:
                            pass
                    i += 1
    def IsWon(self) :
        if (Play_With_Computer.playerPosition == Play_With_Computer.WONPOINT) :
            print("\n---------------------WINNER------------------------------- \n")
            print(f"                          CONGRATS {Play_With_Computer.Name}")
            print("\n---------------------WINNER------------------------------- \n")
            try:    
                speak("\n---------------------WINNER------------------------------- \n")
            except:
                 pass
            try:
                speak(f"                          CONGRATS {Play_With_Computer.Name}")
            except:
                pass
            try:    
                speak("\n---------------------WINNER------------------------------- \n")
            except:
                pass
            self.flag = 1
        if (Play_With_Computer.computerPosition == Play_With_Computer.WONPOINT) :
            print("\n--------------------------------WINNER---------------------------- \n")
            print("                              COMPUTER \n")
            print("                            YOU LOSE !!!!!")
            print("\n------------------------------------------------------------------ \n")
            try:    
                speak("WINNER")
            except:
                pass
            try:    
                speak("COMPUTER")
            except:
                pass
            try:    
                speak("YOU LOSE")
            except:
                pass
            self.flag = 1
    # setGame()
    def setGame(self) :
        print("-------------------------->SET GAME<------------------------------- \n", end ="")
        try:    
            speak("SET GAME")
        except:
            pass
        print("         Levels :   1 - EASY     2 - MEDIUM     3 - HARD \n \n", end ="")
        try:    
            speak("Levels")
        except:
            pass
        try:    
            speak("1 - EASY")
        except:
            pass
        try:    
            speak("2 - MEDIUM")
        except:
            pass
        try:    
            speak("3 - HARD")
        except:
            pass
        print("Choose a Level (1 | 2 | 3 ) : ", end ="")
        try:    
            speak("Choose a Level")
        except:
            pass
        try:    
            speak("1 or 2 or 3 ")
        except:
            pass
        self.Level = input()[0]
        while (self.Level != '1' and self.Level != '2' and self.Level != '3') :
            print("Choose a valid Level (1 | 2 | 3 ) : ", end ="")
            try:    
                speak("Choose a valid Level")
            except:
                pass
            self.Level = input()[0]
        print(" \nEnter Your Name : ", end ="")
        try:    
            speak("Enter Your Name")
        except:
            pass
        Play_With_Computer.Name = input()
    def SnakesAndLaddersPosition(self) :
        if (self.Level == '1') :
            # Snake Mouth Position Setting
            Play_With_Computer.Snake_Mouth_Position[0] = random.randint(95, (99 - 95) + 95)
            Play_With_Computer.Snake_Mouth_Position[1] = random.randint(60, (65 - 60) + 60)
            Play_With_Computer.Snake_Mouth_Position[2] = random.randint(30, (35 - 30) + 30)
            # Snake Tail Position Setting
            Play_With_Computer.Snake_Tail_Position[0] = random.randint(24, (26 - 24) + 24)
            Play_With_Computer.Snake_Tail_Position[1] = random.randint(51, (56 - 51) + 51)
            Play_With_Computer.Snake_Tail_Position[2] = random.randint(15, (19 - 15) + 15)
        elif(self.Level == '2') :
            # Snake Mouth Position Setting
            Play_With_Computer.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_Computer.Snake_Mouth_Position[1] = random.randint(87, (87 - 81) + 81)
            Play_With_Computer.Snake_Mouth_Position[2] = random.randint(55, (59 - 55) + 55)
            Play_With_Computer.Snake_Mouth_Position[3] = random.randint(32, (38 - 32) + 32)
            Play_With_Computer.Snake_Mouth_Position[4] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_Computer.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_Computer.Snake_Tail_Position[1] = random.randint(72, (78 - 72) + 72)
            Play_With_Computer.Snake_Tail_Position[2] = random.randint(41, (42 - 41) + 41)
            Play_With_Computer.Snake_Tail_Position[3] = random.randint(26, (29 - 26) + 26)
            Play_With_Computer.Snake_Tail_Position[4] = random.randint(6,  (9 - 6) + 6)
        else :
            # Snake Mouth Position Setting
            Play_With_Computer.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_Computer.Snake_Mouth_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Snake_Mouth_Position[2] = random.randint(71, (74 - 71) + 71)
            Play_With_Computer.Snake_Mouth_Position[3] = random.randint(62, (65 - 62) + 62)
            Play_With_Computer.Snake_Mouth_Position[4] = random.randint(41, (42 - 41) + 41)
            Play_With_Computer.Snake_Mouth_Position[5] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Snake_Mouth_Position[6] = random.randint(24, (26 - 24) + 24)
            Play_With_Computer.Snake_Mouth_Position[7] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_Computer.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_Computer.Snake_Tail_Position[1] = random.randint(41, (45 - 41) + 41)
            Play_With_Computer.Snake_Tail_Position[2] = random.randint(32, (36 - 32) + 32)
            Play_With_Computer.Snake_Tail_Position[3] = random.randint(22, (26 - 22) + 22)
            Play_With_Computer.Snake_Tail_Position[4] = random.randint(26, (29 - 26) + 26)
            Play_With_Computer.Snake_Tail_Position[5] = random.randint(15, (19 - 15) + 15)
            Play_With_Computer.Snake_Tail_Position[6] = random.randint(15, (19 - 15) + 15)
            Play_With_Computer.Snake_Tail_Position[7] = random.randint(6, (9 - 6) + 6)
        if (self.Level == '1') :
            # Ladder Down Position Setting
            Play_With_Computer.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_Computer.Ladder_Down_Position[1] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Ladder_Down_Position[2] = random.randint(87, (87 - 81) + 81)
            # Laddet Up Position Setting
            Play_With_Computer.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Ladder_Up_Position[2] = random.randint(96, (99 - 96) + 96)
        elif(self.Level == '2') :
            # Ladder Down Position Setting
            Play_With_Computer.Ladder_Down_Position[0] = random.randint(15, (19 - 15) + 15)
            Play_With_Computer.Ladder_Down_Position[1] = random.randint(37, (38 - 37) + 37)
            Play_With_Computer.Ladder_Down_Position[2] = random.randint(51, (59 - 51) + 51)
            Play_With_Computer.Ladder_Down_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Ladder_Down_Position[4] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_Computer.Ladder_Up_Position[0] = random.randint(81, (86 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[1] = random.randint(41, (42 - 41) + 41)
            Play_With_Computer.Ladder_Up_Position[2] = random.randint(81, (86 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[3] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Ladder_Up_Position[4] = random.randint(96, (99 - 96) + 96)
        else :
            # Ladder Down Position Setting
            Play_With_Computer.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_Computer.Ladder_Down_Position[1] = random.randint(24, (26 - 24) + 24)
            Play_With_Computer.Ladder_Down_Position[2] = random.randint(36, (38 - 36) + 36)
            Play_With_Computer.Ladder_Down_Position[3] = random.randint(41, (45 - 41) + 41)
            Play_With_Computer.Ladder_Down_Position[4] = random.randint(54, (59 - 54) + 54)
            Play_With_Computer.Ladder_Down_Position[5] = random.randint(68, (69 - 68) + 68)
            Play_With_Computer.Ladder_Down_Position[6] = random.randint(72, (78 - 72) + 72)
            Play_With_Computer.Ladder_Down_Position[7] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_Computer.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_Computer.Ladder_Up_Position[2] = random.randint(74, (78 - 74) + 74)
            Play_With_Computer.Ladder_Up_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_Computer.Ladder_Up_Position[4] = random.randint(81, (87 - 81) + 81)
            Play_With_Computer.Ladder_Up_Position[5] = random.randint(74, (78 - 74) + 74)
            Play_With_Computer.Ladder_Up_Position[6] = random.randint(95, (96 - 95) + 95)
            Play_With_Computer.Ladder_Up_Position[7] = random.randint(92, (99 - 92) + 92)
    def SnakesAndLaddersPositionPrint(self) :
        print(" \n-------->SNAKES POSITION           |      LADDERS POSITION <--------- \n", end ="")
        try:    
            speak("SNAKES POSITION and LADDERS POSITION")
        except:
            pass
        if (self.Level == '1') :
            i = 0
            while (i < 3) :
                if (i == 0) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    0{Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                i += 1
        elif(self.Level == '2') :
            i = 0
            while (i < 5) :
                if (i == 0) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                elif(i == 4) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   0{Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                i += 1
        else :
            i = 0
            while (i < 8) :
                if (i == 0) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    0{Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                elif(i == 7) :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   0{Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_Computer.Snake_Mouth_Position[i]}     to   {Play_With_Computer.Snake_Tail_Position[i]}      |    {Play_With_Computer.Ladder_Down_Position[i]}     to    {Play_With_Computer.Ladder_Up_Position[i]}")
                i += 1
        print("------------------------------------------------------------------- \n", end ="")
    def RollDice(self) :
        print(" \n----------------------->Roll The Dice<-----------------------------\n", end ="")
        try:    
            speak("Roll The Dice")
        except:
            pass
        print(f" \n            {Play_With_Computer.Name}\'s Turn (Enter character \"R\" or \"r\" ) : ", end ="")
        try:    
            speak("Enter character Capital or Small R")
        except:
            pass
        Play_With_Computer.rollDice = input()
        while (Play_With_Computer.rollDice != 'R' and Play_With_Computer.rollDice != 'r') :
            print("               Enter Valid Character R or r : ", end ="")
            try:    
                speak("Enter Valid Character Capital or Small R")
            except:
                pass
            Play_With_Computer.rollDice = input()
        Play_With_Computer.playerDice = random.randint(1, (6 - 1) + 1)
        Play_With_Computer.playerPosition += Play_With_Computer.playerDice
        print(f"                     Your Dice Score : {Play_With_Computer.playerDice}")
        I = 0
        while (I < 8) :
            if (self.Level == '1' and I < 3) :
                if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(f" \n        --------->Oops, {Play_With_Computer.Name} Swallowed By Snake<---------")
                    try:
                        speak(f"Oops, {Play_With_Computer.Name} Swallowed By Snake")
                    except:
                        pass
                    
                elif(Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(f" \n            ----->Hurry, {Play_With_Computer.Name} Climb Up The Ladder<-----")
                    try:
                        speak(f">Hurry, {Play_With_Computer.Name} Climb Up The Ladder")
                    except:
                        pass
            elif(self.Level == '2' and I < 5) :
                if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(f" \n        --------->Oops, {Play_With_Computer.Name} Swallowed By Snake<---------")
                    try:
                        speak(f"nOops, {Play_With_Computer.Name} Swallowed By Snake")
                    except:
                        pass
                elif(Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(f" \n            ----->Hurry, {Play_With_Computer.Name} Climb Up The Ladder<-----")
                    try:
                        speak(f"Hurry, {Play_With_Computer.Name} Climb Up The Ladder")
                    except:
                        pass
            else :
                if (Play_With_Computer.playerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(f" \n        --------->Oops, {Play_With_Computer.Name} Swallowed By Snake<---------")
                    try:
                        speak(f"Oops, {Play_With_Computer.Name} Swallowed By Snake")
                    except:
                        pass
                elif(Play_With_Computer.playerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(f" \n            ----->Hurry, {Play_With_Computer.Name} Climb Up The Ladder<-----")
                    try:
                        speak(f"Hurry, {Play_With_Computer.Name} Climb Up The Ladder")
                    except:
                        pass
            I += 1
        print("\n                   Computer\'s Turn (Wait) : ", end ="")
        try:    
            speak("Computer\'s Turn (Wait)")
        except:
            pass
        Play_With_Computer.computerDice = random.randint(1, (6 - 1) + 1)
        Play_With_Computer.computerPosition += Play_With_Computer.computerDice
        try :
            # Thread
            k = 0
            while (k < 5) :
                Thread.sleep(501)
                k += 1
        except Exception as expn :
            if (random.randint(6, (9 - 6) + 6)% 2 == 0) :
                print(f"R \n                   Computer\'s Dice Score : {Play_With_Computer.computerDice}")
            else :
                print(f"r \n                   Computer\'s Dice Score : {Play_With_Computer.computerDice}")
            I = 0
        while (I < 8) :
            if (self.Level == '1' and I < 3) :
                if (Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(" \n       -------->Computer Swallowed By Snake<---------")
                    try:    
                        speak("Computer Swallowed By Snake")
                    except:
                        pass
                elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(" \n       -------->Computer Climb Up The Ladder<-------")
                    try:    
                        speak("Computer Climb Up The Ladder")
                    except:
                        pass
            elif(self.Level == '2' and I < 5) :
                if (Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(" \n       -------->Computer Swallowed By Snake<---------")
                    try:    
                        speak("Computer Swallowed By Snake")
                    except:
                        pass
                elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(" \n       -------->Computer Climb Up The Ladder<-------")
                    try:    
                        speak("Computer Climb Up The Ladder")
                    except:
                        pass
            else :
                if (Play_With_Computer.computerPosition == Play_With_Computer.Snake_Mouth_Position[I]) :
                    print(" \n       -------->Computer Swallowed By Snake<---------")
                    try:    
                        speak("Computer Swallowed By Snake")
                    except:
                        pass
                elif(Play_With_Computer.computerPosition == Play_With_Computer.Ladder_Down_Position[I]) :
                    print(" \n       -------->Computer Climb Up The Ladder<-------")
                    try:    
                        speak("Computer Climb Up The Ladder")
                    except:
                        pass
            I += 1
        if (self.flag != 1) :
            self.PlayerAndComputerPosition()
            self.IsWon()
#Play_with_friends class
class Play_With_friends :
    WONPOINT = 100
    rand =  random.randint(1, 7)
    n = 100
    rollDice = ' '
    playerPosition = [0] * (n)
    diceScore = [0] * (n)
    Names = [None] * (n)
    Snake_Mouth_Position = [0] * (8)
    Snake_Tail_Position = [0] * (8)
    Ladder_Up_Position = [0] * (8)
    Ladder_Down_Position = [0] * (8)
    flag = 0
    Level = ' '
    Count = 0
    Snake_flag = 0
    Ladder_flag = 0
    # setGame()
    def setGame(self) :
        print("-------------------------->SET GAME<------------------------------- \n", end ="")
        try:    
            speak("SET GAME")
        except:
            pass
        print("         Levels :   1 - EASY     2 - MEDIUM     3 - HARD \n \n", end ="")
        try:    
            speak("Levels")
        except:
            pass
        try:    
            speak("1 - EASY")
        except:
            pass
        try:    
            speak("2 - MEDIUM")
        except:
            pass
        try:    
            speak("3 - HARD")
        except:
            pass
        print("Choose a Level (1 | 2 | 3 ) : ", end ="")
        try:    
            speak("Choose a Level")
        except:
            pass
        try:    
            speak("1 or 2 or 3 ")
        except:
            pass
        self.Level = input()
        while (self.Level != '1' and self.Level != '2' and self.Level != '3') :
            print("Choose a valid Level (1 | 2 | 3 ) : ", end ="")
            try:    
                speak("Choose a valid Level")
            except:
                pass
            self.Level = input()
    # setPlayer()
    def SetPlayer(self) :
        print(" \nEnter no. of Players : ", end ="")
        try:    
            speak("Enter number of Players")
        except:
            pass
        try:
            Play_With_friends.n = int(input())
        except:
            printf("Enter valid Value : ")
        while (self.n < 0) :
            print("Enter Valid no. of Players : ")
            try:    
                speak("Enter Valid no. of Players")
            except:
                pass
            Play_With_friends.n = input()
        print(" \nEnter players Names : ")
        try:    
            speak("Enter players Names")
        except:
            pass
        i = 0
        while (i < Play_With_friends.n) :
            print(f"player {i + 1}  : ", end ="")
            try:
                speak(f"Enter player {i + 1}  Name")
            except:
                pass
            Play_With_friends.Names[i] = input()
            i += 1
    def SnakesAndLaddersPosition(self) :
        if (self.Level == '1') :
            # Snake Mouth Position Setting
            Play_With_friends.Snake_Mouth_Position[0] = random.randint(95, (99 - 95) + 95)
            Play_With_friends.Snake_Mouth_Position[1] = random.randint(60, (65 - 60) + 60)
            Play_With_friends.Snake_Mouth_Position[2] = random.randint(30, (35 - 30) + 30)
            # Snake Tail Position Setting
            Play_With_friends.Snake_Tail_Position[0] = random.randint(24, (26 - 24) + 24)
            Play_With_friends.Snake_Tail_Position[1] = random.randint(51, (56 - 51) + 51)
            Play_With_friends.Snake_Tail_Position[2] = random.randint(15, (19 - 15) + 15)
        elif(self.Level == '2') :
            # Snake Mouth Position Setting
            Play_With_friends.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_friends.Snake_Mouth_Position[1] = random.randint(87, (87 - 81) + 81)
            Play_With_friends.Snake_Mouth_Position[2] = random.randint(55, (59 - 55) + 55)
            Play_With_friends.Snake_Mouth_Position[3] = random.randint(32, (38 - 32) + 32)
            Play_With_friends.Snake_Mouth_Position[4] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_friends.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_friends.Snake_Tail_Position[1] = random.randint(72, (78 - 72) + 72)
            Play_With_friends.Snake_Tail_Position[2] = random.randint(41, (42 - 41) + 41)
            Play_With_friends.Snake_Tail_Position[3] = random.randint(26, (29 - 26) + 26)
            Play_With_friends.Snake_Tail_Position[4] = random.randint(6,  (9 - 6) + 6)
        else :
            # Snake Mouth Position Setting
            Play_With_friends.Snake_Mouth_Position[0] = random.randint(98, (99 - 98) + 98)
            Play_With_friends.Snake_Mouth_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Snake_Mouth_Position[2] = random.randint(71, (74 - 71) + 71)
            Play_With_friends.Snake_Mouth_Position[3] = random.randint(62, (65 - 62) + 62)
            Play_With_friends.Snake_Mouth_Position[4] = random.randint(41, (42 - 41) + 41)
            Play_With_friends.Snake_Mouth_Position[5] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Snake_Mouth_Position[6] = random.randint(24, (26 - 24) + 24)
            Play_With_friends.Snake_Mouth_Position[7] = random.randint(15, (19 - 15) + 15)
            # Snake Tail Position Setting
            Play_With_friends.Snake_Tail_Position[0] = random.randint(51, (56 - 51) + 51)
            Play_With_friends.Snake_Tail_Position[1] = random.randint(41, (45 - 41) + 41)
            Play_With_friends.Snake_Tail_Position[2] = random.randint(32, (36 - 32) + 32)
            Play_With_friends.Snake_Tail_Position[3] = random.randint(22, (26 - 22) + 22)
            Play_With_friends.Snake_Tail_Position[4] = random.randint(26, (29 - 26) + 26)
            Play_With_friends.Snake_Tail_Position[5] = random.randint(15, (19 - 15) + 15)
            Play_With_friends.Snake_Tail_Position[6] = random.randint(15, (19 - 15) + 15)
            Play_With_friends.Snake_Tail_Position[7] = random.randint(6, (9 - 6) + 6)
        if (self.Level == '1') :
            # Ladder Down Position Setting
            Play_With_friends.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_friends.Ladder_Down_Position[1] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Ladder_Down_Position[2] = random.randint(87, (87 - 81) + 81)
            # Laddet Up Position Setting
            Play_With_friends.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Ladder_Up_Position[2] = random.randint(96, (99 - 96) + 96)
        elif(self.Level == '2') :
            # Ladder Down Position Setting
            Play_With_friends.Ladder_Down_Position[0] = random.randint(15, (19 - 15) + 15)
            Play_With_friends.Ladder_Down_Position[1] = random.randint(37, (38 - 37) + 37)
            Play_With_friends.Ladder_Down_Position[2] = random.randint(51, (59 - 51) + 51)
            Play_With_friends.Ladder_Down_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Ladder_Down_Position[4] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_friends.Ladder_Up_Position[0] = random.randint(81, (86 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[1] = random.randint(41, (42 - 41) + 41)
            Play_With_friends.Ladder_Up_Position[2] = random.randint(81, (86 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[3] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Ladder_Up_Position[4] = random.randint(96, (99 - 96) + 96)
        else :
            # Ladder Down Position Setting
            Play_With_friends.Ladder_Down_Position[0] = random.randint(6, (9 - 6) + 6)
            Play_With_friends.Ladder_Down_Position[1] = random.randint(24, (26 - 24) + 24)
            Play_With_friends.Ladder_Down_Position[2] = random.randint(36, (38 - 36) + 36)
            Play_With_friends.Ladder_Down_Position[3] = random.randint(41, (45 - 41) + 41)
            Play_With_friends.Ladder_Down_Position[4] = random.randint(54, (59 - 54) + 54)
            Play_With_friends.Ladder_Down_Position[5] = random.randint(68, (69 - 68) + 68)
            Play_With_friends.Ladder_Down_Position[6] = random.randint(72, (78 - 72) + 72)
            Play_With_friends.Ladder_Down_Position[7] = random.randint(81, (86 - 81) + 81)
            # Ladder Up Position Setting
            Play_With_friends.Ladder_Up_Position[0] = random.randint(81, (87 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[1] = random.randint(92, (96 - 92) + 92)
            Play_With_friends.Ladder_Up_Position[2] = random.randint(74, (78 - 74) + 74)
            Play_With_friends.Ladder_Up_Position[3] = random.randint(65, (69 - 65) + 65)
            Play_With_friends.Ladder_Up_Position[4] = random.randint(81, (87 - 81) + 81)
            Play_With_friends.Ladder_Up_Position[5] = random.randint(74, (78 - 74) + 74)
            Play_With_friends.Ladder_Up_Position[6] = random.randint(95, (96 - 95) + 95)
            Play_With_friends.Ladder_Up_Position[7] = random.randint(92, (99 - 92) + 92)
    def SnakesAndLaddersPositionPrint(self) :
        print(" \n-------->SNAKES POSITION           |      LADDERS POSITION <--------- \n", end ="")
        try:    
            speak("SNAKES POSITION and LADDERS POSITION")
        except:
            pass
        if (self.Level == '1') :
            i = 0
            while (i < 3) :
                if (i == 0) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    0{Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                i += 1
        elif(self.Level == '2') :
            i = 0
            while (i < 5) :
                if (i == 0) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                elif(i == 4) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   0{Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                i += 1
        else :
            i = 0
            while (i < 8) :
                if (i == 0) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    0{Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                elif(i == 7) :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   0{Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                else :
                    print(f"               {Play_With_friends.Snake_Mouth_Position[i]}     to   {Play_With_friends.Snake_Tail_Position[i]}      |    {Play_With_friends.Ladder_Down_Position[i]}     to    {Play_With_friends.Ladder_Up_Position[i]}")
                i += 1
        print("------------------------------------------------------------------- \n", end ="")
    def RollDice(self) :
        print("\n------------------------>Roll The Dice<--------------------------\n", end ="")
        try:    
            speak("Roll The Dice")
        except:
            pass
        i = 0
        while (i < Play_With_friends.n) :
            print(f" \n           {Play_With_friends.Names[i]}\'s Turn (Enter character "R" or "r" ) : ", end ="")
            try:
                speak(f"{Play_With_friends.Names[i]}\'s Turn")
            except:
                pass
            try:    
                speak("Enter Capital or Small R")
            except:
                pass
            Play_With_friends.rollDice = input()
            while (Play_With_friends.rollDice != 'R' and Play_With_friends.rollDice != 'r') :
                print("\n           Enter Valid Character R or r : ")
                try:    
                    speak("Enter Valid Capital or Small R")
                except:
                    pass
                Play_With_friends.rollDice = input()
            Play_With_friends.diceScore[i] = random.randint(1, (6 - 1) + 1)
            Play_With_friends.playerPosition[i] += Play_With_friends.diceScore[i]
            print(f"                     dice Score = {Play_With_friends.diceScore[i]}")
            try:
                speak(f"dice Score = {Play_With_friends.diceScore[i]}")
            except:
                pass
            I = 0
            while (I < Play_With_friends.n) :
                k = 0
                while (k < 8) :
                    if (self.Level == '1' and I < 3) :
                        if (Play_With_friends.playerPosition[I] == Play_With_friends.Snake_Mouth_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Snake_Mouth_Position[k] != 0)) :
                            print(" \n        --------->Oops, Swallowed By Snake<---------")
                            try:    
                                speak("Oops, Swallowed By Snake")
                            except:
                                pass
                        elif(Play_With_friends.playerPosition[I] == Play_With_friends.Ladder_Down_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Ladder_Down_Position[k] != 0)) :
                            print(" \n            ----->Hurry, Climb Up The Ladder<-----")
                            try:    
                                speak("Hurry, Climb Up The Ladder")
                            except:
                                pass
                    elif(self.Level == '2' and I < 5) :
                        if (Play_With_friends.playerPosition[I] == Play_With_friends.Snake_Mouth_Position[k]  and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Snake_Mouth_Position[k] != 0)) :
                            print(" \n        --------->Oops, Swallowed By Snake<---------")
                            try:    
                                speak("Oops, Swallowed By Snake")
                            except:
                                pass
                        elif(Play_With_friends.playerPosition[I] == Play_With_friends.Ladder_Down_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Ladder_Down_Position[k] != 0)) :
                            print(" \n            ----->Hurry, Climb Up The Ladder<-----")
                            try:    
                                speak("Hurry, Climb Up The Ladder")
                            except:
                                pass
                    else :
                        if (Play_With_friends.playerPosition[I] == Play_With_friends.Snake_Mouth_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Snake_Mouth_Position[k] != 0)) :
                            print(" \n        --------->Oops, Swallowed By Snake<---------")
                            try:    
                                speak("Oops, Swallowed By Snake")
                            except:
                                pass
                        elif(Play_With_friends.playerPosition[I] == Play_With_friends.Ladder_Down_Position[k] and (Play_With_friends.playerPosition[I] != 0 and Play_With_friends.Ladder_Down_Position[k] != 0)) :
                            print(" \n            ----->Hurry, Climb Up The Ladder<-----")
                            try:    
                                speak("Hurry, Climb Up The Ladder")
                            except:
                                pass
                    k += 1
                I += 1
            if (self.flag != 1) :
                self.PlayerPosition()
                self.IsWon()
            i += 1
    def PlayerPosition(self) :
        i = 0
        while (i < Play_With_friends.n) :
            if (Play_With_friends.playerPosition[i] > Play_With_friends.WONPOINT) :
                Play_With_friends.playerPosition[i] -= Play_With_friends.diceScore[i]
            i += 1
        # playerPosition With Snake_Tail_Position
        i = 0
        while (i < Play_With_friends.n) :
            if (self.Level == '1') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[2]
            elif(self.Level == '2') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[4]
                else :
                    pass
            else :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[4]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[5]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[5]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[6]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[6]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Snake_Mouth_Position[7]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Snake_Tail_Position[7]
            i += 1
        # playerPosition With Ladder
        i = 0
        while (i < Play_With_friends.n) :
            if (self.Level == '1') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[2]
            elif(self.Level == '2') :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[4]
            else :
                if (Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[0]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[0]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[1]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[1]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[2]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[2]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[3]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[3]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[4]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[4]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[5]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[5]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[6]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[6]
                elif(Play_With_friends.playerPosition[i] == Play_With_friends.Ladder_Down_Position[7]) :
                    Play_With_friends.playerPosition[i] = Play_With_friends.Ladder_Up_Position[7]
            i += 1
        # player position display
        print("\n------------------:::::Player\'s Position:::::------------------ \n")
        try:    
            speak("Player\'s Position")
        except:
            pass
        i = 0
        while (i < Play_With_friends.n) :
            self.Count = 1
            if (Play_With_friends.diceScore[i] > 0) :
                print(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
                try:
                    speak(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
                except:
                    pass
            else :
                print(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
                try:
                    speak(f"CURRENT :                    {Play_With_friends.Names[i]}  = {Play_With_friends.playerPosition[i]}")
                except:
                    pass
            if (i == Play_With_friends.n - 1) :
                print("------------------------------------------------------------------- ", end ="")
            self.Count += 1
            Play_With_friends.diceScore[i] = 0
            i += 1
    def IsWon(self) :
        i = 0
        while (i < Play_With_friends.n) :
            if (Play_With_friends.playerPosition[i] == Play_With_friends.WONPOINT) :
                print("\n-------------------------WINNER----------------------------------- \n")
                print(f"                          CONGRATS {Play_With_friends.Names[i]}")
                try:
                    speak(f"CONGRATS {Play_With_friends.Names[i]} you won.")
                except:
                    pass
                print("\n-------------------------WINNER----------------------------------- \n")
                self.flag = 1
                break
            if (self.flag == 1) :
                break
            i += 1

def SnakeAndLadder() :
    print("                 Welcome To SNACK AND LADDER GAME \n-------------------------------------------------------------------\n")
    try:    
        speak("Welcome To SNACK AND LADDER GAME")
    except:
        pass
    print("Application Type : Console Game")
    try:    
        speak("Application Type : Console Game")
    except:
        pass
    print("Version : 1.0.1 LTS")
    try:    
        speak("Version : 1.0.1 LTS")
    except:
        pass
    print("Developer : GHANSHYAM VAJA")
    try:    
        speak("Developer : GHANSHYAM vaja")
    except:
        pass
    print("-------------------------------------------------------------------")
    playWith = ' '
    print("\n       1 - play With Computer         2 - play With friends")
    print(" \nEnter Your choice (1 | 2) : ", end ="")
    try:    
        speak("Enter Your choice")
    except:
        pass
    try:    
        speak("1 for play With Computer")
    except:
        pass
    try:    
        speak("2 for play With friends")
    except:
        pass
    playWith = input()
    while (playWith != '1' and playWith != '2') :
        print(" \nEnter valid choice (1 | 2) : ", end ="")
        try:    
            speak("Enter valid choice")
        except:
            pass
        try:    
            speak("1 or 2")
        except:
            pass
        playWith = input()
    print(" \n::::::::::::::::::::---->WINPOINT : 100<----:::::::::::::::::::: \n")
    try:    
        speak("WINPOINT 100")
    except:
        pass
    if (playWith == '1') :
        obj = Play_With_Computer()
        i = 1
        while (obj.flag != 1) :
            if (i == 1) :
                obj.setGame()
                obj.SnakesAndLaddersPosition()
            obj.SnakesAndLaddersPositionPrint()
            if (i == 1) :
                print("\n-------------------::Lets Start The Game::------------------------- ", end ="")
                try:    
                    speak("Lets Start The Game")
                except:
                    pass
            obj.RollDice()
            # obj.PlayerPosition();
            # obj.IsWon();
            i = 2
    else :
        obj2 = Play_With_friends()
        k = 1
        while (obj2.flag != 1) :
            if (k == 1) :
                obj2.setGame()
                obj2.SetPlayer()
                obj2.SnakesAndLaddersPosition()
            obj2.SnakesAndLaddersPositionPrint()
            if (k == 1) :
                print("\n-------------------::Lets Start The Game::------------------------- ", end ="")
                try:    
                    speak("Lets Start The Game")
                except:
                    pass
            obj2.RollDice()
            k = 2