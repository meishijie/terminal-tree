# 安装指南

## 🚀 快速安装

### 方法 1: 克隆仓库（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/terminal-tree.git
cd terminal-tree

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行应用
python run.py
```

### 方法 2: 直接下载

```bash
# 下载并解压项目
wget https://github.com/yourusername/terminal-tree/archive/main.zip
unzip terminal-tree-main.zip
cd terminal-tree-main

# 安装依赖并运行
pip install -r requirements.txt
python run.py
```

## 🔧 系统集成

如果想要将 Terminal Tree 集成到系统中，可以使用以下方式：

### Shell 别名方式（推荐）

```bash
# 运行配置脚本
./scripts/setup_tree_aliases.sh

# 重新加载 shell 配置
source ~/.zshrc  # 或 ~/.bashrc

# 现在可以直接使用
tree
tree /path/to/directory
```

### 全局安装方式

```bash
# 安装为全局命令
./scripts/install_simple_tree.sh

# 添加到 PATH（如果尚未添加）
export PATH="$HOME/.local/bin:$PATH"

# 现在可以在任何地方使用
tree
```

## 📋 依赖要求

- **Python**: 3.8 或更高版本
- **textual**: >= 0.45.0
- **rich**: >= 13.0.0

## 🛠️ 开发安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/terminal-tree.git
cd terminal-tree

# 安装开发依赖
pip install -e ".[dev]"

# 安装 pre-commit 钩子
pre-commit install
```

## ❓ 常见问题

### Q: Python 版本不够

确保使用 Python 3.8+：

```bash
python --version
# 如果版本太低，尝试 python3
python3 --version
```

### Q: 依赖安装失败

尝试使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Q: 权限问题

确保脚本有执行权限：

```bash
chmod +x run.py scripts/*.sh
```

## 🔄 更新

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade
```

## 🗑️ 卸载

### 移除别名配置

编辑 `~/.zshrc` 或 `~/.bashrc`，删除 Terminal Tree 相关的配置块。

### 移除全局安装

```bash
rm -f ~/.local/bin/tree
```

### 删除项目文件

```bash
rm -rf terminal-tree/
```
