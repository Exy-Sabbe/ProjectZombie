class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Camera(metaclass=Singleton):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__window_width = 0
        self.__window_height = 0

    def SetWindowSize(self, width, height):
        self.__window_width = width
        self.__window_height = height

    def GetXPos(self):
        return self.__x

    def GetYPos(self):
        return self.__y

    def SetCameraPos(self, pos):
        self.__x = pos[0] - self.__window_width / 2
        self.__y = pos[1] - self.__window_height / 2