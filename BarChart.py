import pygame

class BarChart(object):
    def __init__(self, name, width, height, xpos, ypos, xdata, ydata, padding):
        self.name = name
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.xdata = xdata
        self.ydata = ydata
        self.padding = padding
        self.bar_width = width / len(xdata)
        self.rects = []

    def draw(self, window, color=(0, 0, 0)):
        self.rects = []
        for num, x in enumerate(self.xdata):
            self.rects.append(pygame.draw.rect(window, color, pygame.Rect(self.xpos + self.bar_width * num, self.ypos + (self.height - self.height * (self.ydata[num] / max(self.ydata))), self.bar_width - self.padding, self.height * (self.ydata[num] / max(self.ydata)))))

    def collidepoint(self, point):
        xpoint, ypoint = point
        return xpoint >= self.xpos and xpoint <= (self.xpos + self.width) and ypoint >= self.ypos and ypoint <= (self.ypos + self.height)

    def move_ip(self, rel, x_min, x_max, y_min, y_max):
        x, y = rel
        if self.xpos + x >= x_min and self.xpos + self.width + x <= x_max:
            self.xpos += x
        if self.ypos + y >= y_min and self.ypos + self.height + y <= y_max:
            self.ypos += y

    def inflate(self, rel, max_width, max_height):
        offset_x, offset_y = rel
        if self.width + offset_x <= max_width and self.width + offset_x >= 100:
            self.width += offset_x
            self.bar_width = self.width / len(self.xdata)
        if self.height + offset_y <= max_height and self.height + offset_y >= 100:
            self.height += offset_y

    def __repr__(self):
        return f"{self.name}"
    
    def __eq__(self, other: object) -> bool:
        return other != None and self.name == other.name
    