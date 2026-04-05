import pygame
import sys
import pygame.mixer
pygame.init()
pygame.mixer.init() # Initialize sound engine

# --- GAME Screen ---
pygame.display.set_caption('Run kitty run')
screen = pygame.display.set_mode((900, 500))
Running = True

# --- LOAD ASSETS (Images) ---
Sky_surface = pygame.image.load("Theme\sky.png").convert()
ground_surface1 = pygame.image.load("Theme\ground1.png").convert()
ground_surface2 = pygame.image.load("Theme\ground2.png").convert()
touchable_surface = pygame.image.load("Theme\Touchableground.png").convert_alpha()

# Kitty Animations
kitty_front = pygame.image.load("Kitty\kittyfront.png").convert_alpha()
kitty_idle = pygame.image.load("Kitty\kittyidle.png").convert_alpha()
kitty_walkA = pygame.image.load("Kitty\kittywalkA.png").convert_alpha()
kitty_walkB = pygame.image.load("Kitty\kittywalkB.png").convert_alpha()
kitty_jump = kitty_front

# Enemy Animations
ladybug_rest = pygame.image.load("Enemies\ladybugrest.png").convert_alpha()
ladybug_walkA = pygame.image.load("Enemies\ladybugwalka.png").convert_alpha()
ladybug_walkB = pygame.image.load("Enemies\ladybugwalkb.png").convert_alpha()

snail_rest = pygame.image.load("Enemies\snailrest.png").convert_alpha()
snail_walkA = pygame.image.load("Enemies\snailwalka.png").convert_alpha()
snail_walkB = pygame.image.load("Enemies\snailwalkb.png").convert_alpha()

# --- LOAD ASSETS (Audio) ---
pygame.mixer.music.load("AUDIO\BackGroundmusic.wav")
snd_jump = pygame.mixer.Sound("AUDIO\Jumpbro.wav")
snd_lose = pygame.mixer.Sound("AUDIO\lostbro.wav")
snd_win = pygame.mixer.Sound("AUDIO\wonbro.wav")
snd_start = pygame.mixer.Sound("AUDIO\soundafterwepress_start.wav")

# UI Fonts
title_font = pygame.font.Font("freesansbold.ttf", 35)
gamenametext_surface = title_font.render("Run kitty run !", True, 'darkblue').convert_alpha()

# --- GAME VARIABLES ---
clock = pygame.time.Clock()
game_state = "menu"
sound_on = True
start_time = 0
survival_time = 0
end_reason = ""

# Kitty Mechanics
kitty_speed = 220
kitty_drag = 30
gravity = 1100
jump_strength = 550
is_jumping = False
kitty_y_vel = 0
kitty_facing_right = True

kitty_x = 200
kitty_y = screen.get_height() - (touchable_surface.get_height() + kitty_front.get_height())
ground_y_level = kitty_y 

# Enemy Mechanics
enemy_speed = 80
#snail
snail_x = -200
snail_y = screen.get_height() - (touchable_surface.get_height() + snail_rest.get_height())
snail_dead = False
#ladybug
ladybug_x = screen.get_width() + 100
ladybug_y = screen.get_height() - (touchable_surface.get_height() + ladybug_rest.get_height())
ladybug_dead = False

# State Mechanics
enemy_state_timer = 0
snail_state = "walk"
ladybug_state = "rest"

# Animation Timers
anim_timer = 0
anim_frame = 0

# Parallax Scrolling
sky_scroll = 0
ground_scroll = 0
touch_scroll = 0

