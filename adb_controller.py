import subprocess
import time
import os

class ADBController:
    def __init__(self, device_id=None):
        self.device_id = device_id
        self.adb_prefix = ["adb"]
        if device_id:
            self.adb_prefix = ["adb", "-s", device_id]

    def _run_cmd(self, cmd):
        """执行 adb 命令并返回输出"""
        full_cmd = self.adb_prefix + cmd
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip()

    def tap(self, x, y):
        """点击坐标"""
        self._run_cmd(["shell", "input", "tap", str(x), str(y)])
        time.sleep(0.2)

    def swipe(self, start_x, start_y, end_x, end_y, duration=500):
        """滑动"""
        self._run_cmd(["shell", "input", "swipe", str(start_x), str(start_y), str(end_x), str(end_y), str(duration)])
        time.sleep(0.5)

    def input_text(self, text):
        """输入文本"""
        self._run_cmd(["shell", "input", "text", text])

    def screenshot(self, save_path="screenshot.png"):
        """截图并保存到电脑"""
        self._run_cmd(["shell", "screencap", "-p", "/sdcard/screen.png"])
        self._run_cmd(["pull", "/sdcard/screen.png", save_path])
        return save_path

    def get_current_activity(self):
        """获取当前前台应用信息"""
        out, _ = self._run_cmd(["shell", "dumpsys", "window", "windows", "|", "grep", "mCurrentFocus"])
        return out

    def start_app(self, package_name, activity_name=None):
        """启动应用"""
        if activity_name:
            cmd = f"shell am start -n {package_name}/{activity_name}"
        else:
            cmd = f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
        self._run_cmd(cmd.split())
        time.sleep(2)