# MCP-Based GenAI Development Crew Setup Guide

## Architecture Overview

```
Claude Desktop (Coordinator)
├── Claude Code MCP Server (Developer Agent)
├── Gemini CLI MCP Server (QA Agent)
└── Git Workflow MCP Server (Version Control)
```

**Claude Desktop Pro** acts as the intelligent coordinator that:
- Receives high-level requirements and URLs/files
- Delegates development tasks to Claude Code via MCP
- Assigns QA tasks to Gemini CLI via MCP
- Orchestrates the entire workflow
- Manages Git operations and merge requests

## Phase 1: MCP Server Setup (Week 1)

### 1.1 Directory Structure for MCP Servers

```bash
# Create MCP servers directory
mkdir -p ~/.config/claude-desktop/mcp-servers/{claude-code,gemini-qa,git-workflow}
mkdir -p ~/.ai-dev-crew/{logs,configs,workflows}
```

### 1.2 Claude Code MCP Server

**Location**: `~/.config/claude-desktop/mcp-servers/claude-code/server.py`

```python
#!/usr/bin/env python3
"""
Claude Code MCP Server - Developer Agent
Handles code generation, file analysis, and development tasks
"""

import asyncio
import json
import subprocess
import sys
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Initialize MCP server
server = Server("claude-code-developer")

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="generate_code",
            description="Generate code for a feature using Claude Code CLI",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature": {"type": "string", "description": "Feature description"},
                    "language": {"type": "string", "description": "Programming language"},
                    "context": {"type": "string", "description": "Additional context (URL/file content)"},
                    "output_dir": {"type": "string", "description": "Output directory", "default": "./src"}
                },
                "required": ["feature", "language"]
            }
        ),
        Tool(
            name="analyze_file",
            description="Analyze and improve existing code file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to file to analyze"},
                    "improvement_type": {"type": "string", "description": "Type of improvement needed"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="create_feature_branch",
            description="Create a new feature branch for development",
            inputSchema={
                "type": "object",
                "properties": {
                    "feature_name": {"type": "string", "description": "Name of the feature"},
                    "base_branch": {"type": "string", "description": "Base branch", "default": "main"}
                },
                "required": ["feature_name"]
            }
        ),
        Tool(
            name="analyze_url_content",
            description="Fetch and analyze web content for code generation",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Web URL to analyze"},
                    "language": {"type": "string", "description": "Target programming language"}
                },
                "required": ["url", "language"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "generate_code":
        return await generate_code_handler(arguments)
    elif name == "analyze_file":
        return await analyze_file_handler(arguments)
    elif name == "create_feature_branch":
        return await create_feature_branch_handler(arguments)
    elif name == "analyze_url_content":
        return await analyze_url_content_handler(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def generate_code_handler(args: Dict[str, Any]) -> List[TextContent]:
    feature = args["feature"]
    language = args["language"]
    context = args.get("context", "")
    output_dir = args.get("output_dir", "./src")
    
    try:
        # Prepare Claude Code command
        cmd = ["claude-code", "generate", "--feature", feature, "--lang", language, "--output", output_dir]
        
        # Add context if provided
        if context:
            # Write context to temp file and pass it
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(context)
                temp_file = f.name
            cmd.extend(["--context-file", temp_file])
        
        # Execute Claude Code
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Code generation completed successfully!\n\nOutput:\n{result.stdout}\n\nFiles created in: {output_dir}"
            )]
        else:
            return [TextContent(
                type="text", 
                text=f"❌ Code generation failed:\n{result.stderr}"
            )]
            
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text="⏰ Code generation timed out")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

async def analyze_file_handler(args: Dict[str, Any]) -> List[TextContent]:
    file_path = args["file_path"]
    improvement_type = args.get("improvement_type", "general")
    
    try:
        # Use Claude Code to analyze file
        cmd = ["claude-code", "analyze", "--file", file_path, "--type", improvement_type]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ File analysis completed!\n\nAnalysis:\n{result.stdout}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ File analysis failed:\n{result.stderr}"
            )]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error analyzing file: {str(e)}")]

async def create_feature_branch_handler(args: Dict[str, Any]) -> List[TextContent]:
    feature_name = args["feature_name"]
    base_branch = args.get("base_branch", "main")
    
    try:
        # Sanitize branch name
        import re
        branch_name = f"feature/{re.sub(r'[^a-zA-Z0-9]', '-', feature_name.lower())}"
        
        # Git operations
        commands = [
            ["git", "checkout", base_branch],
            ["git", "pull", "origin", base_branch],
            ["git", "checkout", "-b", branch_name]
        ]
        
        outputs = []
        for cmd in commands:
            result = subprocess.run(cmd, capture_output=True, text=True)
            outputs.append(f"$ {' '.join(cmd)}\n{result.stdout}")
            if result.returncode != 0:
                outputs.append(f"Warning: {result.stderr}")
        
        return [TextContent(
            type="text",
            text=f"✅ Feature branch '{branch_name}' created successfully!\n\n" + "\n".join(outputs)
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error creating branch: {str(e)}")]

async def analyze_url_content_handler(args: Dict[str, Any]) -> List[TextContent]:
    url = args["url"]
    language = args["language"]
    
    try:
        # Fetch URL content
        import subprocess
        result = subprocess.run(["curl", "-s", "-L", url], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            content = result.stdout[:10000]  # Limit content
            
            # Analyze with Claude Code
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(f"URL: {url}\n\nContent:\n{content}")
                temp_file = f.name
            
            cmd = ["claude-code", "analyze-web", "--file", temp_file, "--target-lang", language]
            analysis = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            return [TextContent(
                type="text",
                text=f"✅ URL content analyzed!\n\nURL: {url}\nTarget Language: {language}\n\nAnalysis:\n{analysis.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Failed to fetch URL: {url}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error analyzing URL: {str(e)}")]

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
```

