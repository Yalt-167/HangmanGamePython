
import pygame as pg
import webbrowser
import sys
from math import sin
from typing import Generator

from Display import Display
from Words import Words

class Game:
    def __init__(self, defaultWordLength : int = 6) -> None:
        self.display: Display = Display()

        self.running: bool = True
        self.won: bool = False

        self.clock: pg.time.Clock = pg.time.Clock()

        self.alphabet: str = "abcdefghijklmnopqrstuvwxyz"
        self.wordLength: int = defaultWordLength
        self.SelectNewWord()
        self.keyToLength: dict[int, int] = {
            pg.K_3 : 3,
            pg.K_4 : 4,
            pg.K_5 : 5,
            pg.K_6 : 6,
            pg.K_7 : 7,
            pg.K_8 : 8,
            pg.K_9 : 9
        }

        self.wrongGuesses: int = 0
        self.maxWrongGuesses: int = 11
        self.usedletters : list[str] = []

        self.timerToRenderInvalidGuessMessage: int = 0
        self.timerToRenderWrongLetterErrorMessageAndLetter: list[int, str|None] = [0, None]

        self.images: dict[str, pg.surface.Surface]  = {
            str(i) : pg.transform.scale(
                pg.image.load(f"imgs/img{i}.jpg"),(self.display.W, self.display.H)
            ) for i in range(11)
        }

        self.images["win"] = pg.transform.scale(
            pg.image.load("imgs/win_screen.jpg"), (self.display.W, self.display.H)
        )

        self.images["loss"] = pg.transform.scale(
            pg.image.load("imgs/loss_screen.jpg"), (self.display.W, self.display.H)
        )

    def Run(self):
        w = " ".join(self.currentWord)
        print(f"The word is {w}")
        while not self.won:

            guess = input("Guess a letter : ")

            try:
                self.PlaceGuess(guess)
            except NameError:
                print(f"You already tried this letter ({guess})")
            except AttributeError:
                print(f"This guess is not valid ({guess})")

            print(f"The letters used are : {self.used_letters}({self.wrongGuesses} wrong guesses)")
            w = " ".join(self.currentWord)
            print(f"The current word you found is : {w}\n")

            if self.test_if_lost():
                break
            self.won = self.test_if_won()

        else:
            print("Congrats you won the game")
            sys.exit()
        print(f"You lost. The word was \"{self.word}\"")

    def RunOnDisplay(self):

        self.SplashScreen()

        while True:

            # reset
            self.usedletters : list[str] = []
            self.wrongGuesses: int = 0
            self.running: bool = True
            self.won: bool = False
            self.SelectNewWord()

            #main loop
            while not self.won:

                self.clock.tick(60)

                self.display.window.blit(
                    self.images[str(self.wrongGuesses)],
                    (0, 0)
                ) # draw background

                for event in pg.event.get():

                    if event.type == pg.KEYDOWN:

                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                            sys.exit()

                        guess: str = event.unicode.lower()

                        try:
                            if guess not in self.alphabet:
                                raise AttributeError # not a letter
                            self.PlaceGuess(guess)

                        except NameError:
                            self.timerToRenderWrongLetterErrorMessageAndLetter = [120, guess] # 2s cah 60FPS


                        except AttributeError:
                            self.timerToRenderInvalidGuessMessage = 120 # 2s still

                if self.timerToRenderWrongLetterErrorMessageAndLetter[0] > 0: # if a wrong letter error occured in the last 2 s
                    self.timerToRenderWrongLetterErrorMessageAndLetter[0] -= 1 # decrease the "timer"
                    self.display.window.blit(
                        self.display.font.render(
                            f"You already tried this letter ({self.timerToRenderWrongLetterErrorMessageAndLetter[1]})",
                            True, (255, 255, 255)
                            ),
                            (400, 550)
                    ) # blit appropriate message error

                if self.timerToRenderInvalidGuessMessage: # if a invalid_guess error occured in the last 2 s
                    self.timerToRenderInvalidGuessMessage -= 1
                    self.display.window.blit(
                        self.display.font.render(
                            f"This guess is not valid",
                            True, (255, 255, 255)
                        ),
                        (400, 600)
                    ) # blit appropriate message error

                self.display.window.blit(
                    self.display.font.render(
                        f"The letters you already used are : {self.usedletters}({self.wrongGuesses}/{self.maxWrongGuesses} wrong guesses)",
                        True, (255, 255, 255)
                    ),
                    (150, 660)
                ) # display the amount of error and the letters used

                if self.HasLost(): # if lost exit the loop without setting won to True
                    break
                self.won = self.HasWon() # if won exit the loop

                w: str = " ".join(self.currentWord) # display the word the player manage to create so far
                self.display.window.blit(
                    self.display.font.render(f"Your word is {w}", True, (255, 255, 255)),
                    (800,200)
                    )

                self.display.Draw() # render everything (use of a class on order to handle resizing easily)

            if self.won: # if exited loop cah won
                background: pg.surface.Surface = self.images["win"]
                txt1: pg.surface.Surface = self.display.font.render(f"\"{self.word}\"  Congrats you won the game", True, (255, 255, 255))
            else:
                background: pg.surface.Surface = self.images["loss"]
                txt1: pg.surface.Surface = self.display.font.render(f"You lost. The word was \"{self.word}\"", True, (255, 255, 255))
            txt2: pg.surface.Surface = self.display.font.render("Press Esc to exit", True, (255, 255, 255))
            txt3: pg.surface.Surface = self.display.font.render("Press the length of the next word you want to play with (3 - 9)", True, (255, 255, 255))
            txt4: pg.surface.Surface = self.display.font.render("Press \"?\" for the translation of the word", True, (255, 255, 255))

            initialYPosition: int = 500
            timer: int = 0

            while self.running: # alternate loop for between games
                self.clock.tick(60)
                self.display.window.blit(background, (0, 0))
                self.display.window.blit(txt1, (650, 200))
                yPosition: float = initialYPosition + sin(timer) * 10 # for the text to move up and down
                self.display.window.blit(txt2, (500, yPosition))
                self.display.window.blit(txt3, (200, yPosition + 50))
                self.display.window.blit(txt4, (350, yPosition + 100))
                timer += 0.05
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            pg.quit()
                            sys.exit()
                        elif event.key in self.keyToLength.keys():
                            self.wordLength = self.keyToLength[event.key] # select the next word's length
                            self.running = False # exit the alternate loop
                        elif event.key == pg.K_COMMA: # same key as "?" -> search the translation
                            webbrowser.open(f"https://www.deepl.com/translator#en/fr/{self.word}") # the best translator :)
                self.display.Draw() # render everything

    def PlaceGuess(self, guess: str) -> bool:

        if len(guess) != 1: # should not occur
            raise AttributeError # would trigger InvalidGuess (outside the func)

        if guess in self.usedletters:
            raise NameError # would trigger AlreadyUsedLetter (outside the func)

        self.usedletters.append(guess)
        if guess in self.word:
            for idx in self.GetOccurencesOf(guess): # fill in the blank(s) associated with the current guess
                self.currentWord[idx] = guess
            return True

        self.wrongGuesses += 1
        return False

    def HasLost(self) -> bool:
        return self.wrongGuesses == self.maxWrongGuesses

    def HasWon(self) -> bool:
        return self.word == "".join(self.currentWord)

    def GetOccurencesOf(self, char: str) -> Generator[int, None, None]:
        for idx in range(len(self.word)):
            if char == self.word[idx]:
                yield idx

    def SelectNewWord(self) -> None:
        # clamp the requested word length
        # should nt happen tho
        if self.wordLength > 9: # longest words in the list
            self.wordLength = 9
        if self.wordLength < 3: # shortest words in the list
            self.wordLength = 3
        self.word = Words.Pick(self.wordLength)
        self.currentWord = ["_" for _ in range(self.wordLength)]

    def SplashScreen(self) -> None: # staring screen
        startButton: pg.rect.Rect = pg.rect.Rect((self.display.W // 2 - 250, self.display.H // 2 - 100), (500, 200))
        newLengthButton: pg.rect.Rect = pg.rect.Rect((self.display.W // 2 - 350, self.display.H // 2 + 150), (700, 100))

        title: pg.surface.Surface = self.display.titleFont.render("The hangman", True, (255, 255, 255))
        titleRect: pg.rect.Rect = title.get_rect(center=(self.display.W // 2, 150))
        
        txt: pg.surface.Surface = self.display.titleFont.render("Start", True, (255, 255, 255))
        txtRect: pg.rect.Rect = txt.get_rect(center=(self.display.W // 2, self.display.H // 2))

        lengthButtonTxt: pg.surface.Surface = self.display.titleFont.render("Choose word's length", True, (255, 255, 255))
        lengthButtonTxtRect: pg.rect.Rect = lengthButtonTxt.get_rect(center=(self.display.W // 2, self.display.H // 2 + 200))

        while True:

            mousePos: tuple[int, int] = self.display.AdjustPos(pg.mouse.get_pos())
            mouse: tuple[bool, bool, bool] = pg.mouse.get_pressed()

            for event in pg.event.get():

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()

                    elif event.key == pg.K_SPACE:
                        return # exit the function to start the game

            if startButton.collidepoint(mousePos) and mouse[0]:
                return # exit the function to start the game
            elif newLengthButton.collidepoint(mousePos) and mouse[0]:
                self.ChooseLength() # exit the function to start the game

            self.display.window.blit(self.images["0"], (0, 0))
            pg.draw.rect(self.display.window, (255, 255, 255), startButton, 3, 5)
            pg.draw.rect(self.display.window, (255, 255, 255), newLengthButton, 3, 5)
            self.display.window.blit(txt, txtRect)
            self.display.window.blit(title, titleRect)
            self.display.window.blit(lengthButtonTxt, lengthButtonTxtRect)

            self.display.Draw()

    def ChooseLength(self): # menu for choosing word length
        buttonsRect = [pg.rect.Rect( (i * 175 + 100, self.display.H // 2), (50, 50) ) for i in range(7)]

        title = self.display.font.render("Choose the amount of letter you wanna play with", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.display.W // 2,250))
        
        while True:

            mousePos = self.display.AdjustPos(pg.mouse.get_pos())
            mouse = pg.mouse.get_pressed()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    
                    elif event.key == pg.K_SPACE: return # exit the function without changing the wanted length

                if mouse[0]:
                    # iterate over each button and their value (idx)
                    for idx, rect in enumerate(buttonsRect, 3): # enumerate link the iterable with an idx
                        if rect.collidepoint(mousePos):
                            self.wordLength = idx
                            return # exit

            self.display.window.blit(self.images["0"], (0, 0))
            self.display.window.blit(title, title_rect)
            
            for idx, rect in enumerate(buttonsRect, 3): # draw every button and the digit on it
                if idx == self.wordLength: # highlight this button as it s the current word's length
                    surf = pg.surface.Surface([50, 50])
                    surf.fill((0, 255, 0))
                    surf_rect = surf.get_rect(center=rect.center)
                    self.display.window.blit(surf, surf_rect)
                pg.draw.rect(self.display.window, (255, 255, 255), rect, 3, 5)
                txt = self.display.titleFont.render(str(idx), True, (255, 255, 255))
                txtRect = txt.get_rect(center=rect.center)
                self.display.window.blit(txt, txtRect)

            self.display.Draw()

if __name__ == "__main__":
    Game().RunOnDisplay()