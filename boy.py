from transitions import Machine
from pico2d import (
    SDLK_LEFT,
    SDLK_RIGHT,
    SDL_KEYDOWN,
    SDL_KEYUP,
    get_time,
    load_image,
)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.idle_started_at = get_time()
        self.last_update_at = get_time()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                ['sleep', 'IDLE', 'SLEEP'],
                ['wake', 'SLEEP', 'IDLE'],
                ['run', 'IDLE', 'RUN'],
                ['stop', 'RUN', 'IDLE'],
            ],
        )

    def handle_event(self, event):
        current_time = get_time()
        delta_time = current_time - self.last_update_at
        self.last_update_at = current_time
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            if current_time - self.idle_started_at >= 5:
                self.sleep()
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.face_dir * 200 * delta_time

    def update(self):
        if self.state == 'SLEEP' and event.type == SDL_KEYDOWN:
            self.wake()
            self.idle_started_at = get_time()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.face_dir = -1 if event.key == SDLK_LEFT else 1
            if self.state == 'IDLE':
                self.run()
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            if self.state == 'RUN':
                self.stop()
                self.idle_started_at = get_time()

    def draw(self):
        source_y = 300 if self.face_dir == 1 else 200
        self.image.clip_draw(self.frame * 100, source_y, 100, 100, self.x, self.y)