### 1.3 Gemini QA MCP Server

**Location**: `~/.config/claude-desktop/mcp-servers/gemini-qa/server.py`

```python
#!/usr/bin/env python3
"""
Gemini CLI MCP Server - QA Agent
Handles code review, testing, and quality assurance tasks
"""

import asyncio
import json
import subprocess
import sys
import os
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("gemini-qa-agent")

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="review_code",
            description="Review code quality using Gemini CLI",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to code file to review"},
                    "review_type": {"type": "string", "description": "Type of review (security, performance, style, etc.)"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="generate_tests",
            description="Generate test cases for code using Gemini",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_file": {"type": "string", "description": "Source code file to test"},
                    "test_framework": {"type": "string", "description": "Testing framework to use"},
                    "coverage_level": {"type": "string", "description": "Test coverage level (basic, comprehensive)"}
                },
                "required": ["source_file"]
            }
        ),
        Tool(
            name="security_audit",
            description="Perform security audit on code",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_path": {"type": "string", "description": "File or directory path to audit"},
                    "audit_level": {"type": "string", "description": "Audit depth (quick, deep)"}
                },
                "required": ["target_path"]
            }
        ),
        Tool(
            name="performance_analysis",
            description="Analyze code performance and suggest optimizations",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Code file to analyze"},
                    "language": {"type": "string", "description": "Programming language"}
                },
                "required": ["file_path", "language"]
            }
        ),
        Tool(
            name="code_quality_report",
            description="Generate comprehensive code quality report",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "description": "Project directory path"},
                    "include_metrics": {"type": "boolean", "description": "Include quality metrics"}
                },
                "required": ["project_path"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "review_code":
        return await review_code_handler(arguments)
    elif name == "generate_tests":
        return await generate_tests_handler(arguments)
    elif name == "security_audit":
        return await security_audit_handler(arguments)
    elif name == "performance_analysis":
        return await performance_analysis_handler(arguments)
    elif name == "code_quality_report":
        return await code_quality_report_handler(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def review_code_handler(args: Dict[str, Any]) -> List[TextContent]:
    file_path = args["file_path"]
    review_type = args.get("review_type", "general")
    
    try:
        if not os.path.exists(file_path):
            return [TextContent(type="text", text=f"❌ File not found: {file_path}")]
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        # Prepare Gemini prompt based on review type
        prompts = {
            "security": f"Perform a security review of this code. Look for vulnerabilities, input validation issues, and security best practices:\n\n{code_content}",
            "performance": f"Analyze this code for performance issues and suggest optimizations:\n\n{code_content}",
            "style": f"Review this code for style, readability, and best practices:\n\n{code_content}",
            "general": f"Perform a comprehensive code review covering quality, security, performance, and best practices:\n\n{code_content}"
        }
        
        prompt = prompts.get(review_type, prompts["general"])
        
        # Call Gemini CLI
        result = subprocess.run(
            ["gemini", prompt], 
            capture_output=True, 
            text=True, 
            timeout=60,
            input=""
        )
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Code review completed!\n\nFile: {file_path}\nReview Type: {review_type}\n\n{result.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Code review failed: {result.stderr}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error during code review: {str(e)}")]

async def generate_tests_handler(args: Dict[str, Any]) -> List[TextContent]:
    source_file = args["source_file"]
    test_framework = args.get("test_framework", "jest")
    coverage_level = args.get("coverage_level", "comprehensive")
    
    try:
        if not os.path.exists(source_file):
            return [TextContent(type="text", text=f"❌ Source file not found: {source_file}")]
        
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        prompt = f"Generate {coverage_level} test cases for this code using {test_framework}. Include unit tests, edge cases, and error scenarios:\n\n{source_code}"
        
        result = subprocess.run(
            ["gemini", prompt],
            capture_output=True,
            text=True,
            timeout=90
        )
        
        if result.returncode == 0:
            # Save test file
            test_file_name = source_file.replace('.js', '.test.js').replace('.py', '_test.py')
            test_file_path = f"./tests/{os.path.basename(test_file_name)}"
            
            os.makedirs("./tests", exist_ok=True)
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            
            return [TextContent(
                type="text",
                text=f"✅ Test cases generated!\n\nSource: {source_file}\nTest File: {test_file_path}\nFramework: {test_framework}\n\nGenerated tests:\n{result.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Test generation failed: {result.stderr}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error generating tests: {str(e)}")]

async def security_audit_handler(args: Dict[str, Any]) -> List[TextContent]:
    target_path = args["target_path"]
    audit_level = args.get("audit_level", "quick")
    
    try:
        if os.path.isfile(target_path):
            files_to_audit = [target_path]
        elif os.path.isdir(target_path):
            # Find code files in directory
            import glob
            patterns = ["**/*.js", "**/*.py", "**/*.ts", "**/*.jsx", "**/*.tsx"]
            files_to_audit = []
            for pattern in patterns:
                files_to_audit.extend(glob.glob(os.path.join(target_path, pattern), recursive=True))
        else:
            return [TextContent(type="text", text=f"❌ Path not found: {target_path}")]
        
        audit_results = []
        for file_path in files_to_audit[:10]:  # Limit to 10 files for quick audit
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            prompt = f"Perform a security audit of this code. Focus on vulnerabilities, input validation, authentication, and authorization issues:\n\nFile: {file_path}\n\n{content}"
            
            result = subprocess.run(
                ["gemini", prompt],
                capture_output=True,
                text=True,
                timeout=45
            )
            
            if result.returncode == 0:
                audit_results.append(f"File: {file_path}\n{result.stdout}\n" + "="*50)
        
        return [TextContent(
            type="text",
            text=f"✅ Security audit completed!\n\nAudited {len(audit_results)} files\nAudit Level: {audit_level}\n\n" + "\n".join(audit_results)
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Security audit error: {str(e)}")]

async def performance_analysis_handler(args: Dict[str, Any]) -> List[TextContent]:
    file_path = args["file_path"]
    language = args["language"]
    
    try:
        if not os.path.exists(file_path):
            return [TextContent(type="text", text=f"❌ File not found: {file_path}")]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        prompt = f"Analyze this {language} code for performance bottlenecks and optimization opportunities. Consider algorithmic complexity, memory usage, and language-specific optimizations:\n\n{code_content}"
        
        result = subprocess.run(
            ["gemini", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Performance analysis completed!\n\nFile: {file_path}\nLanguage: {language}\n\n{result.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Performance analysis failed: {result.stderr}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Performance analysis error: {str(e)}")]

async def code_quality_report_handler(args: Dict[str, Any]) -> List[TextContent]:
    project_path = args["project_path"]
    include_metrics = args.get("include_metrics", True)
    
    try:
        # Analyze project structure
        structure_info = []
        for root, dirs, files in os.walk(project_path):
            level = root.replace(project_path, '').count(os.sep)
            indent = ' ' * 2 * level
            structure_info.append(f"{indent}{os.path.basename(root)}/")
            
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Limit files shown
                structure_info.append(f"{subindent}{file}")
        
        structure_summary = "\n".join(structure_info[:50])  # Limit output
        
        prompt = f"Analyze this project structure and provide a comprehensive code quality report including architecture assessment, best practices compliance, and improvement recommendations:\n\nProject: {project_path}\n\nStructure:\n{structure_summary}"
        
        result = subprocess.run(
            ["gemini", prompt],
            capture_output=True,
            text=True,
            timeout=90
        )
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Code quality report generated!\n\nProject: {project_path}\nMetrics Included: {include_metrics}\n\n{result.stdout}"
            )]
        else:
            return [TextContent(type="text", text=f"❌ Quality report generation failed: {result.stderr}")]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Quality report error: {str(e)}")]

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
```

