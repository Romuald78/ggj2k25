
import arcade

from ecsv3.core.loader.loader import ResourceLoader
from ecsv3.core.scenes.loader_scene import LoaderScene
from ecsv3.core.world import World
from gamejam.scenes.select import Select
from gamejam.utils.pre_load import PRE_LOAD_IMAGES, PRE_LOAD_FONTS, PRE_LOAD_SOUNDS
from gamejam.scenes.ingame import InGame
from gamejam.scenes.intro import Intro
from gamejam.scenes.splash import Splash
from launchers.arcade.arcade_launcher import run
from launchers.arcade.default_config import DEFAULT_CONFIG
try:
    from launchers.arcade.configs.debug.debug_config import USER_CONFIG
except:
    from launchers.arcade.configs.release.release_config import USER_CONFIG


if __name__ == '__main__':


    # ====================================
    # Set Resource loader callback (arcade here)
    # ====================================
    ResourceLoader.set_texture_callback(LoaderScene.load_image)
    ResourceLoader.set_font_callback   (arcade.load_font   )
    ResourceLoader.set_sound_callback  (arcade.Sound)

    # list all resources
    img = PRE_LOAD_IMAGES
    fnt = PRE_LOAD_FONTS
    snd = PRE_LOAD_SOUNDS

    # list all scene classes
    scn = [
        ('Intro',  Intro),
        ('Splash', Splash),
        ('Select', Select),
        ('InGame', InGame),
    ]

    # Create world reference
    world = World('ECSv3 Game App', load_img=img, load_scn=scn, load_fnt=fnt, load_snd=snd)

    # Get default config
    defaultCfg = DEFAULT_CONFIG
    # Get either debug or release config (according to used files)
    userCfg = USER_CONFIG
    # apply user config into default config
    for field in userCfg:
        defaultCfg[field] = userCfg[field]

    # run ___game
    run(world, defaultCfg)
