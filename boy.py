from math import radians

from pico2d import (
    SDLK_a,
    SDLK_LEFT,
    SDLK_RIGHT,
    SDL_KEYDOWN,
    SDL_KEYUP,
    get_time,
    load_image,
)
from transitions import Machine


class Boy:
    SCREEN_WIDTH = 800
    HALF_WIDTH = 50
    GRASS_Y = 30
    GRASS_HEIGHT = 60
    SPRITE_HALF_HEIGHT = 50
    RUN_SPEED = 200
    AUTORUN_SPEED = 350
    AUTORUN_DURATION = 5

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
                ['cancel_autorun', 'AUTORUN', 'RUN'],
            ],
        )

    def update(self):
        current_time = get_time()
        delta_time = current_time - self.last_update_at
        self.last_update_at = current_time

        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            if current_time - self.idle_started_at >= 5:
                self.sleep()
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.face_dir * self.RUN_SPEED * delta_time
            self.x = max(self.HALF_WIDTH, min(self.SCREEN_WIDTH - self.HALF_WIDTH, self.x))
        elif self.state == 'AUTORUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.face_dir * self.AUTORUN_SPEED * delta_time
            if self.x >= self.SCREEN_WIDTH - self.HALF_WIDTH:
                self.x = self.SCREEN_WIDTH - self.HALF_WIDTH
                self.face_dir = -1
            elif self.x <= self.HALF_WIDTH:
                self.x = self.HALF_WIDTH
                self.face_dir = 1
            if current_time - self.autorun_started_at >= self.AUTORUN_DURATION:
                self.finish_autorun()
                self.idle_started_at = current_time

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if self.state == 'SLEEP':
                if event.key in (SDLK_LEFT, SDLK_RIGHT):
                    self.pressed_directions.add(event.key)
                    self.face_dir = -1 if event.key == SDLK_LEFT else 1
                    self.wake()
                    self.run()
                else:
                    self.wake()
                self.idle_started_at = get_time()
            elif self.state == 'IDLE' and event.key == SDLK_a:
                self.autorun_started_at = get_time()
                self.autorun()
            elif self.state == 'AUTORUN' and event.key in (SDLK_LEFT, SDLK_RIGHT):
                self.pressed_directions.add(event.key)
                self.face_dir = -1 if event.key == SDLK_LEFT else 1
                self.cancel_autorun()
            elif event.key in (SDLK_LEFT, SDLK_RIGHT):
                self.pressed_directions.add(event.key)
                self.face_dir = -1 if event.key == SDLK_LEFT else 1
                if self.state == 'IDLE':
                    self.run()
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            self.pressed_directions.discard(event.key)
            if self.state == 'RUN':
                if self.pressed_directions:
                    remaining_key = next(iter(self.pressed_directions))
                    self.face_dir = -1 if remaining_key == SDLK_LEFT else 1
                else:
                    self.stop()
                    self.idle_started_at = get_time()

    def draw(self):
        draw_y = (
            (self.GRASS_Y + self.GRASS_HEIGHT / 2 + self.SPRITE_HALF_HEIGHT) / 2
            if self.state == 'SLEEP'
            else self.y
        )
        if self.state in ('RUN', 'AUTORUN'):
            source_y = 100 if self.face_dir == 1 else 0
        else:
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
                draw_y,
                100,
                100,
            )
        else:
            draw_size = 150 if self.state == 'AUTORUN' else 100
            self.image.clip_draw(
                self.frame * 100,
                source_y,
                100,
                100,
                self.x,
                draw_y,
                draw_size,
                draw_size,
            )