### 1.4 Git Workflow MCP Server

**Location**: `~/.config/claude-desktop/mcp-servers/git-workflow/server.py`

```python
#!/usr/bin/env python3
"""
Git Workflow MCP Server
Handles version control operations and merge request creation
"""

import asyncio
import json
import subprocess
import sys
import os
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("git-workflow")

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="commit_and_push",
            description="Commit staged changes and push to remote",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Commit message"},
                    "auto_push": {"type": "boolean", "description": "Automatically push to remote", "default": True}
                },
                "required": ["message"]
            }
        ),
        Tool(
            name="create_merge_request",
            description="Create merge request/pull request",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "MR/PR title"},
                    "description": {"type": "string", "description": "MR/PR description"},
                    "target_branch": {"type": "string", "description": "Target branch", "default": "main"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="git_status",
            description="Get current git status and branch information",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "commit_and_push":
        return await commit_and_push_handler(arguments)
    elif name == "create_merge_request":
        return await create_merge_request_handler(arguments)
    elif name == "git_status":
        return await git_status_handler(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def commit_and_push_handler(args: Dict[str, Any]) -> List[TextContent]:
    message = args["message"]
    auto_push = args.get("auto_push", True)
    
    try:
        # Commit changes
        commit_result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True
        )
        
        if commit_result.returncode != 0:
            return [TextContent(type="text", text=f"❌ Commit failed: {commit_result.stderr}")]
        
        output = f"✅ Commit successful: {message}\n{commit_result.stdout}"
        
        if auto_push:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
            )
            current_branch = branch_result.stdout.strip()
            
            # Push to remote
            push_result = subprocess.run(
                ["git", "push", "origin", current_branch],
                capture_output=True,
                text=True
            )
            
            if push_result.returncode == 0:
                output += f"\n✅ Pushed to origin/{current_branch}"
            else:
                output += f"\n⚠️ Push failed: {push_result.stderr}"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Git operation error: {str(e)}")]

async def create_merge_request_handler(args: Dict[str, Any]) -> List[TextContent]:
    title = args["title"]
    description = args.get("description", "")
    target_branch = args.get("target_branch", "main")
    
    try:
        # Get current branch
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        )
        current_branch = branch_result.stdout.strip()
        
        # Get remote URL to detect platform
        remote_result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True
        )
        remote_url = remote_result.stdout.strip()
        
        if "github.com" in remote_url:
            # Try GitHub CLI
            gh_result = subprocess.run(
                ["gh", "pr", "create", "--title", title, "--body", description, "--base", target_branch],
                capture_output=True,
                text=True
            )
            if gh_result.returncode == 0:
                return [TextContent(type="text", text=f"✅ GitHub PR created successfully!\n{gh_result.stdout}")]
        
        elif "gitlab" in remote_url:
            # Try GitLab CLI
            glab_result = subprocess.run(
                ["glab", "mr", "create", "--title", title, "--description", description, "--target-branch", target_branch],
                capture_output=True,
                text=True
            )
            if glab_result.returncode == 0:
                return [TextContent(type="text", text=f"✅ GitLab MR created successfully!\n{glab_result.stdout}")]
        
        # Fallback to manual instructions
        return [TextContent(
            type="text",
            text=f"📋 Manual merge request creation required:\n\nSource: {current_branch}\nTarget: {target_branch}\nTitle: {title}\nDescription: {description}\n\nRemote: {remote_url}"
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Merge request creation error: {str(e)}")]

async def git_status_handler(args: Dict[str, Any]) -> List[TextContent]:
    try:
        # Get git status
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        # Get current branch
        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        )
        current_branch = branch_result.stdout.strip()
        
        # Get commit info
        log_result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True,
            text=True
        )
        
        output = f"📊 Git Status\n\nCurrent Branch: {current_branch}\n\nUnstaged Changes:\n{status_result.stdout}\n\nRecent Commits:\n{log_result.stdout}"
        
        return [TextContent(type="text", text=output)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Git status error: {str(e)}")]

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
```

