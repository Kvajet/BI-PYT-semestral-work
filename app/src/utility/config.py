"""Configuration file for the game.
"""
config = dict(
    refresh_rate=240,
    tile_size=16,
    level_size=(18, 9),  # has to be > 0 and dividable by 3
    scale=3,  # this is for rendering purposes only
    except_msg=dict(
        not_implemented='Abstract method is not allowed to be called.'
    ),
    player_type=[
        dict(
            hp=50,
            speed=1.25,
            cooldown=35,
            bullet_dmg=20,
            sprite='player-1.png',
            jumps=3,
            jump_cooldown=45
        ),
        dict(
            hp=40,
            speed=1.0,
            cooldown=25,
            bullet_dmg=15,
            sprite='player-2.png',
            jumps=4,
            jump_cooldown=40
        )
    ],
    enemy_type=[
        # ground enemy
        dict(
            hp=47,
            cooldown=20,
            bullet_dmg=11,
            sprite='enemy-1.png'
        ),
        # flying enemy
        dict(
            hp=70,
            speed=(1.0, 1.0),
            cooldown=15,
            bullet_dmg=7,
            sprite='enemy-2.png'
        ),
        dict(
            hp=60,
            speed=(0.8, 1.2),
            cooldown=5,
            bullet_dmg=10,
            sprite='enemy-2.png'
        )
    ],
    max_enemies=5,
    fire_tile_dmg=4,
    fire_tile_cooldown=20,
    cleared_level_hp=20,
    player_color=(0, 200, 0),
    player_bullet_color=(255, 215, 0),
    enemy_color=(200, 0, 0),
    level_tiles=[
        'top-left.png',
        'top-middle.png',
        'top-right.png',
        'middle-left.png',
        'middle-middle.png',
        'middle-right.png',
        'bottom-left.png',
        'bottom-middle.png',
        'bottom-right.png',
        'lava-puddle.png'
    ],
    text_size=24,
    bullet_scale=0.75,
    top_bar_hp_color=(11, 218, 81, 255),
    top_bar_enemies_color=(237, 41, 57, 255),
    top_bar_teleport_color=(189, 222, 236, 255)
)
