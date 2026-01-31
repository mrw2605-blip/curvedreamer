import pygame
from game import Game


class App:
    '''
    Denne klassen styrer spillvinduet
    '''

    def __init__(self, width=1280, height=720):
        pygame.init()

        self.WIDTH = width
        self.HEIGHT = height

        self.game = Game()

        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT),
            pygame.RESIZABLE | pygame.DOUBLEBUF
        )

        pygame.display.set_caption("CurveFever")
        self.clock = pygame.time.Clock()
        self.running = True

        self.refresh_rate = pygame.display.get_current_refresh_rate() or 60

        # alpha surface
        self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        self.canvas.fill((0, 0, 0, 0)) # transparent
    
    
    def run(self):
        while self.running:
            dt = self.clock.tick(self.refresh_rate) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
            
        pygame.quit()

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                self.WIDTH, self.HEIGHT = event.w, event.h
                self.screen = pygame.display.set_mode(
                    (self.WIDTH, self.HEIGHT),
                    pygame.RESIZABLE | pygame.DOUBLEBUF
                )

                # Make canvas the same size
                old = self.canvas
                self.canvas = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
                self.canvas.fill((0, 0, 0, 0))
                self.canvas.blit(old, (0, 0))

                self.game.resize((self.WIDTH, self.HEIGHT))

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

        self.game.handle_events(events)


    def update(self, dt):
        self.game.update(dt)

    def draw(self):
        self.screen.fill((20, 20, 25))
        self.canvas.fill((0, 0, 0, 0))

        self.game.draw(self.canvas)

        # Copy canvas surface to screen
        self.screen.blit(self.canvas, (0, 0))

        pygame.display.flip()




if __name__ == "__main__":
    game_window = App()
    game_window.run()