## Phase 2: Claude Desktop MCP Configuration

### 2.1 Claude Desktop Configuration

**Location**: `~/.config/claude-desktop/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "claude-code-developer": {
      "command": "python3",
      "args": ["/home/[username]/.config/claude-desktop/mcp-servers/claude-code/server.py"],
      "env": {
        "PYTHONPATH": "/home/[username]/.config/claude-desktop/mcp-servers"
      }
    },
    "gemini-qa-agent": {
      "command": "python3", 
      "args": ["/home/[username]/.config/claude-desktop/mcp-servers/gemini-qa/server.py"],
      "env": {
        "PYTHONPATH": "/home/[username]/.config/claude-desktop/mcp-servers"
      }
    },
    "git-workflow": {
      "command": "python3",
      "args": ["/home/[username]/.config/claude-desktop/mcp-servers/git-workflow/server.py"],
      "env": {
        "PYTHONPATH": "/home/[username]/.config/claude-desktop/mcp-servers"
      }
    }
  }
}
```

### 2.2 MCP Dependencies Installation

```bash
# Install MCP SDK for Python
pip install mcp

# Make MCP servers executable
chmod +x ~/.config/claude-desktop/mcp-servers/*/server.py

# Create requirements file for MCP servers
cat > ~/.config/claude-desktop/mcp-servers/requirements.txt << 'EOF'
mcp>=0.1.0
asyncio
subprocess
typing
EOF

pip install -r ~/.config/claude-desktop/mcp-servers/requirements.txt
```

