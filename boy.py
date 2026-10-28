from transitions import Machine
from pico2d import (
    SDLK_a,
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
        self.pressed_directions = set()
        self.idle_started_at = get_time()
        self.last_update_at = get_time()
        self.autorun_started_at = get_time()
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP', 'AUTORUN'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                ['sleep', 'IDLE', 'SLEEP'],
                ['wake', 'SLEEP', 'IDLE'],
                ['run', 'IDLE', 'RUN'],
                ['stop', 'RUN', 'IDLE'],
                ['autorun', 'IDLE', 'AUTORUN'],
                ['finish_autorun', 'AUTORUN', 'IDLE'],
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
            self.x = max(50, min(750, self.x))
        elif self.state == 'AUTORUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.face_dir * 350 * delta_time
            if self.x >= 750:
                self.x = 750
                self.face_dir = -1
            elif self.x <= 50:
                self.x = 50
                self.face_dir = 1
            if get_time() - self.autorun_started_at >= 5:
                self.finish_autorun()
                self.idle_started_at = get_time()

    def update(self):
        if self.state == 'SLEEP' and event.type == SDL_KEYDOWN:
            if event.key in (SDLK_LEFT, SDLK_RIGHT):
                self.pressed_directions.add(event.key)
                self.face_dir = -1 if event.key == SDLK_LEFT else 1
                self.wake()
                self.run()
            else:
                self.wake()
            self.idle_started_at = get_time()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.pressed_directions.add(event.key)
            self.face_dir = -1 if event.key == SDLK_LEFT else 1
            if self.state == 'IDLE':
                self.run()
        elif self.state == 'IDLE' and event.type == SDL_KEYDOWN and event.key == SDLK_a:
            self.autorun_started_at = get_time()
            self.autorun()
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.pressed_directions.discard(event.key)
            if self.state == 'RUN' and not self.pressed_directions:
                self.stop()
                self.idle_started_at = get_time()

    def draw(self):
        source_y = 300 if self.face_dir == 1 else 200
        if self.state == 'SLEEP':
            self.image.clip_composite_draw(
                self.frame * 100,
                source_y,
                100,
                100,
                radians(90 if self.face_dir == 1 else -90),
                '',
                self.x,
                110,
                100,
                100,
            )
        else:
            self.image.clip_draw(self.frame * 100, source_y, 100, 100, self.x, self.y)
from math import radians
