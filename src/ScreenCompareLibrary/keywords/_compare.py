import imutils
import glob
import os
import cv2
import numpy
from skimage.measure import compare_ssim


class _Compare:
    """ Comparision keywords """
    def _compare(self, image_a, image_b, diff_name=None):
        """ Internal compare function that is responsible for almost everything. """
        if self.resize:
            dim = (int(self.resize.split(",")[0]), int(self.resize.split(",")[1]))
            image_a = cv2.resize(image_a, dim, interpolation=cv2.INTER_AREA)
            image_b = cv2.resize(image_b, dim, interpolation=cv2.INTER_AREA)
        gray_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        gray_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)
        (score, diff) = compare_ssim(gray_a, gray_b, full=True)
        diff = (diff * 255).astype("uint8")
        thresh = cv2.threshold(
            diff, 0, 255,
            cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(image_a, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(image_b, (x, y), (x + w, y + h), (0, 0, 255), 2)
        if score == 1:
            return True
        else:
            if diff_name:
                cv2.imwrite(diff_name, image_b)
            return False

    def compare_screenshots(self, image_a, image_b, diff_name=None):
        """Compare two screenshots and get True/False according to match

        `image_a`    first image to compare

        `image_b`    second image to compare (on this image diff will be shown

        `diff_name`    default None, specify name of image to be stored and diff will be shown on it

        Example:

        | Compare Screenshots | test.png | test2.png |
        | Compare Screenshots | test.png | test2.png | diff.png |
        """
        image_a = cv2.imread(image_a)
        image_b = cv2.imread(image_b)
        comparision = self._compare(image_a, image_b, diff_name)
        if comparision:
            return True
        else:
            return False

    def compare_folders(self, folder_a, folder_b, diff=False, end_on_error=False):
        """Compare two folders one to one

        Beware, the name of images must be the same in order to zip them to list structure

        `folder_a`    first folder

        `folder_b`    second folder

        `diff`    default False. If set to true DIFF folder will be created and diffs will be stored there

        `end_on_error`    default False. If set on first occurrence of different images script is stopped.

        Example:

        | Compare Folders | Actual | Original |
        | Compare Folders | Actual | Original | diff=True |
        | Compare Folders | Actual | Original | diff=True | end_on_error=True |
        """
        list_of_files = zip(glob.glob(f"{folder_a}/*.*"), glob.glob(f"{folder_b}/*.*"))
        for pair in list_of_files:
            if diff:
                if not os.path.isdir("DIFF"):
                    os.mkdir("DIFF")
                _, file1 = os.path.split(pair[0])
                _, file2 = os.path.split(pair[1])
                res = self.compare_screenshots(
                    pair[0], pair[1],
                    diff_name=f"DIFF/{file1}-{file2}.png"
                )
            else:
                res = self.compare_screenshots(pair[0], pair[1])
            if end_on_error:
                if not res:
                    raise AssertionError(
                        f"Pictures {pair[0]} and {pair[1]} are not the same"
                    )
        return None

    def find_image_location(
            self,
            image_original,
            image_in,
            result=None,
            treshold=0.8):
        """Tries to find if image contains another image


        `image_orignal`    image to search in

        `image_in`    image to find within image_original

        `result`    default None. If set, save image and show where image_in is cointained

        `treshold`    default 0.8. Treshold that is used to match

        Example:

        | Find Image Location | ORIGINAL.png | TO_FIND.png |
        | Find Image Location | ORIGINAL.png | TO_FIND.png | result=RESULT.png |
        """
        treshold = float(treshold)
        img_original = cv2.imread(image_original)
        img_to_find = cv2.imread(image_in)
        w, h = img_to_find.shape[:-1]

        res = cv2.matchTemplate(img_original, img_to_find,
                                cv2.TM_CCOEFF_NORMED)
        loc = numpy.where(res >= treshold)
        print(loc)
        print(type(loc))
        if loc[0].size == 0:
            raise AssertionError("Image is not within source image")
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_original, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)
        if result:
            cv2.imwrite(result, img_original)