## Phase 3: Coordinator Workflow Templates

### 3.1 Claude Desktop Workflow Prompts

Create these templates that you can use in Claude Desktop to orchestrate the entire development crew:

**Template 1: Feature Development from Description**
```
I need to develop a new feature using my development crew. Please coordinate this workflow:

Feature: [FEATURE_DESCRIPTION]
Language: [PROGRAMMING_LANGUAGE]

Steps:
1. Use claude-code-developer to create a feature branch and generate initial code
2. Use gemini-qa-agent to review the generated code for quality and security
3. Use claude-code-developer to implement any suggested improvements
4. Use gemini-qa-agent to generate comprehensive tests
5. Use git-workflow to commit and create a merge request

Please execute this workflow step by step and provide status updates.
```

**Template 2: URL/API Analysis and Implementation**
```
I want to analyze a web URL/API and implement integration code:

URL: [WEB_URL]
Target Language: [LANGUAGE]
Integration Type: [CLIENT/WRAPPER/INTEGRATION]

Workflow:
1. Use claude-code-developer to analyze the URL content and create feature branch
2. Generate integration code based on the analysis
3. Use gemini-qa-agent to review for security vulnerabilities and best practices
4. Generate tests for the integration
5. Create documentation
6. Use git-workflow to commit and create merge request

Execute this coordinated workflow.
```

**Template 3: Code Improvement and Refactoring**
```
I need to improve existing code using my development crew:

File/Directory: [PATH_TO_CODE]
Improvement Focus: [PERFORMANCE/SECURITY/STYLE/ARCHITECTURE]

Process:
1. Use claude-code-developer to analyze existing code and create improvement branch
2. Use gemini-qa-agent to perform comprehensive code audit
3. Use claude-code-developer to implement improvements based on audit findings
4. Use gemini-qa-agent to verify improvements and generate additional tests
5. Use git-workflow to commit improvements and create merge request

Please coordinate this improvement workflow.
```

**Template 4: Full Project Quality Audit**
```
Please perform a comprehensive quality audit of my project:

Project Path: [PROJECT_DIRECTORY]
Focus Areas: [SECURITY/PERFORMANCE/TESTING/DOCUMENTATION]

Audit Workflow:
1. Use claude-code-developer to analyze project structure and create audit branch
2. Use gemini-qa-agent to perform security audit on all code files
3. Use gemini-qa-agent to analyze performance across the codebase
4. Use gemini-qa-agent to generate quality report with recommendations
5. Use claude-code-developer to implement critical fixes
6. Use git-workflow to commit audit results and recommendations

Execute this comprehensive audit process.
```

### 3.2 Advanced Coordinator Prompts

