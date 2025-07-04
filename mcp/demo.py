#!/usr/bin/env python3
"""
Demo script showing MCP servers functionality
"""

import asyncio
import json
import subprocess
import tempfile
import os

async def demo_claude_code_developer():
    """Demonstrate Claude Code Developer MCP Server"""
    print("\n🔧 Claude Code Developer Demo")
    print("=" * 50)
    
    # Create a simple test file for analysis
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

# Main execution
number = 10
result = calculate_fibonacci(number)
print(f"Fibonacci of {number} is {result}")
""")
        test_file = f.name
    
    try:
        print(f"✨ Created test file: {test_file}")
        print("📝 File contains a simple Fibonacci function")
        
        # Test the MCP server by simulating tool calls
        print("\n🧪 This would normally be called via MCP protocol")
        print("📋 Available tools:")
        print("   - generate_code: Generate new code features")
        print("   - analyze_file: Analyze existing code")
        print("   - create_feature_branch: Create Git branches")
        print("   - analyze_url_content: Analyze web content")
        print("   - ask_claude: Direct Claude Code interaction")
        
        print(f"\n💡 Example: Analyzing file {test_file}")
        print("   Would perform code quality analysis and suggest improvements")
        
    finally:
        # Clean up
        os.unlink(test_file)

async def demo_gemini_qa_agent():
    """Demonstrate Gemini QA Agent MCP Server"""
    print("\n🔍 Gemini QA Agent Demo")
    print("=" * 50)
    
    # Create a test file with potential issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write("""
// Potentially problematic JavaScript code
function processUserInput(input) {
    // No input validation!
    var result = eval(input);  // Security issue!
    
    // Performance issue - unnecessary loop
    for (var i = 0; i < 1000000; i++) {
        console.log("Processing...");
    }
    
    return result;
}

// No error handling
var userInput = getUserInput();
var output = processUserInput(userInput);
document.getElementById("result").innerHTML = output;  // XSS vulnerability
""")
        test_file = f.name
    
    try:
        print(f"✨ Created test file with issues: {test_file}")
        print("⚠️  File contains security and performance issues")
        
        print("\n🧪 This would normally be called via MCP protocol")
        print("📋 Available tools:")
        print("   - review_code: Comprehensive code review")
        print("   - generate_tests: Create test suites")
        print("   - security_audit: Security vulnerability scanning")
        print("   - performance_analysis: Performance optimization")
        print("   - code_quality_report: Overall quality assessment")
        print("   - ask_gemini: Direct Gemini interaction")
        
        print(f"\n🔍 Example: Security audit of {test_file}")
        print("   Would identify:")
        print("   - eval() usage (code injection vulnerability)")
        print("   - Missing input validation")
        print("   - XSS vulnerability in DOM manipulation")
        print("   - Performance issues with unnecessary loops")
        
    finally:
        # Clean up
        os.unlink(test_file)

async def demo_workflow_integration():
    """Demonstrate integrated workflow"""
    print("\n🔄 Integrated Workflow Demo")
    print("=" * 50)
    
    print("🎯 Typical Development Workflow:")
    print("\n1. 🔧 Developer Agent (Claude Code):")
    print("   - Creates feature branch")
    print("   - Generates initial code implementation")
    print("   - Analyzes requirements from URLs/docs")
    
    print("\n2. 🔍 QA Agent (Gemini):")
    print("   - Reviews generated code for quality")
    print("   - Performs security audit")
    print("   - Generates comprehensive tests")
    print("   - Analyzes performance bottlenecks")
    
    print("\n3. 🔄 Coordinator (Claude Desktop):")
    print("   - Orchestrates the entire workflow")
    print("   - Manages communication between agents")
    print("   - Ensures quality gates are met")
    print("   - Handles Git operations and merge requests")
    
    print("\n💡 Example Prompt for Claude Desktop:")
    print('"""')
    print("I need to implement a user authentication system using JWT.")
    print("Please coordinate my development crew to:")
    print("1. Create a feature branch")
    print("2. Generate secure authentication code")
    print("3. Review for security vulnerabilities")
    print("4. Generate comprehensive tests")
    print("5. Create merge request with documentation")
    print('"""')

async def main():
    print("🚀 MCP Development Crew Demo")
    print("=" * 70)
    print("This demo shows the capabilities of the MCP-based development crew")
    print("consisting of Claude Code (Developer) and Gemini (QA) agents.")
    
    await demo_claude_code_developer()
    await demo_gemini_qa_agent()
    await demo_workflow_integration()
    
    print("\n" + "=" * 70)
    print("🎉 Demo Complete!")
    print("\nTo use these MCP servers:")
    print("1. Configure Claude Desktop with the provided JSON configs")
    print("2. Restart Claude Desktop to load the MCP servers")
    print("3. Use the example prompts to coordinate your development crew")
    print("\nFor more examples, see the README.md file.")

if __name__ == "__main__":
    asyncio.run(main())