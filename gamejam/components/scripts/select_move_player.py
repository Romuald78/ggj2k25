
from ecsv3.core.component.script.script_comp import ScriptComponent


class MovePlayer(ScriptComponent):

    SPEED = 50

    # -----------------------------------------
    # ABSTRACT METHOD
    # -----------------------------------------
    def execute(self, delta_time = 1/60):
        # search for player and check if this player is 'selected'
        if not self.__players[self.__ctrlID]['selected']:
            # Move
            self.__gfx.x += self.__axisX.value * MovePlayer.SPEED
            self.__gfx.y += self.__axisY.value * MovePlayer.SPEED
            # Limits
            self.__gfx.x = min(self.__limits[1], max(self.__limits[0], self.__gfx.x))
            self.__gfx.y = min(self.__limits[2], max(self.__limits[3], self.__gfx.y))


    # -----------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------
    def __init__(self, name, gfx, axisX, axisY, limits, ctrlID, players):
        super().__init__(name)
        self.__gfx = gfx
        self.__axisX = axisX
        self.__axisY = axisY
        self.__limits = limits
        self.__ctrlID = ctrlID
        self.__players = players