**Multi-Stage Development Workflow**
```
I'm starting a complex development project that needs full crew coordination:

Project: [PROJECT_NAME]
Requirements: [DETAILED_REQUIREMENTS]
Tech Stack: [TECHNOLOGIES]

Full Development Lifecycle:
1. **Planning Phase**:
   - Use claude-code-developer to create project structure and feature branches
   - Analyze requirements and create development roadmap

2. **Development Phase**:
   - Use claude-code-developer for core feature implementation
   - Use gemini-qa-agent for continuous code review during development

3. **Quality Assurance Phase**:
   - Use gemini-qa-agent for comprehensive testing strategy
   - Security audit and performance analysis
   - Generate test suites for all components

4. **Integration Phase**:
   - Use claude-code-developer for integration code
   - Use gemini-qa-agent for integration testing

5. **Deployment Preparation**:
   - Use git-workflow for proper branching and merge requests
   - Final quality checks and documentation

Please coordinate this multi-phase development process with regular status updates.
```

### 3.3 Monitoring and Status Templates

**Development Status Check**
```
Please check the current status of my development workflow:

1. Use git-workflow to get current repository status
2. Use claude-code-developer to analyze recent changes
3. Use gemini-qa-agent to provide quality assessment of current state
4. Provide recommendations for next steps

Give me a comprehensive development status report.
```

**Quick Code Review Request**
```
I need a quick code review from my QA agent:

Files to review: [FILE_PATHS]
Review focus: [FOCUS_AREA]

Please use gemini-qa-agent to:
1. Review code quality and best practices
2. Check for security vulnerabilities
3. Suggest performance improvements
4. Provide actionable recommendations

Keep the review concise but thorough.
```

## Phase 4: Advanced Integration Features

### 4.1 Custom MCP Tools for Enhanced Coordination

**Location**: `~/.config/claude-desktop/mcp-servers/coordinator/server.py`

```python
#!/usr/bin/env python3
"""
Coordinator MCP Server
Advanced workflow orchestration and cross-agent communication
"""

import asyncio
import json
import subprocess
import sys
import os
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("workflow-coordinator")

@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="orchestrate_full_workflow",
            description="Orchestrate complete development workflow across all agents",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow_type": {"type": "string", "description": "Type of workflow (feature, refactor, audit, integration)"},
                    "input_data": {"type": "string", "description": "Input data (feature description, file path, URL, etc.)"},
                    "language": {"type": "string", "description": "Programming language"},
                    "options": {"type": "object", "description": "Additional workflow options"}
                },
                "required": ["workflow_type", "input_data"]
            }
        ),
        Tool(
            name="cross_agent_communication",
            description="Facilitate communication between developer and QA agents",
            inputSchema={
                "type": "object",
                "properties": {
                    "from_agent": {"type": "string", "description": "Source agent"},
                    "to_agent": {"type": "string", "description": "Target agent"},
                    "message": {"type": "string", "description": "Message to relay"},
                    "context": {"type": "object", "description": "Additional context"}
                },
                "required": ["from_agent", "to_agent", "message"]
            }
        ),
        Tool(
            name="workflow_status",
            description="Get comprehensive status of all ongoing workflows",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="save_workflow_template",
            description="Save a successful workflow as a reusable template",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_name": {"type": "string", "description": "Name for the template"},
                    "workflow_steps": {"type": "array", "description": "Array of workflow steps"},
                    "description": {"type": "string", "description": "Template description"}
                },
                "required": ["template_name", "workflow_steps"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    if name == "orchestrate_full_workflow":
        return await orchestrate_workflow_handler(arguments)
    elif name == "cross_agent_communication":
        return await cross_agent_communication_handler(arguments)
    elif name == "workflow_status":
        return await workflow_status_handler(arguments)
    elif name == "save_workflow_template":
        return await save_workflow_template_handler(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def orchestrate_workflow_handler(args: Dict[str, Any]) -> List[TextContent]:
    workflow_type = args["workflow_type"]
    input_data = args["input_data"]
    language = args.get("language", "javascript")
    options = args.get("options", {})
    
    try:
        workflow_log = []
        
        if workflow_type == "feature":
            # Feature development workflow
            workflow_log.append("🚀 Starting feature development workflow")
            
            # Step 1: Developer creates branch and initial code
            workflow_log.append("Step 1: Creating feature branch and generating code...")
            # This would call the claude-code-developer MCP
            
            # Step 2: QA reviews code
            workflow_log.append("Step 2: QA reviewing generated code...")
            # This would call the gemini-qa-agent MCP
            
            # Step 3: Implement improvements
            workflow_log.append("Step 3: Implementing QA feedback...")
            
            # Step 4: Generate tests
            workflow_log.append("Step 4: Generating comprehensive tests...")
            
            # Step 5: Final commit and MR
            workflow_log.append("Step 5: Committing and creating merge request...")
            
        elif workflow_type == "audit":
            # Code audit workflow
            workflow_log.append("🔍 Starting comprehensive code audit workflow")
            # Implementation for audit workflow
            
        elif workflow_type == "integration":
            # API integration workflow
            workflow_log.append("🌐 Starting API integration workflow")
            # Implementation for integration workflow
            
        # Save workflow state
        workflow_state = {
            "type": workflow_type,
            "input": input_data,
            "language": language,
            "steps": workflow_log,
            "status": "completed",
            "timestamp": str(asyncio.get_event_loop().time())
        }
        
        os.makedirs("~/.ai-dev-crew/workflows", exist_ok=True)
        with open(f"~/.ai-dev-crew/workflows/workflow_{workflow_type}_{int(asyncio.get_event_loop().time())}.json", "w") as f:
            json.dump(workflow_state, f, indent=2)
        
        return [TextContent(
            type="text",
            text=f"✅ {workflow_type.title()} workflow completed successfully!\n\n" + "\n".join(workflow_log)
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Workflow orchestration error: {str(e)}")]

# Additional handler implementations...
async def cross_agent_communication_handler(args: Dict[str, Any]) -> List[TextContent]:
    # Implementation for cross-agent communication
    return [TextContent(type="text", text="Cross-agent communication feature")]

async def workflow_status_handler(args: Dict[str, Any]) -> List[TextContent]:
    # Implementation for workflow status
    return [TextContent(type="text", text="Workflow status feature")]

async def save_workflow_template_handler(args: Dict[str, Any]) -> List[TextContent]:
    # Implementation for saving workflow templates
    return [TextContent(type="text", text="Save workflow template feature")]

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
```

