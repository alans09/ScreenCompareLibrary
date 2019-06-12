from ScreenCompareLibrary.keywords._compare import _Compare
from ScreenCompareLibrary.version import VERSION


__version__ = VERSION


class ScreenCompareLibrary(_Compare):
    """ Screen Compare Library uses cv2 to compare screenshots/pictures

    This library should work on all environments (windows/linux/osx/unix)

    = Before running tests =

    To run and use library all you need is to install it via setup.py

    = Resizing images before running =

    Library is easy to use and straightforward. Because if you want to compare screenshots
    they have to be the same size you may want to resize images
    before comparision.
    To do this initialize library with parameter that is sizex,sizey

    `Library    ScreenCompareLibrary    1024,768`
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, resize=None):
        """ ScreenCompareLibrary can use one optional argument

        `resize`    sizex,sizey    (eg. 1024,768)

        Example:

        | Library | ScreenCompareLibrary |
        | Library | ScreenCompareLibrary | 1024,768
        | Library | ScreenCompareLibrary | 1900,1080
        """
        self.resize = resize
