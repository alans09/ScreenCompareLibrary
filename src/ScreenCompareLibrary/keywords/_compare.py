import imutils
import glob
import os
import cv2
import numpy
from robot.api import logger
from skimage.measure import compare_ssim


class _Compare:
    """ Comparision keywords """
    def _compare(self, image_a, image_b, diff_name=None, threshold=1):
        """ Internal compare function that is responsible for almost everything.

        Function gets all required information as:
        `image_a`    first image

        `image_b`    second image

        `diff_name`  default None, if set it will create file on specified path

        `threshold`  default 1. if changed it will use it for computations
        """
        if self.resize:
            dim = (int(self.resize.split(",")[0]), int(self.resize.split(",")[1]))
            logger.debug(f"Dimensions: {dim}")
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
        logger.debug(f"Image comparision score: {score}")
        logger.debug(f"Threshold set to: {threshold}")
        if score >= int(threshold):
            return True
        else:
            if diff_name:
                cv2.imwrite(diff_name, image_b)
            return False

    def compare_screenshots(self, image_a_path, image_b_path, diff_name=None, threshold=1):
        """Compare two screenshots and get True/False according to match

        `image_a_path`    first image to compare

        `image_b_path`    second image to compare (on this image diff will be shown

        `diff_name`    default None, specify name of image to be stored and diff will be shown on it

        `threshold`     default 1, specify threshold that could be used make comparision (0.0 - 1.0:
                        1 means 100% the same image)

        Example:

        | Compare Screenshots | test.png | test2.png |
        | Compare Screenshots | test.png | test2.png | diff.png |
        """
        logger.debug(f"Image A path: {image_a_path}")
        logger.debug(f"Image B path: {image_b_path}")
        image_a = cv2.imread(image_a_path) if os.path.isfile(image_a_path) else False
        image_b = cv2.imread(image_b_path) if os.path.isfile(image_b_path) else False
        if not isinstance(image_a, numpy.ndarray):
            raise AssertionError(f"Image {image_a_path} does not exists!")
        if not isinstance(image_b, numpy.ndarray):
            raise AssertionError(f"Image {image_b_path} does not exists!")
        return self._compare(image_a, image_b, diff_name, threshold)

    def compare_folders(self, folder_a, folder_b, diff=False, end_on_error=False, threshold=1):
        """Compare two folders one to one

        Beware, the name of images must be the same in order to zip them to list structure

        `folder_a`    first folder

        `folder_b`    second folder

        `diff`    default False. If set to True 'DIFF' folder in actual directory
                  will be created and diffs will be stored there

        `end_on_error`    default False. If set on first occurrence of different images script is stopped.

        `threshold`    default 1. Set the threshold value to use for comparision

        Example:

        | Compare Folders | Actual | Original |
        | Compare Folders | Actual | Original | diff=True |
        | Compare Folders | Actual | Original | diff=True | end_on_error=True |
        | Compare Folders | Actual | Original | threshold=0.5 |
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
                    diff_name=f"DIFF/{file1}-{file2}.png",
                    threshold=threshold
                )
            else:
                res = self.compare_screenshots(pair[0], pair[1], threshold)
            if end_on_error:
                if not res:
                    return False
        return True

    @staticmethod
    def contained_within_image(
            image_original,
            image_within,
            result=None,
            threshold=0.8):
        """Tries to find if image contains another image


        `image_original`    image to search in

        `image_within`    image to find within image_original

        `result`    default None. If set, save image and show where image_in is contained

        `threshold`    default 0.8. Threshold that is used to match

        Example:

        | Contained Within Image | ORIGINAL.png | TO_FIND.png |
        | Contained Within Image | ORIGINAL.png | TO_FIND.png | result=RESULT.png |
        | Contained Within Image | ORIGINAL.png | TO_FIND.png | result=RESULT.png | threshold=0.4 |
        """
        threshold = float(threshold)
        img_original = cv2.imread(image_original)
        img_to_find = cv2.imread(image_within)
        w, h = img_to_find.shape[:-1]

        res = cv2.matchTemplate(img_original, img_to_find,
                                cv2.TM_CCOEFF_NORMED)
        loc = numpy.where(res >= threshold)
        if loc[0].size == 0:
            return False
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_original, pt, (pt[0] + h, pt[1] + w), (0, 0, 255), 2)
        if result:
            logger.debug(f"Going to write image: {result}")
            cv2.imwrite(result, img_original)
        return True