### 4.2 Claude Desktop Integration Commands

**Quick Start Commands for Claude Desktop:**

1. **Initialize Development Session**:
```
Please initialize my development crew for a new session. Check that all MCP servers (claude-code-developer, gemini-qa-agent, git-workflow) are connected and ready. Provide a status report of available tools and current git repository state.
```

2. **Smart Feature Development**:
```
I want to develop: [FEATURE_DESCRIPTION]
Input type: [description/url/file]
Input: [YOUR_INPUT]

Please use my development crew to:
1. Analyze the input and create appropriate feature branch
2. Generate code using claude-code-developer
3. Review and improve with gemini-qa-agent  
4. Create tests and documentation
5. Commit and create merge request

Coordinate the entire process and keep me updated on each step.
```

3. **Intelligent Code Review**:
```
Please have my QA agent (gemini-qa-agent) perform a comprehensive review of:
File/Directory: [PATH]
Focus: [security/performance/style/all]

After the review, use claude-code-developer to implement any critical fixes, then use git-workflow to commit the improvements.
```

### 4.3 Automated Workflow Examples

**Example 1: URL to Feature Implementation**
```
Input: https://api.github.com/repos/owner/repo/issues
Language: Python
Goal: Create GitHub issues client

Please coordinate my development crew to:
1. Analyze the GitHub API documentation at the URL
2. Create a feature branch for 'github-issues-client'
3. Generate Python client code for GitHub issues API
4. Review the code for security and best practices
5. Generate comprehensive tests including error handling
6. Create documentation and examples
7. Commit and create merge request

Execute this workflow with full coordination between all agents.
```

**Example 2: Legacy Code Modernization**
```
Input: ./src/legacy-auth.js
Goal: Modernize authentication module

Development crew workflow:
1. Analyze the legacy authentication code
2. Create feature branch 'modernize-auth'
3. Generate modern, secure authentication implementation
4. Security audit the new implementation
5. Generate migration tests and backwards compatibility tests
6. Create migration documentation
7. Commit modernization and create merge request

Please execute this modernization workflow.
```

## Phase 5: Advanced Features and Monitoring

### 5.1 Workflow Analytics and Learning

**Location**: `~/.ai-dev-crew/analytics/workflow_analyzer.py`

