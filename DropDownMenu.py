import pygame

class DropDownMenu(object):
    def __init__(self, name, dropdown_list, width, height):
        self.name = name
        self.dropdown_list = dropdown_list
        self.is_open = False
        self.selected_item = dropdown_list[0] if dropdown_list else "..."
        self.width = width
        self.height = height
        self.main_rect = None
        self.dropdown_rects = []

    def draw(self, window, xpos, ypos, font_color=(0,0,0), main_color=(255,255,255), dropdown_color=(235,235,235)):
        self.dropdown_rects = []
        self.main_rect = pygame.draw.rect(window, main_color, pygame.Rect(xpos, ypos, self.width, self.height))
        my_font = pygame.font.SysFont('Comic Sans MS', self.height - 20)
        dropdown_text = my_font.render(self.selected_item, False, font_color)
        window.blit(dropdown_text, (xpos + (self.width / 2 - dropdown_text.get_width() / 2), ypos + (self.height / 2 - dropdown_text.get_height() / 2)))
        if self.is_open == True:
            for num, item in enumerate(self.dropdown_list):
                self.dropdown_rects.append(pygame.draw.rect(window, dropdown_color, pygame.Rect(xpos, ypos + (self.height * (num+1)), self.width, self.height)))
                dropdown_text = my_font.render(item, False, font_color)
                window.blit(dropdown_text, (xpos + (self.width / 2 - dropdown_text.get_width() / 2), ypos + (self.height * (num+1)) + (self.height / 2 - dropdown_text.get_height() / 2)))
        
    def process_click(self, point):
        if self.main_rect.collidepoint(point):
            self.is_open = not self.is_open
            return
        if self.is_open == True:
            for num, rect in enumerate(self.dropdown_rects):
                if rect.collidepoint(point):
                    self.selected_item = self.dropdown_list[num]
                    self.is_open = False

    def __repr__(self):
        return f"{self.name} dropdown list has the following list values: {self.dropdown_list}"
    
    def __eq__(self, other: object) -> bool:
        return other != None and self.name == other.name
    