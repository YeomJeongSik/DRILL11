from pico2d import *
from boy import Boy
from grass import Grass


def handle_events():
    global running

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)


def reset_world():
    global world, boy

    world = [Grass()]
    boy = Boy()
    world.append(boy)


def update_world():
    for game_object in world:
        game_object.update()


def render_world():
    clear_canvas()
    for game_object in world:
        game_object.draw()
    update_canvas()


running = True
open_canvas()
reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
close_canvas()
