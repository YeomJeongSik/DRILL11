from pico2d import load_image


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.image = load_image('animation_sheet.png')

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 300, 100, 100, self.x, self.y)
