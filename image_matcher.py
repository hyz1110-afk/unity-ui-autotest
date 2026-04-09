import cv2
import numpy as np
import time
import os

class ImageMatcher:
    def __init__(self, threshold=0.6):
        self.threshold = threshold

    def find_template(self, screenshot_path, template_path):
        """
        在截图中查找模板，返回中心坐标 (x, y) 或 None
        """
        if not os.path.exists(screenshot_path) or not os.path.exists(template_path):
            return None

        img = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)
        if img is None or template is None:
            return None

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= self.threshold:
            h, w = template_gray.shape
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return (center_x, center_y)
        return None

    def wait_for_image(self, adb_controller, template_path, timeout=10, interval=0.5, screenshot_dir="screenshots"):
        """
        循环截图等待模板出现，返回坐标；超时返回 None
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 确保截图目录存在
            os.makedirs(screenshot_dir, exist_ok=True)
            temp_screenshot = os.path.join(screenshot_dir, f"temp_{int(time.time()*1000)}.png")
            adb_controller.screenshot(temp_screenshot)
            pos = self.find_template(temp_screenshot, template_path)
            if pos:
                return pos
            time.sleep(interval)
        return None