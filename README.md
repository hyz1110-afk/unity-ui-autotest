# Unity 手游 UI 自动化测试工具

基于 ADB + OpenCV + pytest 的轻量级手游自动化测试工具。

## 功能

- 图像识别定位 UI 元素
- 模拟点击、滑动、输入
- 性能监控（CPU、内存）
- 自动生成 HTML 测试报告

## 快速开始

1. 安装依赖：`pip install opencv-python pytest pytest-html`
2. 连接安卓设备/模拟器，确保 `adb devices` 能看到设备
3. 修改 `test_game_flow.py` 中的 `PACKAGE_NAME` 为你的游戏包名
4. 运行测试：`pytest test_game_flow.py -v -s --html=reports/report.html`

## 目录结构

- `adb_controller.py` - ADB 命令封装
- `image_matcher.py` - 图像识别
- `performance_monitor.py` - 性能采集
- `test_game_flow.py` - 测试用例
- `templates/` - 模板图片
- `reports/` - 测试报告（自动生成）

## 开源协议

MIT License