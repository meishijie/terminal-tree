#!/bin/bash

echo "🌲 Installing simple 'tree' command globally..."

# 获取脚本所在目录的父目录作为项目路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_PATH="$(dirname "$SCRIPT_DIR")"

# 创建用户bin目录
mkdir -p "$HOME/.local/bin"

# 创建自包含的tree脚本
cat > "$HOME/.local/bin/tree" << EOF
#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# 添加项目路径
project_path = "$PROJECT_PATH"
sys.path.insert(0, project_path)

def main():
    try:
        # 检查依赖
        import textual
        import rich
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please install dependencies:")
        print("pip install textual rich")
        return 1
    
    try:
        from terminal_tree_plugin.app import TerminalTreeApp
        
        # 解析命令行参数
        start_path = Path.cwd()
        if len(sys.argv) > 1:
            provided_path = Path(sys.argv[1])
            if provided_path.exists() and provided_path.is_dir():
                start_path = provided_path
            else:
                print(f"⚠️  Warning: '{provided_path}' is not a valid directory")
                print(f"📁 Using current directory: {start_path}")
        
        # 运行应用
        app = TerminalTreeApp(start_path=start_path)
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"🔍 Make sure the project is available at: {project_path}")
        return 1

if __name__ == "__main__":
    exit(main() or 0)
EOF

# 使脚本可执行
chmod +x "$HOME/.local/bin/tree"

# 检查PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "📝 Adding $HOME/.local/bin to PATH..."
    
    # 检查shell类型
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        SHELL_CONFIG="$HOME/.bashrc"
    else
        SHELL_CONFIG="$HOME/.profile"
    fi
    
    # 添加PATH到shell配置
    echo "" >> "$SHELL_CONFIG"
    echo "# Add local bin to PATH" >> "$SHELL_CONFIG"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
    
    echo "✅ Updated $SHELL_CONFIG"
    echo "🔄 Run: source $SHELL_CONFIG"
fi

echo ""
echo "✅ Tree command installed successfully!"
echo "📍 Location: $HOME/.local/bin/tree"
echo ""
echo "🚀 Usage:"
echo "  tree           # Browse current directory"
echo "  tree /path     # Browse specific directory"
echo ""
echo "📦 Dependencies required:"
echo "  pip install textual rich"
echo ""
echo "🔄 To use immediately:"
echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
echo "  tree" 