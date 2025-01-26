import arcade
from arcade import Sprite, TextureAnimationSprite, Texture

from ecsv3.core.component.gfx.gfx_comp import GfxComponent, GfxAnchor
from ecsv3.core.loader.loader import ResourceLoader


class ArcadeFixed(GfxComponent):

    def __init__(self, texture_ref, name='gfx_fix0', priority=1, anchor=GfxAnchor.CENTER, filter_color=(255,255,255,255), flipH=False):
        super().__init__(name, priority, anchor)
        if isinstance(texture_ref, Sprite):
            # print('store sprite directly', name, texture_ref)
            self._spr = texture_ref
        elif isinstance(texture_ref, Texture):
            # print('create sprite from texture reference', name)
            self._spr = Sprite(texture_ref)
        else:
            # print('create sprite from texture name', name)
            if flipH:
                tex = ResourceLoader.getTextureReferenceFlipH(texture_ref)
            else:
                tex = ResourceLoader.getTextureReference(texture_ref)
            # print(texture_ref, tex)
            self._spr = Sprite(tex)
            # print(self._spr)
        # set color
        self.color = filter_color
        # update priority
        self._spr.prio = self.priority

    # -----------------------------------------
    # PROPERTIES
    # -----------------------------------------
    @property
    def gfx_object(self):
        return self._spr

    @property
    def x(self):
        return self._spr.center_x + self.offset_x

    @x.setter
    def x(self, value):
        self._spr.center_x = value - self.offset_x

    @property
    def y(self):
        return self._spr.center_y + self.offset_y

    @y.setter
    def y(self, value):
        self._spr.center_y = value - self.offset_y

    @property
    def angle(self):
        return self._spr.angle

    @angle.setter
    def angle(self, value):
        self._spr.angle = value

    @property
    def scale(self):
        return self._spr.scale_x

    @scale.setter
    def scale(self, value):
        self._spr.scale = value

    @property
    def width(self):
        return self._spr.width

    @property
    def height(self):
        return self._spr.height

    @property
    def color(self):
        return self._spr.color

    @color.setter
    def color(self, value):
        self._spr.color = value

    @property
    def alpha(self):
        return self._spr.alpha

    @alpha.setter
    def alpha(self, value):
        self._spr.alpha = value

    # -----------------------------------------
    # PUBLIC METHODS
    # -----------------------------------------
    def set_new_priority_value(self, new_prio):
        self._spr.depth = new_prio

    def resize(self, width=None, height=None, keepRatio=True):
        kx = 1
        ky = 1
        if width is not None:
            kx = width / self.width
        if height is not None:
            ky = height / self.height

        if width is not None and height is None:
            if keepRatio:
                ky = kx
        elif height is not None and width is None:
            if keepRatio:
                kx = ky
        else:
            if keepRatio:
                kx = min(kx, ky)
                ky = kx

        self._spr.scale_x *= kx
        self._spr.scale_y *= ky


class ArcadeAnim(ArcadeFixed):

    def __init__(self, texture_name, name,
                 priority = 1, anchor = GfxAnchor.CENTER,
                 nb_frame_X=1, nb_frame_Y=1,
                 startIndex=0, endIndex=0,
                 frameDuration=1,
                 repeat=None, back_forth=False,
                 flip_h=False, flip_v=False,
                 filter_color=(255,255,255,255) ):
        arcanim = InternalArcadeAnimation(texture_name, nb_frame_X, nb_frame_Y,
                                          startIndex, endIndex, frameDuration, repeat, back_forth,
                                          flip_h=flip_h, flip_v=flip_v)

        super().__init__(arcanim, name=name, priority=priority, anchor=anchor, filter_color=filter_color)

    def rewind(self):
        self._spr.rewind()

    def pause(self):
        self._spr.pause()

    def resume(self):
        self._spr.resume()

    def toggle_play(self):
        self._spr.toggle_play()

    # rewind and resume animation
    def restart(self):
        self.rewind()
        self.resume()

    @property
    def playing(self):
        return self._spr.playing

    @property
    def stopped(self):
        return self._spr.stopped

    @property
    def finished(self):
        return self._spr.finished



