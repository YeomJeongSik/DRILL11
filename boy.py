from transitions import Machine
from pico2d import load_image


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE'],
            initial='IDLE',
            auto_transitions=False,
        )

    def handle_event(self, event):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8

    def update(self):
        pass

    def draw(self):
        source_y = 300 if self.face_dir == 1 else 200
        self.image.clip_draw(self.frame * 100, source_y, 100, 100, self.x, self.y)
