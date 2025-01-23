import arcade
from arcade import LRBT

from ecsv3.core.loader.loader import ResourceLoader
from ecsv3.core.scenes.scene import Scene
from ecsv3.utils.logs import ECSv3


class LoaderScene(Scene):

    MIN_TIME = 0.016666666

    @staticmethod
    def load_image(filepath):
        tex = arcade.load_texture(filepath)
        return tex
    
    def __init__(self, world, next_scene_name, images={}, fonts={}):
        super().__init__(world, 'Loader scene')
        self.__next_scene = next_scene_name
        self.__img = images
        self.__N     = len(self.__img)
        self.__count = LoaderScene.MIN_TIME
        self.__name  = None
        self.__names = arcade.SpriteList()
        self.__loading = False
        self.__fonts = fonts
        # Load all fonts
        for fnt in self.__fonts:
            ResourceLoader.addFont(self.__fonts[fnt])

    def update(self, delta_time=1/60):
        # Load one image per period
        self.__count += delta_time
        if len(self.__img) > 0:
            if self.__count >= LoaderScene.MIN_TIME:
                self.__count -= LoaderScene.MIN_TIME
                # get first resource from dictionary
                names = list(self.__img.keys())
                name = names[0]
                self.__name = arcade.create_text_sprite(text=f"Loading image '{name}'...",
                                                        width=self.width, font_size=32,
                                                        align='center',
                                                        anchor_x='left',
                                                        font_name='Super Kinds',
                                                        color=(255,255,255,200))
                self.__names.clear()
                self.__names.append(self.__name)
                # print(f"loading texture {name}")
                ResourceLoader.addTexture(name, self.__img[name])
                # remove
                del self.__img[name]
                if ResourceLoader.getTextureFilepath(name) is None:
                    ECSv3.error(f"Failure when trying to load texture '{name}'")

        elif self.__count >= LoaderScene.MIN_TIME:
            if not self.__loading:
                self.__loading = True
                # Load all scenes in memory
                self.world.load_all_scenes()
                # reinit timer to display message
                self.__count -= LoaderScene.MIN_TIME
                # display message
                self.__name = arcade.create_text_sprite(f"Loading scenes...",
                                                        width=self.width, font_size=32,
                                                        align='center',
                                                        anchor_x='left',
                                                        font_name='Super Kinds',
                                                        color=(255,255,255,255))
                self.__names.clear()
                self.__names.append(self.__name)
            else:
                # and switch to next scene when loading is finished
                self.world.switch_to_scene(self.__next_scene)

    def draw(self):
        coef  = 1 - len(self.__img) / self.__N
        coef2 = 1 - (len(self.__img)+1) / self.__N
        W, H = self.world.window.get_size()
        x   = W * 0.125
        W2  = W * 0.75
        dx  = W2 * coef
        dx2 = W2 * coef2
        y   = (H / 2)
        dy  = 50
        # Create rectangles (Green Red and outline)
        arcade.draw_rect_filled ( LRBT(x, x + dx , y, y+ dy), (255, 128, 128, 192))
        arcade.draw_rect_filled ( LRBT(x, x + dx2, y, y+ dy), (  0, 255, 128, 160))
        arcade.draw_rect_outline( LRBT(x, x + W2 , y, y+ dy), (255, 255, 255, 128))
        if self.__name is not None:
            self.__name.center_x = W / 2
            self.__name.center_y = H / 2 - dy
            self.__names.draw()

    def enter(self, params=None):
        pass

    def exit(self, params=None):
        pass
