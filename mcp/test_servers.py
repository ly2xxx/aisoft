#!/usr/bin/env python3
"""
Test script for MCP servers
"""

import subprocess
import json
import asyncio
import time
import os

async def test_mcp_server(server_path, server_name):
    """Test an MCP server by starting it and checking basic functionality"""
    print(f"\n🧪 Testing {server_name}...")
    
    try:
        # Start the server process (use python instead of python3 for Windows compatibility)
        python_cmd = "python3" if os.name != "nt" else "python"
        process = subprocess.Popen(
            [python_cmd, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        await asyncio.sleep(0.5)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ {server_name} started successfully")
            
            # Terminate the process
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ {server_name} failed to start")
            if stderr:
                print(f"Error: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ {server_name} test failed: {str(e)}")
        return False

async def main():
    print("🚀 Testing MCP Servers")
    print("=" * 50)
    
    # Test both servers
    claude_result = await test_mcp_server(
        "/mnt/h/code/yl/aisoft/mcp/claude-code-developer/server.py",
        "Claude Code Developer MCP Server"
    )
    
    gemini_result = await test_mcp_server(
        "/mnt/h/code/yl/aisoft/mcp/gemini-qa-agent/server.py", 
        "Gemini QA Agent MCP Server"
    )
    
    print("\n📊 Test Results:")
    print("=" * 50)
    print(f"Claude Code Developer: {'✅ PASS' if claude_result else '❌ FAIL'}")
    print(f"Gemini QA Agent: {'✅ PASS' if gemini_result else '❌ FAIL'}")
    
    if claude_result and gemini_result:
        print("\n🎉 All MCP servers are working correctly!")
        return True
    else:
        print("\n⚠️  Some MCP servers have issues. Check the error messages above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)