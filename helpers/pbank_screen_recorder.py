import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import os
from helpers.pbank_driver_manager import logger, driver


def set_screencapture(test_name, video_file_path):
    logger.info("Started video recording in :" + str(video_file_path) + " for test: " + test_name)
    if os.path.isfile(video_file_path):
        os.remove(video_file_path)
        logger.info("Removed existing file: " + str(video_file_path))
    else:
        logger.info('The file doesnt exist')

    resolution = (1920, 1080)  # resolution for head less browser
    # resolution = (1920, 846) #resolution for headed browser

    filename = str(video_file_path)
    codec = cv2.VideoWriter_fourcc(*"XVID")
    fps = 10.0
    out = cv2.VideoWriter(filename, codec, fps, resolution)
    while str(test_name) in str(os.getenv('PYTEST_CURRENT_TEST')) and "teardown" not in str(
            os.getenv('PYTEST_CURRENT_TEST')):
        img = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(img))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)

    out.release()
    cv2.destroyAllWindows()
    logger.info("Completed the recording for test name " + test_name)