# --- GAME LOOP ---
while Running:
    delta_time = clock.tick(60) / 1000.0
    delta_time = max(0.01, min(delta_time, 0.1))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "menu":
            mouse_pos = pygame.mouse.get_pos()
            if start_rect.collidepoint(mouse_pos):
                if sound_on:
                    snd_start.play()
                    pygame.mixer.music.play(-1) # Loop background music
                game_state = "playing"
                start_time = pygame.time.get_ticks()
            if sound_rect.collidepoint(mouse_pos):
                sound_on = not sound_on
            if exit_rect.collidepoint(mouse_pos):
                Running = False

    if game_state == "playing":
        
        # --- TIMERS & ANIMATIONS ---
        anim_timer += delta_time
        if anim_timer >= 0.2: # Switch animation frame every 0.2 seconds
            anim_timer = 0
            anim_frame = 1 
            if anim_frame == 0:
                anim_frame = 1 
            else :anim_frame = 0
            
        enemy_state_timer += delta_time
        if enemy_state_timer >= 3.0: # Swap enemy states every 3 seconds
            enemy_state_timer = 0
            if snail_state == "walk":
                snail_state = "rest"
                ladybug_state = "walk"
            else:
                snail_state = "walk"
                ladybug_state = "rest"

        # --- PARALLAX SCROLLING ---
        sky_scroll -= 15 * delta_time 
        ground_scroll -= 40 * delta_time
        touch_scroll -= 100 * delta_time 

        if sky_scroll <= -Sky_surface.get_width(): sky_scroll = 0
        if ground_scroll <= -ground_surface1.get_width(): ground_scroll = 0
        if touch_scroll <= -touchable_surface.get_width(): touch_scroll = 0

        # --- KITTY PHYSICS & CONTROLS ---
        kitty_x -= kitty_drag * delta_time
        keys = pygame.key.get_pressed()
        is_moving = False
        
        if keys[pygame.K_LEFT]:
            kitty_x -= kitty_speed * delta_time
            kitty_facing_right = False
            is_moving = True
        if keys[pygame.K_RIGHT]:
            kitty_x += kitty_speed * delta_time
            kitty_facing_right = True
            is_moving = True
            
        if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not is_jumping:
            if sound_on: snd_jump.play()
            kitty_y_vel = -jump_strength
            is_jumping = True

        kitty_y_vel += gravity * delta_time
        kitty_y += kitty_y_vel * delta_time

        if kitty_y >= ground_y_level:
            kitty_y = ground_y_level
            kitty_y_vel = 0
            is_jumping = False

        if not snail_dead and snail_state == "walk":
            if snail_x < kitty_x: snail_x += enemy_speed * delta_time 
            elif snail_x > kitty_x: snail_x -= enemy_speed * delta_time
            
        if not ladybug_dead and ladybug_state == "walk":
            if ladybug_x < kitty_x: ladybug_x += (enemy_speed + 20) * delta_time
            elif ladybug_x > kitty_x: ladybug_x -= (enemy_speed + 20) * delta_time

        # Kitty Image
        if is_jumping:
            current_kitty_img = kitty_jump
        elif is_moving:
            current_kitty_img = kitty_walkA if anim_frame == 0 else kitty_walkB
        else:
            current_kitty_img = kitty_front if anim_frame == 0 else kitty_idle

        # Snail Image
        if snail_state == "rest" or snail_dead:
            current_snail_img = snail_rest
        else:
            current_snail_img = snail_walkA if anim_frame == 0 else snail_walkB
            
        # Ladybug Image
        if ladybug_state == "rest" or ladybug_dead:
            current_ladybug_img = ladybug_rest
        else:
            current_ladybug_img = ladybug_walkA if anim_frame == 0 else ladybug_walkB

        # --- HITBOXES & COLLISION DETECTION (MARIO STOMP) ---
        kitty_rect = pygame.Rect(kitty_x, kitty_y, current_kitty_img.get_width(), current_kitty_img.get_height()).inflate(-20, -20)
        snail_rect = pygame.Rect(snail_x, snail_y, current_snail_img.get_width(), current_snail_img.get_height()).inflate(-15, -15)
        ladybug_rect = pygame.Rect(ladybug_x, ladybug_y, current_ladybug_img.get_width(), current_ladybug_img.get_height()).inflate(-15, -15)

        # Check Snail Collision
        if not snail_dead and kitty_rect.colliderect(snail_rect):
            # If kitty is falling AND hits the top half of the snail AND snail is walking
            if kitty_y_vel > 0 and kitty_rect.bottom < snail_rect.centery + 15 and snail_state == "walk":
                snail_dead = True
                kitty_y_vel = -jump_strength / 1.2 # Bounce off the enemy!
                if sound_on: snd_jump.play()
            else:
                # Got hit / Poisoned
                end_reason = "Kitty was poisoned by the Snail!"
                if sound_on: snd_lose.play()
                survival_time = (pygame.time.get_ticks() - start_time) // 1000
                game_state = "game_over"

        # Check Ladybug Collision
        if not ladybug_dead and kitty_rect.colliderect(ladybug_rect):
            if kitty_y_vel > 0 and kitty_rect.bottom < ladybug_rect.centery + 15 and ladybug_state == "walk":
                ladybug_dead = True
                kitty_y_vel = -jump_strength / 1.2 # Bounce!
                if sound_on: snd_jump.play()
            else:
                end_reason = "Kitty was poisoned by the Ladybug!"
                if sound_on: snd_lose.play()
                survival_time = (pygame.time.get_ticks() - start_time) // 1000
                game_state = "game_over"

        # --- BORDERS & WIN/LOSS CONDITIONS ---
        if kitty_x <= 0:
            end_reason = "Kitty ran outside the safe borders!"
            if sound_on: snd_lose.play()
            survival_time = (pygame.time.get_ticks() - start_time) // 1000
            game_state = "game_over"

        # Right Border Logic
        if kitty_x + current_kitty_img.get_width() >= screen.get_width():
            if snail_dead and ladybug_dead:
                # Win!
                end_reason = "Kitty escaped successfully!"
                if sound_on: snd_win.play()
                pygame.mixer.music.stop()
                survival_time = (pygame.time.get_ticks() - start_time) // 1000
                game_state = "game_over"
            else:
                # Block the right border if enemies are still alive
                kitty_x = screen.get_width() - current_kitty_img.get_width()

        # --- DRAWING THE GAME ---
        for x_pos in range(0, screen.get_width() + Sky_surface.get_width(), Sky_surface.get_width()):
            for y_pos in range(0, screen.get_height() - Sky_surface.get_height(), Sky_surface.get_height()): 
                screen.blit(Sky_surface, (x_pos + sky_scroll, y_pos))
        
        for x_pos in range(0, screen.get_width() + ground_surface1.get_width() + ground_surface2.get_width(), ground_surface1.get_width() + ground_surface2.get_width()):
            for y_pos in range(screen.get_height() - ground_surface1.get_height(), screen.get_height(), ground_surface1.get_height()): 
                screen.blit(ground_surface1, (x_pos + ground_scroll, y_pos))
                
        for x_pos in range(ground_surface2.get_width(), screen.get_width() + ground_surface1.get_width() + ground_surface2.get_width(), ground_surface1.get_width() + ground_surface2.get_width()): 
            for y_pos in range(screen.get_height() - ground_surface1.get_height(), screen.get_height(), ground_surface2.get_height()): 
                screen.blit(ground_surface2, (x_pos + ground_scroll, y_pos))

        for x_pos in range(0, screen.get_width() + touchable_surface.get_width(), touchable_surface.get_width()):
            for y_pos in range (screen.get_height() - touchable_surface.get_height(), screen.get_height(), touchable_surface.get_height()):
                screen.blit(touchable_surface, (x_pos + touch_scroll, y_pos))
        
        # Draw Kitty
        if not kitty_facing_right:
            current_kitty_img = pygame.transform.flip(current_kitty_img, True, False)
        screen.blit(current_kitty_img, (kitty_x, kitty_y))
        
        # Draw Snail (Dead icon vs Alive)
        if snail_dead:
            dead_snail = pygame.transform.scale(current_snail_img, (30, 30))
            dead_snail = pygame.transform.flip(dead_snail, False, True) # Upside down
            screen.blit(dead_snail, (20, screen.get_height() - 40)) # Trophies at bottom left
        else:
            # CHANGED > to < HERE
            if snail_x < kitty_x: # Flip enemy to face right if it is behind kitty
                current_snail_img = pygame.transform.flip(current_snail_img, True, False)
            screen.blit(current_snail_img, (snail_x, snail_y))
            
        # Draw Ladybug (Dead icon vs Alive)
        if ladybug_dead:
            dead_bug = pygame.transform.scale(current_ladybug_img, (30, 30))
            dead_bug = pygame.transform.flip(dead_bug, False, True) # Upside down
            screen.blit(dead_bug, (60, screen.get_height() - 40)) # Trophies at bottom left
        else:
            # CHANGED > to < HERE
            if ladybug_x < kitty_x: 
                current_ladybug_img = pygame.transform.flip(current_ladybug_img, True, False)
            screen.blit(current_ladybug_img, (ladybug_x, ladybug_y))

    # 3. STATE: MENU
    elif game_state == "menu":
        screen.fill((100, 150, 250)) 
        
        start_text = pygame.font.Font(None, 60).render("START GAME", True, 'white')
        start_rect = start_text.get_rect(center=(screen.get_width()//2, 200))
        
        sound_text = pygame.font.Font(None, 60).render(f"SOUND: {'ON' if sound_on else 'OFF'}", True, 'white')
        sound_rect = sound_text.get_rect(center=(screen.get_width()//2, 280))
        
        exit_text = pygame.font.Font(None, 60).render("EXIT", True, 'white')
        exit_rect = exit_text.get_rect(center=(screen.get_width()//2, 360))
        
        screen.blit(start_text, start_rect)
        screen.blit(sound_text, sound_rect)
        screen.blit(exit_text, exit_rect)
        screen.blit(gamenametext_surface, (screen.get_width()//2 - gamenametext_surface.get_width()//2, 50))

    # 4. STATE: GAME OVER
    elif game_state == "game_over":
        screen.fill((20, 20, 30)) 
        
        end_text = pygame.font.Font(None, 50).render(end_reason, True, 'white')
        time_text = pygame.font.Font(None, 40).render(f"Survival Time: {survival_time} seconds", True, 'yellow')
        quit_text = pygame.font.Font(None, 30).render("Close the window to exit.", True, 'gray')
        
        screen.blit(end_text, (screen.get_width()//2 - end_text.get_width()//2, screen.get_height()//2 - 50))
        screen.blit(time_text, (screen.get_width()//2 - time_text.get_width()//2, screen.get_height()//2 + 20))
        screen.blit(quit_text, (screen.get_width()//2 - quit_text.get_width()//2, screen.get_height() - 50))

    pygame.display.update()
    
pygame.quit()
sys.exit()