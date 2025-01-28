import arcade

from ecsv3.utils.logs import ECSv3


class ResourceLoader:

    # static properties
    __textures = {}
    __sounds   = {}
    __img_cb   = None
    __snd_cb   = None
    __fnt_cb   = None

    @staticmethod
    def set_texture_callback(cb):
        ResourceLoader.__img_cb = cb

    @staticmethod
    def set_font_callback(cb):
        ResourceLoader.__fnt_cb = cb

    @staticmethod
    def set_sound_callback(cb):
        ResourceLoader.__snd_cb = cb

    @staticmethod
    def addSound(name, snd_path):
        if ResourceLoader.__snd_cb is not None:
            if name in ResourceLoader.__sounds:
                ECSv3.error(f"Try to add sound '{name}' twice !")
            # Create sound
            snd = ResourceLoader.__snd_cb(snd_path)
            # store sound
            ResourceLoader.__sounds[name] = { 'path' : snd_path, 'sound' : snd}
        print(ResourceLoader.__sounds)

    @staticmethod
    def getSoundFilepath(name):
        result = None
        if name in ResourceLoader.__sounds:
            result = ResourceLoader.__sounds[name]['path']
        return result


    @staticmethod
    def addTexture(name, img_path):
        # print(f"loading image {img_path}...")
        if ResourceLoader.__img_cb is not None:
            if name in ResourceLoader.__textures:
                ECSv3.error(f"Try to add texture '{name}' twice !")
            # Create texture
            tex = ResourceLoader.__img_cb(img_path)
            # store texture
            ResourceLoader.__textures[name] = { 'path' : img_path, 'texture' : tex}

    @staticmethod
    def getTextureFilepath(name):
        result = None
        if name in ResourceLoader.__textures:
            result = ResourceLoader.__textures[name]['path']
        return result


    @staticmethod
    def getSoundReference(name):
        result = None
        if name in ResourceLoader.__sounds:
            result = ResourceLoader.__sounds[name]['sound']
        return result

    @staticmethod
    def getTextureReference(name):
        result = None
        if name in ResourceLoader.__textures:
            result = ResourceLoader.__textures[name]['texture']
        return result

    @staticmethod
    def getTextureReferenceFlipH(name):
        result = None
        if name in ResourceLoader.__textures:
            result = ResourceLoader.__textures[name]['texture']
            result = result.flip_left_right()
        return result


    @staticmethod
    def addFont(fontfile):
        # print(f"loading font {fontfile}...")
        if ResourceLoader.__fnt_cb is not None:
            ResourceLoader.__fnt_cb(fontfile)