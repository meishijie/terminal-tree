#!/usr/bin/env python3
"""简化的tree应用，针对受限终端环境优化"""

import sys
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.widgets import Header, Footer, Tree, Static
from textual.reactive import reactive

class SimpleTreeApp(App):
    """简化的树形应用"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Header {
        height: 1;
        background: $primary;
        color: $text;
    }
    
    Footer {
        height: 1;
        background: $primary;
        color: $text;
    }
    
    #main_container {
        height: 1fr;
        width: 1fr;
        margin: 0;
        padding: 0;
    }
    
    #tree_container {
        width: 1fr;
        height: 1fr;
        border: solid $primary;
        margin: 0;
        padding: 0;
    }
    
    Tree {
        height: 1fr;
        width: 1fr;
        background: $surface;
        color: $text;
    }
    
    Static {
        height: auto;
        width: 1fr;
        background: $surface;
        color: $text;
        padding: 0 1;
    }
    """
    
    TITLE = "Simple Tree"
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("h", "toggle_hidden", "Hidden"),
        ("backspace", "go_up", "Parent Dir"),
    ]
    
    show_hidden: reactive[bool] = reactive(False)
    
    def __init__(self, start_path: Path = None, **kwargs):
        super().__init__(**kwargs)
        self.start_path = start_path or Path.cwd()
        self._tree_widget = None
    
    def compose(self) -> ComposeResult:
        """组合界面"""
        yield Header()
        
        with Container(id="main_container"):
            yield Static(f"📁 {self.start_path}", id="path_display")
            
            with Container(id="tree_container"):
                self._tree_widget = Tree(f"📁 {self.start_path.name or str(self.start_path)}", id="tree")
                self._tree_widget.show_root = True
                self._tree_widget.show_guides = True
                yield self._tree_widget
        
        yield Footer()
    
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
            self._tree_widget.root.set_label(f"📁 {self.start_path.name or str(self.start_path)}")
            self._tree_widget.root.data = self.start_path
            
            # 获取目录内容
            items = list(self.start_path.iterdir())
            
            # 过滤隐藏文件
            if not self.show_hidden:
                items = [item for item in items if not item.name.startswith('.')]
            
            # 排序并限制数量
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            items = items[:30]  # 限制显示数量
            
            # 添加到树中
            for item in items:
                try:
                    if item.is_dir():
                        icon = "📁"
                        style = "bold blue"
                    else:
                        if item.suffix.lower() in {".py", ".js", ".html", ".css"}:
                            icon = "📄"
                            style = "green"
                        else:
                            icon = "📄"
                            style = "white"
                    
                    label = f"{icon} {item.name}"
                    node = self._tree_widget.root.add(label, data=item)
                    
                    # 为目录添加占位符
                    if item.is_dir():
                        try:
                            # 检查是否有内容
                            if any(item.iterdir()):
                                node.add("...", data=None)
                        except (PermissionError, OSError):
                            node.add("🔒", data=None)
                            
                except Exception:
                    continue
            
            # 展开根节点
            self._tree_widget.root.expand()
            
            # 更新路径显示
            path_widget = self.query_one("#path_display", Static)
            path_widget.update(f"📁 {self.start_path} ({len(items)} items)")
            
        except Exception as e:
            # 错误处理
            if self._tree_widget.root:
                self._tree_widget.root.set_label(f"❌ Error: {str(e)[:50]}")
    
    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """处理节点选择"""
        node = event.node
        path = node.data
        
        if path and path.is_dir():
            # 切换到选择的目录
            self.start_path = path
            self.populate_tree()
    
    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        """处理节点展开"""
        node = event.node
        path = node.data
        
        if path and path.is_dir():
            # 移除占位符并添加实际内容
            if len(node.children) == 1 and node.children[0].data is None:
                node.remove_children()
                self.add_directory_children(node, path)
    
    def add_directory_children(self, node, path: Path):
        """为目录节点添加子项"""
        try:
            items = list(path.iterdir())
            
            # 过滤隐藏文件
            if not self.show_hidden:
                items = [item for item in items if not item.name.startswith('.')]
            
            # 排序并限制
            items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            items = items[:20]
            
            for item in items:
                try:
                    icon = "📁" if item.is_dir() else "📄"
                    label = f"{icon} {item.name}"
                    child_node = node.add(label, data=item)
                    
                    # 为子目录添加占位符
                    if item.is_dir():
                        try:
                            if any(item.iterdir()):
                                child_node.add("...", data=None)
                        except (PermissionError, OSError):
                            child_node.add("🔒", data=None)
                except Exception:
                    continue
                    
        except Exception:
            node.add("❌ Error", data=None)
    
    def watch_show_hidden(self, show_hidden: bool) -> None:
        """响应隐藏文件显示选项变化"""
        self.populate_tree()
    
    def action_quit(self):
        """退出应用"""
        self.exit()
    
    def action_refresh(self):
        """刷新"""
        self.populate_tree()
    
    def action_toggle_hidden(self):
        """切换隐藏文件显示"""
        self.show_hidden = not self.show_hidden
    
    def action_go_up(self):
        """返回上级目录"""
        parent = self.start_path.parent
        if parent != self.start_path:  # 不在根目录
            self.start_path = parent
            self.populate_tree()

if __name__ == "__main__":
    print("🚀 启动简化Tree应用...")
    print("📏 此版本针对受限终端环境优化")
    
    try:
        app = SimpleTreeApp()
        app.run()
        print("✅ 应用正常退出")
    except Exception as e:
        print(f"❌ 应用出错: {e}")
        import traceback
        traceback.print_exc() 