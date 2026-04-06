import pgzrun
WIDTH = 256 * 4
HEIGHT = 256 * 3
TITLE = "Run Kitty Run"
GROUND_Y = HEIGHT - 64
SCROLL_SPEED = 1.5
sound_on = True
sky_offset = 0
clouds_offset = 0
trees_offset = 0
floor_offset = 0
enemy_timer = 0
enemy_frame = 0
enemy_state = "idle"
player_timer = 0
space_was_down = False
music_started = False
win_sound_played = False
lose_sound_played = False
ladybug = Actor("ladybugrest", (WIDTH + 100, GROUND_Y))
snail = Actor("snailrest", (WIDTH + 300, GROUND_Y))
player = Actor("kittyidle", (200, GROUND_Y))
player.vy = 0
player.on_ground = True
player.facing = 1
gamestate = "menu"
did_win = False
enemies_killed = 0
def play_sound(name):
    if sound_on:
        getattr(sounds, name).play()
def start_music():
    global music_started
    if sound_on and not music_started:
        sounds.bgmusic.play(-1)
        music_started = True
def stop_music():
    global music_started
    sounds.bgmusic.stop()
    music_started = False
def reset_game():
    global did_win, enemies_killed
    global sky_offset, clouds_offset, trees_offset, floor_offset
    global enemy_timer, enemy_frame, enemy_state
    global player_timer, win_sound_played, lose_sound_played
    did_win = False
    enemies_killed = 0
    sky_offset = 0
    clouds_offset = 0
    trees_offset = 0
    floor_offset = 0
    enemy_timer = 0
    enemy_frame = 0
    enemy_state = "idle"
    player_timer = 0
    win_sound_played = False
    lose_sound_played = False
    player.x = 200
    player.bottom = GROUND_Y
    player.vy = 0
    player.on_ground = True
    player.facing = 1
    player.flip_x = False
    player.image = "kittyidle"
    ladybug.x = WIDTH + 100
    ladybug.bottom = GROUND_Y
    ladybug.image = "ladybugrest"
    snail.x = WIDTH + 300
    snail.bottom = GROUND_Y
    snail.image = "snailrest"

def draw():
    if gamestate == "menu":
        screen.clear()
        screen.draw.text("Run Kitty Run!!!", topleft=(10, 10), fontsize=60, color="black")
        screen.draw.text("Press SPACE to Start", center=(WIDTH / 2, HEIGHT / 2), fontsize=60, color="green")
    elif gamestate == "playing":
        screen.clear()
        for x in range(-256, WIDTH + 256, 256):
            sky = Actor("sky", (x + sky_offset, 128))
            sky.draw()
        for x in range(-256, WIDTH + 256, 256):
            clouds = Actor("clouds", (x + clouds_offset, 128 + 256))
            clouds.draw()
        for x in range(-256, WIDTH + 256, 256):
            trees = Actor("trees", (x + trees_offset, 128 + 512))
            trees.draw()
        for x in range(-64, WIDTH + 64, 64):
            floor = Actor("floor", (x + floor_offset, HEIGHT - 32))
            floor.draw()
        player.draw()
        ladybug.draw()
        snail.draw()
        screen.draw.text("Run Kitty Run!!!", topleft=(10, 10), fontsize=60, color="black")
        screen.draw.text("Kill 2 enemies to pass the right border to win",
                         center=(WIDTH / 2, 80), fontsize=34, color="yellow")
    elif gamestate == "gameover":
        screen.clear()
        screen.draw.text("Game Over", center=(WIDTH / 2, HEIGHT / 2), fontsize=80, color="red")
        screen.draw.text("Press SPACE to restart", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=40, color="green")

    elif gamestate == "win":
        screen.clear()
        screen.draw.text("YOU WIN!", center=(WIDTH / 2, HEIGHT / 2), fontsize=80, color="green")
        screen.draw.text("Press SPACE to play again", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=40, color="white")