class InternalArcadeAnimation(TextureAnimationSprite):

    def __init__(self, texture_name,
                 nb_frame_X=1, nb_frame_Y=1,
                 startIndex=0, endIndex=0,
                 frameDuration=1,
                 repeat=None, back_forth=False,
                 flip_h=False, flip_v=False
                ):
        # get resource
        full_texture = ResourceLoader.getTextureReference(texture_name)
        # repeat counter (loop_step=0 means infinite)
        self.__loop_step   = -1
        self.__max_counter = repeat
        if repeat is None or repeat <= 0:
            self.__loop_step   = 0
            self.__max_counter = 1
        self.__counter = self.__max_counter
        self.__frameDuration = frameDuration
        self.__back_forth = back_forth
        self.__paused = False

        # get textures from image
        textureKeyFrames = []
        indexes = list(range(startIndex, endIndex + 1))
        if back_forth:
            indexes += list(range(endIndex -1, startIndex, -1))
        for i in indexes:
            y = i // nb_frame_X
            x = i % nb_frame_X
            w = full_texture.width  // nb_frame_X
            h = full_texture.height // nb_frame_Y
            texture = full_texture.crop(x * w, y * h, w, h)
            if flip_h:
                texture = texture.flip_left_right()
            if flip_v:
                texture = texture.flip_top_bottom()
            tkf     = arcade.TextureKeyframe(texture, frameDuration*1000)
            textureKeyFrames.append(tkf)
        # if self.__back_forth:
        #     for i in range(endIndex -1, startIndex, -1):
        #         y = i // nb_frame_Y
        #         x = i % nb_frame_X
        #         w = full_texture.width // nb_frame_X
        #         h = full_texture.height // nb_frame_Y
        #         texture = full_texture.crop(x * w, y * h, w, h)
        #         tkf = arcade.TextureKeyframe(texture, frameDuration * 1000)
        #         textures.append(tkf)

        # Load textures into Time based Sprite
        anim = arcade.TextureAnimation(textureKeyFrames)
        super().__init__(animation=anim)

    # just rewind to the very first frame
    # reinit nb of loops too
    # do not modify pause property
    def rewind(self):
        self.__counter = self.__max_counter
        self._current_keyframe_index = 0
        self.texture = self._animation.keyframes[0].texture
        self._time = 0.0

    def pause(self):
        self.__paused = True

    def resume(self):
        self.__paused = False

    def toggle_play(self):
        self.__paused = not self.__paused

    @property
    def playing(self):
        return not self.paused

    @property
    def stopped(self):
        return not self.playing

    @property
    def finished(self):
        return self.__counter <= 0

    def update_animation(self, delta_time=1/60, **kwargs):
        if self.__counter > 0 and not self.__paused:
            # get texture number before update
            i = self._current_keyframe_index
            # update animation if needed
            super().update_animation(delta_time)
            # get texture number after update
            j = self._current_keyframe_index
            # check if frame has been changed
            # if yes : check repeat number
            if j < i:
                self.__counter += self.__loop_step
                # keep the last animation frame
                if self.__counter <= 0:
                    if not self.__back_forth:
                        super().update_animation(-self.__frameDuration)




class ArcadeRectangle(ArcadeFixed):

    def __init__(self, name,
                 priority = 1, anchor = GfxAnchor.CENTER,
                 w=100, h=100,
                 clr=(255,255,255) ):
        texture = arcade.make_soft_square_texture(size=max(w, h), color=(255,255,255,255),
                                                  center_alpha=255,
                                                  outer_alpha=255)
        texture.width  = w
        texture.height = h
        super().__init__(texture, name=name, priority=priority, anchor=anchor, filter_color=clr)


class ArcadeOval(ArcadeFixed):

    def __init__(self, name,
                 priority = 1, anchor = GfxAnchor.CENTER,
                 w=100, h=100,
                 clr=(255,255,255) ):
        texture = arcade.make_soft_circle_texture(diameter=max(w, h),
                                                  color=(255,255,255,255),
                                                  center_alpha=255,
                                                  outer_alpha=255)
        texture.width  = w
        texture.height = h
        super().__init__(texture, name=name, priority=priority, anchor=anchor, filter_color=clr)


class ArcadeText(ArcadeFixed):

    def __init__(self, name, msg, font='arial', size=40,
                 priority = 1, anchor = GfxAnchor.CENTER,
                 w=None, h=None,
                 clr=(255,255,255) ):

        sprite = arcade.create_text_sprite(text=msg,
                                           color=clr,
                                           font_size=size,
                                           font_name=font)
        super().__init__(sprite._texture, name=name,
                         priority=priority,
                         anchor=anchor)
        self.resize(w, h)

