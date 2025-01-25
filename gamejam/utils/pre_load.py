import os
import sys

def get_path(relative_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = os.path.join(sys._MEIPASS, relative_path)
    else:
        bundle_dir = os.path.join(os.path.dirname(__file__), '..', '..', relative_path)
    return bundle_dir


IMG_DIR = get_path('resources/images')
FNT_DIR = get_path('resources/fonts')

PRE_LOAD_IMAGES = {
    # INTRO backgrounds
    'rphstudio'    : f"{IMG_DIR}/backgrounds/rphstudio.png",
    'arcade'       : f"{IMG_DIR}/backgrounds/arcade.png",
    'gamejam'      : f"{IMG_DIR}/backgrounds/gamejam.png",
    'splash'       : f"{IMG_DIR}/backgrounds/splash.png",
    'select'       : f"{IMG_DIR}/backgrounds/select.png",
    'ingame'       : f"{IMG_DIR}/backgrounds/ingame.png",

    'bubble_select': f"{IMG_DIR}/characters/bubble_select.png",

    'front_hero1'  : f"{IMG_DIR}/characters/front_hero1.png",
    'front_hero2'  : f"{IMG_DIR}/characters/front_hero2.png",
    'front_hero3'  : f"{IMG_DIR}/characters/front_hero3.png",
    'front_hero4'  : f"{IMG_DIR}/characters/front_hero4.png",

    'back_hero1': f"{IMG_DIR}/characters/back_hero1.png",
    'back_hero2': f"{IMG_DIR}/characters/back_hero2.png",
    # 'back_hero3': f"{IMG_DIR}/characters/back_hero3.png",
    'back_hero4': f"{IMG_DIR}/characters/back_hero4.png"

}


PRE_LOAD_FONTS = {
    'superkinds'  : f"{FNT_DIR}/super_kinds.ttf",
}
