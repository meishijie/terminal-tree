#!/usr/bin/env python3
"""紧凑版tree应用，适合非常小的终端"""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Tree, Static
from textual.containers import Vertical

class CompactTreeApp(App):
    """紧凑版树形应用"""

    CSS = """
    Screen {
        background: $surface;
        height: 100vh;
    }

    Tree {
        height: 1fr;
        width: 1fr;
        background: $surface;
        color: $text;
        border: none;
        margin: 0;
        padding: 0;
    }

    Static {
        height: 1;
        background: $primary;
        color: $text;
        margin: 0;
        padding: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("backspace", "go_up", "Parent Dir"),
    ]

    def __init__(self, start_path: Path = None, **kwargs):
        super().__init__(**kwargs)
        self.start_path = start_path or Path.cwd()
        self._tree_widget = None

    def compose(self) -> ComposeResult:
        """组合界面 - 最小化布局"""
        yield Static(f"📁 Tree: {self.start_path.name or str(self.start_path)} | q=quit", id="status")

        self._tree_widget = Tree(f"📁 {self.start_path.name or str(self.start_path)}")
        self._tree_widget.show_root = True
        self._tree_widget.show_guides = False  # 简化显示
        yield self._tree_widget

    def on_mount(self) -> None:
        """挂载时初始化"""
        if self._tree_widget:
            self.populate_tree()
            self._tree_widget.focus()

    def populate_tree(self):
        """填充树结构"""
        if not self._tree_widget:
            return

        try:
            # 清除现有内容
            self._tree_widget.clear()

            # 设置根节点
            root_name = self.start_path.name or str(self.start_path)
            self._tree_widget.root.set_label(f"📁 {root_name}")
            self._tree_widget.root.data = self.start_path

            # 获取目录内容
            try:
                items = list(self.start_path.iterdir())

                # 过滤和排序
                items = [item for item in items if not item.name.startswith('.')]
                items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
                items = items[:15]  # 限制显示数量

                # 添加到树中
                for item in items:
                    icon = "📁" if item.is_dir() else "📄"
                    self._tree_widget.root.add(f"{icon} {item.name}", data=item)

                # 展开根节点
                self._tree_widget.root.expand()

                # 更新状态
                status_widget = self.query_one("#status", Static)
                status_widget.update(f"📁 {root_name} ({len(items)} items) | q=quit")

            except PermissionError:
                self._tree_widget.root.add("❌ Permission denied")
            except Exception as e:
                self._tree_widget.root.add(f"❌ Error: {str(e)[:30]}")

        except Exception as e:
            if self._tree_widget and self._tree_widget.root:
                self._tree_widget.root.set_label(f"❌ Error: {str(e)[:30]}")

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """处理节点选择"""
        node = event.node
        path = node.data

        if path and path.is_dir():
            # 切换到选择的目录
            self.start_path = path
            self.populate_tree()

    def action_quit(self):
        """退出应用"""
        self.exit()
    
    def action_go_up(self):
        """返回上级目录"""
        parent = self.start_path.parent
        if parent != self.start_path:  # 不在根目录
            self.start_path = parent
            self.populate_tree()

if __name__ == "__main__":
    import sys
    
    print("🚀 启动紧凑Tree应用...")
    print("📏 此版本适合非常小的终端")
    print("🎯 使用箭头键导航，回车选择目录，q退出")
    print()
    
    # 支持命令行参数指定起始目录
    start_path = None
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
        if target_path.exists() and target_path.is_dir():
            start_path = target_path
        else:
            print(f"❌ 错误: 目录 '{sys.argv[1]}' 不存在")
            sys.exit(1)
    
    try:
        app = CompactTreeApp(start_path=start_path)
        app.run()
        print("✅ 应用正常退出")
    except Exception as e:
        print(f"❌ 应用出错: {e}")
        import traceback
        traceback.print_exc()