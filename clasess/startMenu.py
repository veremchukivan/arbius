import sys
import pygame

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.running = True

    def display_menu(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Стартове меню", True, (255, 255, 255))
        play_button = self.font.render("Почати гру", True, (255, 255, 255))
        exit_button = self.font.render("Вийти", True, (255, 255, 255))

        title_rect = title.get_rect(center=(self.screen.get_width() /2 , self.screen.get_height() / 2 - 100))
        play_button_rect = play_button.get_rect(center=(self.screen.get_width() /2 , self.screen.get_height() / 2 ))
        exit_button_rect = exit_button.get_rect(center=(self.screen.get_width() /2 , self.screen.get_height() / 2 + 100))

        self.screen.blit(title, title_rect)
        self.screen.blit(play_button, play_button_rect)
        self.screen.blit(exit_button, exit_button_rect)

        pygame.display.flip()

        return play_button_rect, exit_button_rect

    def handle_events(self):
        play_button_rect, exit_button_rect = self.display_menu()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button_rect.collidepoint(event.pos):
                        self.running = False  # Перехід до гри
                    elif exit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()