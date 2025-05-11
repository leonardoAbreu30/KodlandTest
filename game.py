import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 600

menu_active = True
music_on = True
sound_on = True
game_active = False
win_active = False

goal = Actor('goal_flag', (750, 545))

hero = Actor('hero_idle_1', (50, 500))
hero.vx = 0
hero.vy = 0
hero.on_ground = True
hero.direction = 'right'

platforms = [
    # Ground layer
    Rect((0, 580), (800, 20)),
    
    Rect((100, 480), (50, 50)),
    
    # Upper left structure
    Rect((200, 420), (50, 50)),
    Rect((250, 420), (50, 50)),
    Rect((300, 420), (50, 50)),
    Rect((350, 420), (50, 50)),
    Rect((400, 370), (50, 50)),
    
    # Mid right floating platforms (above the spikes in image)
    Rect((525, 380), (50, 50)),
    Rect((600, 470), (50, 50)),
    
]

enemies = [Actor('enemy', (700, 565))]
enemy2 = Actor('enemy', (210, 405)) 
enemy2.direction = 'right'
enemy2.patrol_min_x = 220
enemy2.patrol_max_x = 380
enemy2.dead = False
enemy2.death_timer = 0
enemies.append(enemy2)

enemies[0].direction = 'left'

total_frames = 2
idle_anim = {
    'right': ['hero_idle_1', 'hero_idle_2'],
    'left': ['hero_idle_1_left', 'hero_idle_2_left']
}
walk_anim = {
    'right': ['hero_walk_1', 'hero_walk_2'],
    'left': ['hero_walk_1_left', 'hero_walk_2_left']
}
jump_anim = {
    'right': ['hero_jump'],
    'left': ['hero_jump_left']
}
enemy_walk_anim = {
    'right': ['enemy_walk_1', 'enemy_walk_2'],
    'left': ['enemy_walk_1_left', 'enemy_walk_2_left']
}

frame = 0
frame_delay = 5
frame_counter = 0

start_button = Rect((300, 200), (200, 50))
exit_button = Rect((300, 300), (200, 50))
sound_button = Rect((300, 400), (200, 50))

# if music_on:
#     music.play('bg_music')

def update():
    global menu_active, game_active, frame, frame_counter

    if menu_active:
        return

    if game_active:
        keys = keyboard
        hero.vx = 0
        if hero.colliderect(goal):
            game_win()

        if keys.left:
            hero.vx = -4
            hero.direction = 'left'
        elif keys.right:
            hero.vx = 4
            hero.direction = 'right'

        if keys.up and hero.on_ground:
            hero.vy = -10
            hero.on_ground = False

        hero.vy += 0.5
        if hero.vy > 10:
            hero.vy = 10

        hero.x += hero.vx
        hero.y += hero.vy

        for plat in platforms:
            if hero.colliderect(plat) and hero.vy >= 0:
                hero.y = plat.top - hero.height / 2
                hero.vy = 0
                hero.on_ground = True

        frame_counter += 1
        if frame_counter >= frame_delay:
            frame = (frame + 1) % total_frames
            frame_counter = 0

        if not hero.on_ground:
            hero.image = jump_anim[hero.direction][0]
        elif hero.vx != 0:
            hero.image = walk_anim[hero.direction][frame]
        else:
            hero.image = idle_anim[hero.direction][frame]

        for enemy in enemies[:]:
            if hasattr(enemy, 'dead') and enemy.dead:
                enemy.death_timer -= 1
                if enemy.death_timer <= 0:
                    enemies.remove(enemy)
                    continue
            if not hasattr(enemy, 'dead') or not enemy.dead:
                # Enemy logic
                if hasattr(enemy, 'patrol_min_x') and hasattr(enemy, 'patrol_max_x'):
                    # Patrolling enemy
                    if enemy.direction == 'right':
                        enemy.x += 1
                        if enemy.x >= enemy.patrol_max_x:
                            enemy.direction = 'left'
                    else:
                        enemy.x -= 1
                        if enemy.x <= enemy.patrol_min_x:
                            enemy.direction = 'right'
                else:
                    # Regular enemy moves left
                    enemy.x -= 1
                    enemy.direction = 'left'

            if enemy.image != 'enemy_dead':
                enemy.image = enemy_walk_anim[enemy.direction][frame]

            enemy_hitbox = Rect(enemy.x - 15, enemy.y - 25, 30, 50)
            hero_hitbox = Rect(hero.x - 15, hero.y - 25, 30, 50)
            enemy_head_hitbox = Rect(enemy.x - 15, enemy.y - 40, 30, 10)

            if enemy_head_hitbox.colliderect(hero_hitbox) and hero.vy > 0:
                enemy.image = 'enemy_dead'
                enemy.dead = True
                enemy.death_timer = 20
                hero.vy = -7
            elif enemy_hitbox.colliderect(hero_hitbox):
                game_over()


def draw():
    screen.clear()
    if win_active:
        screen.draw.text("You Win!", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="yellow")
        return
    if menu_active:
        screen.draw.text("Platformer Game", center=(WIDTH/2, 100), fontsize=50)
        screen.draw.filled_rect(start_button, "green")
        screen.draw.text("Start", center=start_button.center, fontsize=30)
        screen.draw.filled_rect(exit_button, "red")
        screen.draw.text("Exit", center=exit_button.center, fontsize=30)
        screen.draw.filled_rect(sound_button, "blue")
        sound_text = "Sound: ON" if sound_on else "Sound: OFF"
        screen.draw.text(sound_text, center=sound_button.center, fontsize=30)
    else:
        for plat in platforms:
            screen.draw.filled_rect(plat, "brown")

        hero.draw()
        goal.draw()

        for enemy in enemies:
            enemy.draw()

def on_mouse_down(pos):
    global menu_active, game_active, music_on, sound_on
    if menu_active:
        if start_button.collidepoint(pos):
            menu_active = False
            game_active = True
        elif exit_button.collidepoint(pos):
            exit()
        elif sound_button.collidepoint(pos):
            sound_on = not sound_on
            if sound_on:
                music.play('bg_music')
            else:
                music.stop()

def game_win():
    global game_active, win_active, menu_active
    game_active = False
    win_active = True
    menu_active = False

def game_over():
    global menu_active, game_active
    menu_active = True
    game_active = False
    hero.x, hero.y = 100, 500
    hero.vy = 0
    for enemy in enemies:
        enemy.x, enemy.y = 700, 565
        enemy.direction = 'left'

pgzrun.go()
