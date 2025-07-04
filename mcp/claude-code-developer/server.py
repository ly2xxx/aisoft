#!/usr/bin/env python
"""
Claude Code MCP Server - Developer Agent
Handles code generation, file analysis, and development tasks using actual Claude Code CLI
"""

import asyncio
import json
import subprocess
import sys
import os
import tempfile
import re
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
                    "output_dir": {"type": "string", "description": "Output directory", "default": "./"}
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
        ),
        Tool(
            name="ask_claude",
            description="Ask Claude Code directly for development assistance",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "Prompt to send to Claude Code"},
                    "working_dir": {"type": "string", "description": "Working directory", "default": "./"}
                },
                "required": ["prompt"]
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
    elif name == "ask_claude":
        return await ask_claude_handler(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def generate_code_handler(args: Dict[str, Any]) -> List[TextContent]:
    feature = args["feature"]
    language = args["language"]
    context = args.get("context", "")
    output_dir = args.get("output_dir", "./")
    
    try:
        # Construct a comprehensive prompt for Claude Code
        prompt_parts = [
            f"I need to implement a feature in {language}:",
            f"Feature: {feature}",
            f"Output directory: {output_dir}",
        ]
        
        if context:
            prompt_parts.append(f"Additional context: {context}")
        
        prompt_parts.extend([
            "",
            "Please:",
            "1. Create the necessary files for this feature",
            "2. Write clean, well-documented code",
            "3. Follow best practices for the language",
            "4. Include proper error handling",
            "5. Add comments explaining the implementation",
            "",
            "Generate the complete implementation ready for production use."
        ])
        
        full_prompt = "\n".join(prompt_parts)
        
        # Change to output directory
        original_dir = os.getcwd()
        try:
            if output_dir != "./" and os.path.exists(output_dir):
                os.chdir(output_dir)
            
            # Execute Claude Code
            result = subprocess.run(
                ["claude", "--print", full_prompt], 
                capture_output=True, 
                text=True, 
                timeout=180,
                cwd=output_dir if os.path.exists(output_dir) else original_dir
            )
            
            if result.returncode == 0:
                return [TextContent(
                    type="text",
                    text=f"✅ Code generation completed successfully!\n\nFeature: {feature}\nLanguage: {language}\nOutput Directory: {output_dir}\n\nClaude Code Response:\n{result.stdout}"
                )]
            else:
                return [TextContent(
                    type="text", 
                    text=f"❌ Code generation failed:\nError: {result.stderr}\nOutput: {result.stdout}"
                )]
        finally:
            os.chdir(original_dir)
            
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text="⏰ Code generation timed out")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

async def analyze_file_handler(args: Dict[str, Any]) -> List[TextContent]:
    file_path = args["file_path"]
    improvement_type = args.get("improvement_type", "general")
    
    try:
        if not os.path.exists(file_path):
            return [TextContent(type="text", text=f"❌ File not found: {file_path}")]
        
        # Read file content for context
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Create analysis prompt
        prompt = f"""Please analyze this code file and provide {improvement_type} improvements:

File: {file_path}

Code:
```
{file_content}
```

Please provide:
1. Code quality assessment
2. Specific improvement suggestions
3. Best practices recommendations
4. Security considerations (if applicable)
5. Performance optimization opportunities
6. Refactored code examples where beneficial

Focus on {improvement_type} improvements."""
        
        # Use Claude Code to analyze file
        result = subprocess.run(
            ["claude", "--print", prompt], 
            capture_output=True, 
            text=True, 
            timeout=120
        )
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ File analysis completed!\n\nFile: {file_path}\nImprovement Type: {improvement_type}\n\nAnalysis:\n{result.stdout}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ File analysis failed:\nError: {result.stderr}"
            )]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error analyzing file: {str(e)}")]

async def create_feature_branch_handler(args: Dict[str, Any]) -> List[TextContent]:
    feature_name = args["feature_name"]
    base_branch = args.get("base_branch", "main")
    
    try:
        # Sanitize branch name
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
        # Create comprehensive prompt for URL analysis
        prompt = f"""Please analyze the content at this URL and help me implement integration code:

URL: {url}
Target Language: {language}

Please:
1. Fetch and analyze the content at the URL
2. Identify key information relevant for {language} integration
3. Suggest implementation approach
4. Provide code examples for integration
5. Include error handling and best practices
6. Consider security implications

Generate ready-to-use {language} code for working with this URL/API."""
        
        # Use Claude Code with web fetch capability
        result = subprocess.run(
            ["claude", "--print", prompt], 
            capture_output=True, 
            text=True, 
            timeout=120
        )
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ URL content analyzed!\n\nURL: {url}\nTarget Language: {language}\n\nAnalysis and Implementation:\n{result.stdout}"
            )]
        else:
            return [TextContent(
                type="text", 
                text=f"❌ Failed to analyze URL: {url}\nError: {result.stderr}"
            )]
            
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error analyzing URL: {str(e)}")]

async def ask_claude_handler(args: Dict[str, Any]) -> List[TextContent]:
    prompt = args["prompt"]
    working_dir = args.get("working_dir", "./")
    
    try:
        # Execute Claude Code with the prompt
        result = subprocess.run(
            ["claude", "--print", prompt], 
            capture_output=True, 
            text=True, 
            timeout=120,
            cwd=working_dir
        )
        
        if result.returncode == 0:
            return [TextContent(
                type="text",
                text=f"✅ Claude Code Response:\n\n{result.stdout}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Claude Code Error:\n{result.stderr}"
            )]
            
    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text="⏰ Claude Code request timed out")]
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, 
            write_stream, 
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())