def update():
    global gamestate, did_win, enemies_killed,sky_offset, clouds_offset, trees_offset, floor_offset, enemy_timer, enemy_frame, enemy_state, player_timer, space_was_down, win_sound_played, lose_sound_played,space_pressed
    space_pressed = keyboard.space and not space_was_down
    if gamestate == "menu" and space_pressed:
        gamestate = "playing"
        reset_game()
        start_music()
        space_was_down = keyboard.space
        return
    if gamestate == "gameover" and space_pressed:
        gamestate = "menu"
        space_was_down = keyboard.space
        return
    if gamestate == "win" and space_pressed:
        gamestate = "menu"
        space_was_down = keyboard.space
        return
    if gamestate != "playing":
        space_was_down = keyboard.space
        return
    sky_offset += 0.5
    clouds_offset += 1
    trees_offset += 2
    floor_offset += 3
    if sky_offset >= 256:
        sky_offset -= 256
    if clouds_offset >= 256:
        clouds_offset -= 256
    if trees_offset >= 256:
        trees_offset -= 256
    if floor_offset >= 64:
        floor_offset -= 64
    player.vy += 0.8
    player.y += player.vy
    if player.bottom >= GROUND_Y:
        player.bottom = GROUND_Y
        player.vy = 0
        player.on_ground = True
    else:
        player.on_ground = False
    if space_pressed and player.on_ground:
        player.vy = -12
        player.on_ground = False
        play_sound("jumpingsound")
    if keyboard.left:
        player.x -= 5
        player.facing = -1
    if keyboard.right:
        player.x += 5
        player.facing = 1
    player.x -= SCROLL_SPEED
    ladybug.x -= SCROLL_SPEED
    snail.x -= SCROLL_SPEED
    player.flip_x = player.facing == -1
    if player.x < 10:
        gamestate = "gameover"
        if sound_on and not lose_sound_played:
            play_sound("losingsound")
            lose_sound_played = True
        space_was_down = keyboard.space
        return
    if player.x > WIDTH and did_win:
        gamestate = "win"
        if sound_on and not win_sound_played:
            play_sound("wonsound")
            win_sound_played = True
        space_was_down = keyboard.space
        return
    player_timer += 1
    if keyboard.left or keyboard.right:
        if player_timer > 8:
            player_timer = 0
            if player.image == "kittywalka":
                player.image = "kittywalkb"
            else:
                player.image = "kittywalka"
    else:
        if player.on_ground:
            player.image = "kittyidle"
    if not player.on_ground:
        player.image = "kittyjump"
    enemy_timer += 1
    if enemy_timer > 120:
        enemy_timer = 0
        if enemy_state == "idle":
            enemy_state = "walk"
        else:
            enemy_state = "idle"
    if enemy_state == "walk":
        enemy_frame += 1
        if enemy_frame > 15:
            enemy_frame = 0
            if ladybug.image == "ladybugwalka":
                ladybug.image = "ladybugwalkb"
            else:
                ladybug.image = "ladybugwalka"
            if snail.image == "snailwalka":
                snail.image = "snailwalkb"
            else:
                snail.image = "snailwalka"
        if ladybug.x < player.x:
            ladybug.x += 3
        else:
            ladybug.x -= 3
        if snail.x < player.x:
            snail.x += 1.5
        else:
            snail.x -= 1.5
    else:
        ladybug.image = "ladybugrest"
        snail.image = "snailrest"
    ladybug.bottom = GROUND_Y
    snail.bottom = GROUND_Y
    if player.colliderect(ladybug) and player.vy > 0:
        ladybug.x = -1000
        enemies_killed += 1
    if player.colliderect(snail) and player.vy > 0:
        snail.x = -1000
        enemies_killed += 1
    if enemies_killed >= 2:
        did_win = True
    if (player.colliderect(ladybug) or player.colliderect(snail)) and player.vy <= 0:
        gamestate = "gameover"
        if sound_on and not lose_sound_played:
            play_sound("losingsound")
            lose_sound_played = True
    space_was_down = keyboard.space
pgzrun.go()