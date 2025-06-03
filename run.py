#!/usr/bin/env python3
"""
Terminal Tree - 现代化终端文件系统导航器
运行脚本，启动完整功能版本
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from terminal_tree_plugin.app import TerminalTreeApp


def main():
    """运行Terminal Tree应用."""
    # 解析命令行参数
    start_path = Path.cwd()

    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
        if target_path.exists() and target_path.is_dir():
            start_path = target_path
        else:
            print(f"❌ 错误: 目录 '{sys.argv[1]}' 不存在")
            print(f"📁 使用当前目录: {start_path}")

    print("🌲 Terminal Tree - 现代化文件浏览器")
    print(f"📁 起始目录: {start_path}")
    print("💡 快捷键: ↑↓←→ 导航, Enter 进入, Backspace 返回, q 退出")
    print()

    try:
        app = TerminalTreeApp(start_path=start_path)
        app.run()
    except KeyboardInterrupt:
        print("\n👋 再见!")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())