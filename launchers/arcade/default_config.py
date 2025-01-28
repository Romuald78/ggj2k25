
DEFAULT_CONFIG = {
    'full_screen'  : False,
    'mouse_visible': True,
    'title'        : 'Elemental Altar : Bubble Edition',
}

class ScreenRatio:

    __ratio = 1.0

    @staticmethod
    def get_ratio():
        return ScreenRatio.__ratio

    @staticmethod
    def set_ratio(valueW, valueH):
        if valueW <= 0 or valueH <= 0:
            raise ValueError(f"bad values for RATIO = {valueW}/{valueH} !")
        ScreenRatio.__ratio = min(valueW / 1920, valueH / 1080)
        # print('Screen ratio', ScreenRatio.__ratio)
