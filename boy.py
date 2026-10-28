from transitions import Machine
from pico2d import get_time, load_image


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.idle_started_at = get_time()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[['sleep', 'IDLE', 'SLEEP']],
        )

    def handle_event(self, event):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            if get_time() - self.idle_started_at >= 5:
                self.sleep()

    def update(self):
        pass

    def draw(self):
        source_y = 300 if self.face_dir == 1 else 200
        self.image.clip_draw(self.frame * 100, source_y, 100, 100, self.x, self.y)
