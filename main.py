import pygame
from checkersA.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED
from checkersA.game import Game

def main():
    '''Función principal que ejecuta el juego.'''
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')
    clock = pygame.time.Clock()
    game = Game(WIN)  # Inicializar el juego

    
    font = pygame.font.SysFont('comicsans', 40, bold=True)

    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  #obtener la posición del mouse al hacer clic
                row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                game.select(row, col)

        game.update()

        winner = game.board.winner()
        if winner:
            winner_text = f"{winner} Wins!"
            text_surface = font.render(winner_text, True, pygame.Color('Gold'))
            WIN.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, (HEIGHT - text_surface.get_height()) // 2))
            pygame.display.update()
            pygame.time.wait(500)  # Esperar antes de cerrar el juego
            run = False

        pygame.display.update()

    # Keep the window open until the user closes it
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
