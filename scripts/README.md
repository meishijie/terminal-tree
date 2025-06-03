# Scripts - 安装和配置脚本

这个目录包含了用于安装、配置和测试 Terminal Tree 的脚本。

## 📋 脚本说明

### `setup_tree_aliases.sh` - 主配置脚本 ⭐

设置 shell 别名，将 Terminal Tree 集成到系统中。

**功能**:

- 创建 `tree` 命令别名
- 设置各版本的快捷命令
- 添加帮助函数
- 备份现有配置

**使用方式**:

```bash
chmod +x scripts/setup_tree_aliases.sh
./scripts/setup_tree_aliases.sh
source ~/.zshrc  # 重新加载配置
```

**创建的命令**:

- `tree` - 启动完整版 Terminal Tree
- `tree-simple` - 启动简化版
- `tree-compact` - 启动紧凑版
- `tree-help` - 显示帮助信息

### `install_simple_tree.sh` - 全局安装脚本

将 Terminal Tree 安装为全局命令。

**功能**:

- 在 `~/.local/bin/` 创建可执行文件
- 自动添加到 PATH
- 支持在任何目录使用

**使用方式**:

```bash
chmod +x scripts/install_simple_tree.sh
./scripts/install_simple_tree.sh
```

### `test_tree_setup.sh` - 安装验证脚本

检查 Terminal Tree 的安装状态和依赖。

**功能**:

- 检查项目文件完整性
- 验证 Python 依赖
- 测试配置状态
- 显示安装建议

**使用方式**:

```bash
chmod +x scripts/test_tree_setup.sh
./scripts/test_tree_setup.sh
```

## 🚀 快速开始

### 推荐安装流程

1. **安装依赖**:

   ```bash
   pip install -r requirements.txt
   ```

2. **配置 shell 集成**:

   ```bash
   ./scripts/setup_tree_aliases.sh
   source ~/.zshrc
   ```

3. **验证安装**:

   ```bash
   ./scripts/test_tree_setup.sh
   ```

4. **开始使用**:
   ```bash
   tree              # 启动 Terminal Tree
   tree-help         # 查看帮助
   ```

## 🔧 自定义配置

### 修改默认路径

编辑 `setup_tree_aliases.sh` 中的 `PROJECT_PATH` 变量：

```bash
PROJECT_PATH="/your/custom/path/to/terminal-tree"
```

### 添加自定义别名

在脚本中添加新的别名：

```bash
alias tree-dev='cd "$PROJECT_PATH" && python run.py --debug'
```

### 更改快捷键

修改各应用文件中的 `BINDINGS` 配置。

## 🛠️ 故障排除

### 常见问题

**Q: 脚本没有执行权限**

```bash
chmod +x scripts/*.sh
```

**Q: 找不到 Python 模块**

```bash
pip install textual rich
```

**Q: shell 配置没有生效**

```bash
source ~/.zshrc  # 或 ~/.bashrc
# 或者重启终端
```

**Q: 想要卸载配置**
手动编辑 `~/.zshrc` 文件，删除 Terminal Tree 相关的配置块。

## 📝 开发说明

这些脚本主要用于：

- 用户安装和配置
- 开发环境设置
- 部署和分发
- 自动化测试

如果需要添加新的脚本，请遵循现有的命名规范和注释风格。
