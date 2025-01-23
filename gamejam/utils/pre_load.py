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
    'rphstudio'   : f"{IMG_DIR}/backgrounds/rphstudio.png",
    'arcade'      : f"{IMG_DIR}/backgrounds/arcade.png",
    'gamejam'     : f"{IMG_DIR}/backgrounds/gamejam.png",

}


PRE_LOAD_FONTS = {
    'superkinds'  : f"{FNT_DIR}/super_kinds.ttf",
}
