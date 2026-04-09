import pytest
import time
from adb_controller import ADBController
from image_matcher import ImageMatcher
from performance_monitor import PerformanceMonitor

# 配置（根据你的实际修改）
PACKAGE_NAME = "com.hyz.game"   # 替换为你的包名
LAUNCH_ACTIVITY = "com.unity3d.player.UnityPlayerActivity"
TEMPLATE_BUTTON = "templates/button.png"   # 按钮模板图片

adb = ADBController()
matcher = ImageMatcher(threshold=0.7)
perf = PerformanceMonitor(adb, PACKAGE_NAME)

class TestGameUI:
    def setup_method(self):
        # 启动游戏
        adb._run_cmd(["shell", "am", "start", "-n", f"{PACKAGE_NAME}/{LAUNCH_ACTIVITY}"])
        time.sleep(3)

    def teardown_method(self):
        adb.screenshot(f"screenshots/final_{int(time.time())}.png")

    def test_click_button(self):
        # 等待按钮出现
        btn_pos = matcher.wait_for_image(adb, TEMPLATE_BUTTON, timeout=10)
        assert btn_pos is not None, "按钮未出现"
        # 点击
        adb.tap(btn_pos[0], btn_pos[1])
        time.sleep(1)
        # 可选：验证文本变化（如果需要）
        print("按钮点击成功")