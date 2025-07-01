#\!/bin/bash

echo "🔍 Verifying AI Development Crew Setup..."

# Check directory structure
echo "📁 Checking directory structure..."
directories=(
    "$HOME/.ai-dev-flow"
    "$HOME/.ai-dev-flow/bin"
    "$HOME/.ai-dev-flow/config"
    "$HOME/.ai-dev-flow/scripts"
    "$HOME/.ai-dev-flow/templates"
    "$HOME/.ai-dev-flow/logs"
)

for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir exists"
    else
        echo "❌ $dir missing"
    fi
done

# Check files
echo "📄 Checking configuration files..."
files=(
    "$HOME/.ai-dev-flow/config/.ai-dev-config.yaml"
    "$HOME/.ai-dev-flow/bin/ai-dev-functions.sh"
    "$HOME/.ai-dev-flow/config/.env"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

# Check if functions are loaded
echo "🔧 Checking if functions are available..."
if command -v ai-dev-flow &> /dev/null; then
    echo "✅ ai-dev-flow command available"
else
    echo "❌ ai-dev-flow command not found - restart your shell or source the config"
fi

# Check external tools
echo "🛠️  Checking external tools..."
tools=("claude-code" "gemini" "git" "node" "python3")

for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "✅ $tool available"
    else
        echo "⚠️  $tool not found (may need installation)"
    fi
done

echo "
🎉 Setup verification complete\!

Next steps:
1. Restart your shell or run: source ~/.bashrc
2. Test with: ai-dev-flow init test-project
3. Verify Claude Code and Gemini CLI are working: claude-code --version && gemini --version
"
EOF < /dev/null
