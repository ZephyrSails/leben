import pygame
import random
import os
import sys

pygame.mixer.init()
pygame.mixer.set_num_channels(30)

APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(APP_FOLDER)

sfx_missle_impact_miss = [
    pygame.mixer.Sound("rsc/sounds/Missile Impact Miss_001.ogg"),
    pygame.mixer.Sound("rsc/sounds/Missile Impact Miss_002.ogg"),
    pygame.mixer.Sound("rsc/sounds/Missile Impact Miss_003.ogg"),
]
sfx_missle_impact = [
    pygame.mixer.Sound("rsc/sounds/Missile Impact_005.ogg"),
    pygame.mixer.Sound("rsc/sounds/Missile Impact_006.ogg"),
    pygame.mixer.Sound("rsc/sounds/Missile Impact_007.ogg"),
]
sfx_weapon_c_art_cruier_missile_fire = [
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_art-cruiser_missile_fire_01.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_art-cruiser_missile_fire_02.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_art-cruiser_missile_fire_03.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_art-cruiser_missile_fire_04.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_art-cruiser_missile_fire_05.ogg"),
]
sfx_weapon_c_rapidfire_light_loop_near = [
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_near_01.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_near_02.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_near_03.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_near_04.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_near_05.ogg"),
]
sfx_weapon_c_rapidfire_light_outro_near = [
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_near_01.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_near_02.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_near_03.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_near_04.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_near_05.ogg"),
]
sfx_weapon_c_rapidfire_light_loop_far = [
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_far_01.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_far_02.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_far_03.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_far_04.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_loop_far_05.ogg"),
]
sfx_weapon_c_rapidfire_light_outro_far = [
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_far_01.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_far_02.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_far_03.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_far_04.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weapon_c_rapidfire_light_outro_far_05.ogg"),
]
sfx_catamaran_impact_metal = [
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_01.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_02.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_03.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_04.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_05.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_06.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_07.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_08.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_09.ogg"),
    pygame.mixer.Sound("rsc/sounds/Catamaran_Impact_Metal_10.ogg"),
]
sfx_weap_mg_ricochet = [
    pygame.mixer.Sound("rsc/sounds/sfx_weap_mg_ricochet01.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weap_mg_ricochet03.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weap_mg_ricochet10.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weap_mg_ricochet12.ogg"),
    pygame.mixer.Sound("rsc/sounds/sfx_weap_mg_ricochet13.ogg"),
]


def play_list(sound_list):
    get_sound_from_list(sound_list).play()

def get_sound_from_list(sound_list):
    idx = random.randint(0, len(sound_list) - 1)
    return sound_list[idx]
