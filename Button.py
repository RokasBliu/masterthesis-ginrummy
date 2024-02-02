import pygame

class Button(object):
    def __init__(self, name, width, height, color=(255,255,255), font_color=(0,0,0)):
        self.name = name
        self.width = width
        self.height = height
        self.color = color
        self.font_color = font_color
        self.rect = None

    def draw(self, window, xpos, ypos):
        self.rect = pygame.draw.rect(window, self.color, pygame.Rect(xpos, ypos, self.width, self.height))

        # Draw button border
        pygame.draw.line(window, (0, 0, 0), (xpos, ypos), (xpos + self.width, ypos), width=1)
        pygame.draw.line(window, (0, 0, 0), (xpos, ypos), (xpos, ypos + self.height), width=1)
        pygame.draw.line(window, (0, 0, 0), (xpos + self.width, ypos), (xpos + self.width, ypos + self.height), width=1)
        pygame.draw.line(window, (0, 0, 0), (xpos, ypos + self.height), (xpos + self.width, ypos + self.height), width=1)

        # Draw text
        my_font = pygame.font.SysFont('Comic Sans MS', self.height - 4)
        button_text = my_font.render(self.name, False, self.font_color)
        window.blit(button_text, (xpos + (self.width / 2 - button_text.get_width() / 2), ypos + (self.height / 2 - button_text.get_height() / 2)))

        
    def collidepoint(self, point):
        return self.rect.collidepoint(point)

    def __repr__(self):
        return f"{self.name} button"
    
    def __eq__(self, other: object) -> bool:
        return other != None and self.name == other.name
    