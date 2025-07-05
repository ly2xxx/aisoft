# MCP-Based Development Crew

This directory contains two MCP (Model Context Protocol) servers that implement a development crew system as described in the `mcp-based-dev-crew.md` design document.

## 🏗️ Architecture

```
Claude Desktop (Coordinator)
├── Claude Code MCP Server (Developer Agent)
└── Gemini CLI MCP Server (QA Agent)
```

## 📁 Contents

- `claude-code-developer/server.py` - Developer agent using Claude Code CLI
- `gemini-qa-agent/server.py` - QA agent using Gemini CLI
- `claude_desktop_config.json` - Configuration for Claude Desktop (Linux/WSL)
- `windows_claude_desktop_config.json` - Configuration for Claude Desktop on Windows (system Python)
- `windows_venv_claude_desktop_config.json` - Configuration for Claude Desktop on Windows (virtual environment)
- `wsl_claude_desktop_config.json` - Configuration for Claude Desktop on Windows using WSL
- `test_servers.py` - Test script to verify MCP servers work correctly
- `README.md` - This documentation

## 🚀 Setup Instructions

### Prerequisites

1. **Python 3.12+** with MCP library:
   
   For Linux/WSL:
   ```bash
   pip install --break-system-packages mcp
   ```
   
   For Windows (in virtual environment):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install mcp
   ```

2. **Claude Code CLI** installed and working:
   ```bash
   claude --version
   ```

3. **Gemini CLI** installed and working:
   ```bash
   gemini --help
   ```

### 🧪 Testing the Servers

Run the test script to verify both MCP servers work correctly:

For Linux/WSL:
```bash
python3 test_servers.py
```

For Windows:
```powershell
python test_servers.py
```

You should see:
```
🎉 All MCP servers are working correctly!
```

### 📱 Claude Desktop Configuration

#### For Linux/WSL (Direct):

Copy the contents of `claude_desktop_config.json` to your Claude Desktop configuration file, typically located at:
- Linux: `~/.config/claude-desktop/claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

#### For Windows (Direct Python):

If using system Python, copy the contents of `windows_claude_desktop_config.json`.

If using a virtual environment, copy the contents of `windows_venv_claude_desktop_config.json`.

Copy to your Claude Desktop configuration file on Windows:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

#### For Windows (using WSL):

Copy the contents of `wsl_claude_desktop_config.json` to your Claude Desktop configuration file on Windows:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Note:** Make sure to update the file paths in the configuration to match your actual installation location.

### 🔧 Making Servers Executable

```bash
chmod +x claude-code-developer/server.py
chmod +x gemini-qa-agent/server.py
```

## 🛠️ Available Tools

### Claude Code Developer Agent

- `generate_code` - Generate code for features using Claude Code CLI
- `analyze_file` - Analyze and improve existing code files
- `create_feature_branch` - Create feature branches for development
- `analyze_url_content` - Fetch and analyze web content for code generation
- `ask_claude` - Direct communication with Claude Code

### Gemini QA Agent

- `review_code` - Comprehensive code quality review
- `generate_tests` - Generate test cases with various frameworks
- `security_audit` - Perform security audits on code
- `performance_analysis` - Analyze code performance
- `code_quality_report` - Generate comprehensive quality reports
- `ask_gemini` - Direct communication with Gemini

## 📋 Usage Examples

### 1. Feature Development Workflow

```
I need to develop a new feature using my development crew:

Feature: User authentication with JWT tokens
Language: Python

Please coordinate this workflow:
1. Use claude-code-developer to create a feature branch and generate initial code
2. Use gemini-qa-agent to review the generated code for security
3. Use claude-code-developer to implement suggested improvements
4. Use gemini-qa-agent to generate comprehensive tests
5. Commit the final implementation

Execute this workflow step by step.
```

### 2. Code Review and Improvement

```
Please have my QA agent perform a comprehensive review of:
File: ./auth/jwt_handler.py
Focus: security

After the review, use claude-code-developer to implement any critical fixes.
```

### 3. URL Analysis and Implementation

```
I want to analyze a web API and implement integration code:

URL: https://api.github.com/repos/owner/repo/issues
Target Language: Python

Use claude-code-developer to:
1. Analyze the GitHub API documentation
2. Generate Python client code for the API
3. Then use gemini-qa-agent to review for security and best practices
```

## 🔍 Troubleshooting

### Server Startup Issues

1. **ImportError: No module named 'mcp'**
   ```bash
   pip install --break-system-packages mcp
   ```

2. **Claude Code not found**
   ```bash
   which claude
   # Make sure Claude Code is in your PATH
   ```

3. **Gemini not found**
   ```bash
   which gemini
   # Make sure Gemini CLI is installed and in your PATH
   ```

### Configuration Issues

1. **File paths not found**
   - Update the absolute paths in the configuration files to match your installation
   - Make sure the server files are executable

2. **WSL Path Issues**
   - Ensure the WSL paths are correct
   - Use forward slashes in paths even on Windows when using WSL

## 🧩 Integration with Claude Desktop

Once configured, the MCP servers will appear as available tools in Claude Desktop. You can then use templates like:

**Development Session Initialization:**
```
Please initialize my development crew. Check that all MCP servers are connected and provide a status report of available tools.
```

**Smart Feature Development:**
```
I want to develop: [FEATURE_DESCRIPTION]
Please use my development crew to analyze, implement, review, test, and commit this feature.
```

## 📚 Advanced Usage

The MCP servers support advanced workflows including:
- Cross-agent communication
- Workflow orchestration
- Template-based development
- Quality gates and audits
- Continuous improvement loops

See the original `mcp-based-dev-crew.md` design document for comprehensive workflow examples.

## 🤝 Contributing

To extend or modify the MCP servers:

1. Both servers follow the standard MCP protocol
2. Add new tools by implementing the `@server.list_tools()` and `@server.call_tool()` decorators
3. Test your changes using the `test_servers.py` script
4. Update this README with any new functionality

## 📄 License

This implementation is based on the MCP-based GenAI Development Crew design and is intended for development and educational purposes.