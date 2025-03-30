import pygame as pg


class Display:
    # everything is handled with a fixed size then resized at draw time (allow the use of fullscreen regardless of the monitor size)
    def __init__(self) -> None:
        pg.init()
        self.W: int = 1280 # fixed width
        self.H: int = 720 # fixed height
        self.display: pg.surface.Surface = pg.display.set_mode((0, 0), pg.FULLSCREEN) # fullscreen display
        pg.display.set_caption("Hangman")
        self.NewDisplay() # fixed size display

        self.sizedDimension: tuple[int, int] = self.display.get_size() # fullscreen dimension

        self.font: pg.font.Font = pg.font.Font("font/Chalktastic-r78L.ttf", 24)
        self.titleFont: pg.font.Font = pg.font.Font("font/EraserRegular.ttf", 48)

    def NewDisplay(self) -> pg.surface.Surface: # reset the fixed size display (cah was resized and manipulated)
        self.window: pg.surface.Surface = pg.surface.Surface((self.W, self.H))

    def AdjustPos(self,mouse_XY : tuple[int,int]):
        # if im at (200,200) on my screen it may be (380,500) in computation coordinates due to resizing
        x, y = mouse_XY
        x /= (self.sizedDimension[0] / self.W)
        y /= (self.sizedDimension[1] / self.H)
        return x,y

    def UpdateDimensions(self) -> None: # update the wanted size
        self.sizedDimension = self.display.get_size()

    def Draw(self): # render
        self.window = pg.transform.scale(self.window, (self.sizedDimension)) # resize fixed size display to actual dimensions
        self.display.blit(self.window, (0, 0)) # blit it on the actual screen
        pg.display.update() # render
        self.NewDisplay() # new fixed size display