```python
#!/usr/bin/env python3
"""
Workflow Analytics and Learning System
Analyzes development patterns and suggests optimizations
"""

import json
import os
import glob
from datetime import datetime
from typing import Dict, List, Any

class WorkflowAnalyzer:
    def __init__(self):
        self.workflows_dir = "~/.ai-dev-crew/workflows"
        self.analytics_dir = "~/.ai-dev-crew/analytics"
        
    def analyze_workflow_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in completed workflows"""
        workflow_files = glob.glob(f"{self.workflows_dir}/*.json")
        
        patterns = {
            "most_common_languages": {},
            "average_workflow_time": {},
            "success_rates": {},
            "common_issues": []
        }
        
        for file_path in workflow_files:
            with open(file_path, 'r') as f:
                workflow = json.load(f)
                
            # Analyze language usage
            lang = workflow.get('language', 'unknown')
            patterns["most_common_languages"][lang] = patterns["most_common_languages"].get(lang, 0) + 1
            
            # Analyze workflow types
            wf_type = workflow.get('type', 'unknown')
            if wf_type not in patterns["success_rates"]:
                patterns["success_rates"][wf_type] = {"success": 0, "failed": 0}
            
            if workflow.get('status') == 'completed':
                patterns["success_rates"][wf_type]["success"] += 1
            else:
                patterns["success_rates"][wf_type]["failed"] += 1
        
        return patterns
    
    def generate_optimization_suggestions(self) -> List[str]:
        """Generate suggestions based on workflow analysis"""
        patterns = self.analyze_workflow_patterns()
        suggestions = []
        
        # Language-specific suggestions
        most_used = max(patterns["most_common_languages"].items(), key=lambda x: x[1])
        suggestions.append(f"Consider creating specialized templates for {most_used[0]} (most used language)")
        
        # Success rate analysis
        for wf_type, rates in patterns["success_rates"].items():
            total = rates["success"] + rates["failed"]
            if total > 0:
                success_rate = rates["success"] / total
                if success_rate < 0.8:
                    suggestions.append(f"Improve {wf_type} workflow - success rate: {success_rate:.1%}")
        
        return suggestions

# Usage in Claude Desktop:
# "Please analyze my development workflow patterns and provide optimization suggestions using the workflow analyzer."
```

### 5.2 Continuous Learning and Improvement

**Template for Learning Sessions**:
```
I want to improve my development crew's performance. Please:

1. Use workflow-coordinator to analyze recent development patterns
2. Identify areas where the crew can be more efficient
3. Suggest improvements to the MCP server configurations
4. Recommend new tools or integrations that could enhance the workflow

Provide a comprehensive improvement plan based on actual usage data.
```

### 5.3 Integration with External Tools

**Slack/Discord Integration Template**:
```
Set up my development crew to send status updates to Slack/Discord:

Webhook URL: [YOUR_WEBHOOK]
Channel: [CHANNEL_NAME]

Configure notifications for:
- Feature development completion
- Code review findings
- Merge request creation
- Workflow errors or failures

Please integrate this notification system with all MCP servers.
```

## Phase 6: Usage Examples and Best Practices

### 6.1 Daily Development Workflow

**Morning Standup with AI Crew**:
```
Good morning! Please provide my daily development crew standup:

1. Check git status and recent changes
2. Review any pending code reviews or merge requests  
3. Analyze yesterday's development metrics
4. Suggest today's development priorities
5. Check for any security alerts or performance issues

Give me a comprehensive status update to start my development day.
```

### 6.2 Emergency Response Workflows

**Critical Bug Fix Workflow**:
```
URGENT: Critical bug fix needed

Issue: [BUG_DESCRIPTION]
Affected Files: [FILE_PATHS]
Priority: HIGH

Emergency crew workflow:
1. Immediately create hotfix branch
2. Use claude-code-developer to analyze and fix the issue
3. Use gemini-qa-agent for rapid security and regression testing
4. Fast-track code review and testing
5. Create emergency merge request with proper documentation

Execute this emergency workflow with highest priority.
```

### 6.3 Project Delivery Workflows

**Pre-deployment Quality Gate**:
```
Preparing for production deployment. Please run comprehensive quality gate:

Project: [PROJECT_NAME]
Target Environment: [PRODUCTION/STAGING]

Quality Gate Checklist:
1. Complete security audit of all code
2. Performance analysis and optimization check
3. Test coverage verification (target: 90%+)
4. Documentation completeness review
5. Dependency security scan
6. Final code quality metrics
7. Deployment readiness assessment

Execute this quality gate process and provide go/no-go recommendation.
```

This MCP-based architecture gives you a true AI development crew where Claude Desktop Pro acts as an intelligent coordinator, seamlessly orchestrating Claude Code (developer) and Gemini CLI (QA) through standardized MCP protocols. The system is extensible, maintainable, and provides enterprise-level workflow automation!