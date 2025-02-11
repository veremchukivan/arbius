import sys
import pygame

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)

    def display_menu(self):
        """Малює екран паузи"""
        pause_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 150))  # Напівпрозорий фон
        self.screen.blit(pause_overlay, (0, 0))

        title = self.font.render("Pause", True, (255, 255, 255))
        continue_button = self.font.render("resume", True, (255, 255, 255))
        exit_button = self.font.render("exit", True, (255, 255, 255))

        title_rect = title.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 -100))
        continue_button_rect = continue_button.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        exit_button_rect = exit_button.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 100))

        self.screen.blit(title, title_rect)
        self.screen.blit(continue_button, continue_button_rect)
        self.screen.blit(exit_button, exit_button_rect)

        pygame.display.flip()

        return continue_button_rect, exit_button_rect

    def handle_events(self):
        """Обробка подій меню паузи"""
        continue_button_rect, exit_button_rect = self.display_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button_rect.collidepoint(event.pos):
                        return "resume"
                    elif exit_button_rect.collidepoint(event.pos):
                        return "exit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        return "resume"
