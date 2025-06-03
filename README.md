# 🌲 Terminal Tree

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Textual](https://img.shields.io/badge/Framework-Textual-green)](https://github.com/textualize/textual)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

一个基于 [Textual](https://github.com/textualize/textual) 框架的现代化终端文件系统导航器，为传统的 `tree` 命令提供交互式、彩色的用户体验。

## ✨ 特色功能

- 🌳 **交互式导航** - 使用键盘浏览文件系统，支持展开/折叠目录
- 📄 **文件预览** - 语法高亮的代码文件预览，支持多种文件格式
- 🔍 **智能路径** - 路径编辑和自动补全功能
- 🎨 **现代界面** - 基于 Textual 的美观终端用户界面
- ⚡ **多版本支持** - 完整版、简化版、紧凑版适应不同终端大小
- 🔧 **易于集成** - 可以完全替代系统的 tree 命令

## 🎬 演示

```
📁 terminal-tree/
├── 📁 terminal_tree_plugin/
│   ├── 📄 app.py (5.7KB)
│   ├── 📁 widgets/
│   │   ├── 📄 tree_view.py (8.1KB)
│   │   ├── 📄 file_preview.py (4.2KB)
│   │   └── 📄 path_input.py (6.8KB)
│   └── 📁 utils/
├── 📄 run.py (1.2KB)
└── 📄 README.md (4.5KB)
```

### 快捷键操作

- **导航**: `↑↓` 上下移动, `←→` 展开/折叠目录
- **操作**: `Enter` 进入目录, `Backspace` 返回上级
- **功能**: `g` 编辑路径, `F5` 刷新, `Ctrl+H` 显示隐藏文件
- **其他**: `Tab` 切换面板, `q` 退出

## 🚀 快速开始

### 安装

1. **克隆仓库**

   ```bash
   git clone https://github.com/yourusername/terminal-tree.git
   cd terminal-tree
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用**

   ```bash
   python run.py

   # 或指定目录
   python run.py /path/to/directory
   ```

### 系统集成（可选）

如果想要替代系统的 `tree` 命令：

```bash
# 配置 shell 别名
chmod +x scripts/setup_tree_aliases.sh
./scripts/setup_tree_aliases.sh

# 重新加载 shell 配置
source ~/.zshrc  # 或 ~/.bashrc

# 现在可以直接使用
tree              # 启动 Terminal Tree
tree /usr/local   # 在指定目录启动
```

## 📁 项目结构

```
terminal-tree/
├── terminal_tree_plugin/     # 核心应用代码
│   ├── app.py               # 主应用类
│   ├── main.py              # 入口点
│   ├── widgets/             # UI 组件
│   │   ├── tree_view.py     # 文件树组件
│   │   ├── file_preview.py  # 文件预览组件
│   │   └── path_input.py    # 路径输入组件
│   ├── utils/               # 工具函数
│   │   ├── file_utils.py    # 文件操作
│   │   └── path_utils.py    # 路径处理
│   └── styles/              # CSS 样式
│       └── app.tcss         # Textual 样式文件
├── examples/                # 不同版本示例
│   ├── simple_tree_app.py   # 简化版
│   └── compact_tree.py      # 紧凑版
├── scripts/                 # 安装和配置脚本
│   ├── setup_tree_aliases.sh
│   ├── install_simple_tree.sh
│   └── test_tree_setup.sh
├── run.py                   # 主启动脚本
├── requirements.txt         # Python 依赖
├── pyproject.toml          # 项目配置
└── README.md               # 项目说明
```

## 🛠️ 版本说明

| 版本       | 文件                          | 特点                           | 适用场景           |
| ---------- | ----------------------------- | ------------------------------ | ------------------ |
| **完整版** | `run.py`                      | 三面板布局，文件预览，语法高亮 | 日常开发，功能齐全 |
| **简化版** | `examples/simple_tree_app.py` | 双面板布局，基础功能           | 中等终端窗口       |
| **紧凑版** | `examples/compact_tree.py`    | 单面板布局，最小界面           | 小终端窗口         |

## 🔧 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/yourusername/terminal-tree.git
cd terminal-tree

# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python -m pytest tests/  # 如果有测试

# 运行应用
python run.py
```

### 代码结构

- **`terminal_tree_plugin/app.py`** - 主应用类，处理整体布局和事件
- **`terminal_tree_plugin/widgets/`** - 自定义 UI 组件
- **`terminal_tree_plugin/utils/`** - 工具函数和辅助类
- **`terminal_tree_plugin/styles/`** - Textual CSS 样式

## 🤝 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 贡献指南

- 保持代码风格一致
- 添加适当的文档和注释
- 确保新功能有相应的测试
- 更新 README 如果需要

## 📝 更新日志

### v1.0.0

- ✨ 初始发布
- 🌳 交互式文件树导航
- 📄 文件预览功能
- 🎨 现代化界面设计
- ⌨️ 完整的键盘快捷键支持

## ❓ 常见问题

**Q: 如何退出应用？**
A: 按 `q` 键或 `Ctrl+C`

**Q: 为什么看不到隐藏文件？**
A: 按 `Ctrl+H` 切换显示隐藏文件

**Q: 如何快速跳转到指定路径？**
A: 按 `g` 键进入路径编辑模式

**Q: 支持哪些文件预览？**
A: 支持文本文件、代码文件，包含语法高亮

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Will McGugan](https://github.com/willmcgugan) - 创建了出色的 Textual 框架
- [Textual](https://github.com/textualize/textual) - 现代 Python TUI 框架
- [Rich](https://github.com/textualize/rich) - 终端文本美化库

---

⭐ 如果这个项目对你有帮助，请给个 Star！

🐛 遇到问题？[提交 Issue](https://github.com/yourusername/terminal-tree/issues)

🌲 享受现代化的终端文件浏览体验！
