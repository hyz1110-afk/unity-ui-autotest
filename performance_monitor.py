import re
import subprocess

class PerformanceMonitor:
    def __init__(self, adb_controller, package_name):
        self.adb = adb_controller
        self.package = package_name

    def _run_cmd(self, cmd):
        full_cmd = ["adb"] + cmd
        result = subprocess.run(full_cmd, capture_output=True, text=True)
        return result.stdout, result.stderr

    def get_cpu_usage(self):
        """获取 CPU 占用百分比（近似值）"""
        out, _ = self._run_cmd(["shell", "top", "-n", "1", "-d", "0.5", "|", "grep", self.package])
        # top 输出示例: 12345  u0_a123  10%  S   123456K  ...
        match = re.search(r'(\d+)%', out)
        if match:
            return int(match.group(1))
        return None

    def get_memory_mb(self):
        """获取内存占用（MB）"""
        out, _ = self._run_cmd(["shell", "dumpsys", "meminfo", self.package])
        for line in out.split('\n'):
            if "TOTAL" in line and "PSS" not in line:
                numbers = re.findall(r'\d+', line)
                if numbers:
                    # 单位是 KB
                    return int(numbers[-1]) / 1024
        return None

    def get_fps(self):
        """
        获取帧率（需要游戏支持，通过 dumpsys gfxinfo 计算）
        简化实现：返回 None，可后续扩展
        """
        # 完整实现较复杂，先返回模拟值或 None
        return None