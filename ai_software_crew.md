# File Organization and Installation Guide for AI Development Crew

## Directory Structure Setup

First, create the main directory structure in your WSL2 environment:

```bash
# Create the main AI development flow directory
mkdir -p ~/.ai-dev-flow/{bin,config,scripts,templates,logs}

# Create subdirectories for organization
mkdir -p ~/.ai-dev-flow/scripts/{git,deploy,test,monitor}
mkdir -p ~/.ai-dev-flow/templates/{projects,workflows}
mkdir -p ~/.ai-dev-flow/config/{claude,gemini,shared}
```

## 1. Configuration File Placement

### Main Configuration File
**Location**: `~/.ai-dev-flow/config/.ai-dev-config.yaml`

```bash
# Create the main config file
cat > ~/.ai-dev-flow/config/.ai-dev-config.yaml << 'EOF'
tools:
  claude_code:
    model: "claude-sonnet-4"
    context_window: "large"
    auto_save: true
    code_review: true
  
  gemini_cli:
    model: "gemini-pro"
    temperature: 0.3
    safety_settings: "high"
  
  claude_desktop:
    subscription: "pro"
    integration: true

workflows:
  development:
    - requirements_analysis
    - architecture_design
    - code_generation
    - testing
    - review
    - documentation
    - deployment
  
  monitoring:
    - performance_tracking
    - error_detection
    - automated_fixes
    - reporting

automation_levels:
  code_generation: 80%
  testing: 90%
  documentation: 85%
  deployment: 70%
  monitoring: 95%
EOF
```

## 2. Bash Functions Placement

### Master Functions File
**Location**: `~/.ai-dev-flow/bin/ai-dev-functions.sh`

```bash
# Create the main functions file
cat > ~/.ai-dev-flow/bin/ai-dev-functions.sh << 'EOF'
#!/bin/bash

# AI Development Crew Functions
# Source this file in your shell configuration

# Load configuration
AI_DEV_CONFIG="$HOME/.ai-dev-flow/config/.ai-dev-config.yaml"

# Main orchestration function
ai-dev-flow() {
    local command=$1
    shift
    
    case $command in
        "init")
            ai_project_init "$@"
            ;;
        "code")
            ai_code_gen "$@"
            ;;
        "test")
            ai_test_gen "$@"
            ;;
        "review")
            ai_code_review "$@"
            ;;
        "docs")
            ai_docs_gen "$@"
            ;;
        "deploy")
            ai_deploy "$@"
            ;;
        *)
            echo "Usage: ai-dev-flow {init|code|test|review|docs|deploy} [options]"
            ;;
    esac
}

# Project initialization
ai_project_init() {
    local project_name=$1
    local project_type=${2:-"web-app"}
    
    echo "🚀 Initializing AI-powered project: $project_name"
    
    # Create project directory
    mkdir -p "$project_name"
    cd "$project_name"
    
    # Initialize with Claude Code
    if command -v claude-code &> /dev/null; then
        claude-code project init --template "$project_type" --name "$project_name"
    else
        echo "⚠️  Claude Code not found. Setting up basic structure..."
        git init
        npm init -y 2>/dev/null || python -m venv venv
    fi
    
    # Generate project structure with Gemini
    if command -v gemini &> /dev/null; then
        gemini "Generate optimal project structure for $project_type named $project_name" > project_structure.md
    fi
    
    echo "✅ Project $project_name initialized successfully"
}

# Code generation function with automatic feature branch creation
ai_code_gen() {
    local input=$1
    local language=${2:-"javascript"}
    
    if [ -z "$input" ]; then
        echo "❌ Please provide a feature name, URL, or file path"
        echo "Usage examples:"
        echo "  ai-code 'login feature' javascript"
        echo "  ai-code https://example.com/api-docs"
        echo "  ai-code ./existing-component.js"
        echo "  ai-code requirements.txt"
        return 1
    fi
    
    # Determine input type and process accordingly
    local feature_name=""
    local context_data=""
    local input_type=""
    
    if [[ "$input" =~ ^https?:// ]]; then
        # Handle web URL
        input_type="url"
        echo "🌐 Processing web URL: $input"
        
        # Extract feature name from URL
        feature_name=$(basename "$input" | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]')
        if [ -z "$feature_name" ] || [ "$feature_name" == "index" ]; then
            feature_name="web-content-$(date +%s)"
        fi
        
        # Fetch content from URL
        if command -v curl &> /dev/null; then
            echo "📥 Fetching content from URL..."
            context_data=$(curl -s -L "$input" | head -c 10000) # Limit to first 10KB
            if [ $? -eq 0 ] && [ -n "$context_data" ]; then
                echo "✅ Content fetched successfully"
            else
                echo "❌ Failed to fetch content from URL"
                return 1
            fi
        else
            echo "❌ curl not installed. Cannot fetch URL content."
            return 1
        fi
        
    elif [ -f "$input" ]; then
        # Handle file path
        input_type="file"
        echo "📁 Processing file: $input"
        
        # Extract feature name from filename
        feature_name=$(basename "$input" | sed 's/\.[^.]*$//' | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]')
        
        # Read file content
        if [ -r "$input" ]; then
            context_data=$(cat "$input")
            echo "✅ File content loaded successfully"
        else
            echo "❌ Cannot read file: $input"
            return 1
        fi
        
        # Auto-detect language from file extension
        case "$input" in
            *.js|*.jsx) language="javascript" ;;
            *.ts|*.tsx) language="typescript" ;;
            *.py) language="python" ;;
            *.go) language="go" ;;
            *.java) language="java" ;;
            *.cpp|*.cc|*.cxx) language="cpp" ;;
            *.c) language="c" ;;
            *.cs) language="csharp" ;;
            *.php) language="php" ;;
            *.rb) language="ruby" ;;
            *.rs) language="rust" ;;
            *.swift) language="swift" ;;
            *.kt) language="kotlin" ;;
            *.html) language="html" ;;
            *.css) language="css" ;;
            *.scss|*.sass) language="scss" ;;
            *.json) language="json" ;;
            *.yaml|*.yml) language="yaml" ;;
            *.md) language="markdown" ;;
            *) echo "⚠️  Could not auto-detect language, using: $language" ;;
        esac
        echo "🔍 Detected language: $language"
        
    elif [ -d "$input" ]; then
        # Handle directory path
        input_type="directory"
        echo "📂 Processing directory: $input"
        
        feature_name=$(basename "$input" | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]')
        
        # Create summary of directory structure and key files
        echo "📊 Analyzing directory structure..."
        context_data="Directory: $input\n\nStructure:\n$(tree "$input" 2>/dev/null || find "$input" -type f | head -20)\n\n"
        
        # Add content from key files (package.json, requirements.txt, etc.)
        for keyfile in "$input/package.json" "$input/requirements.txt" "$input/Cargo.toml" "$input/go.mod" "$input/pom.xml" "$input/README.md"; do
            if [ -f "$keyfile" ]; then
                context_data+="\n\nContent of $(basename "$keyfile"):\n$(head -50 "$keyfile")\n"
            fi
        done
        
        echo "✅ Directory analysis completed"
        
    else
        # Handle as regular feature description
        input_type="feature"
        feature_name=$(echo "$input" | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]')
        echo "💡 Processing feature request: $input"
    fi
    
    # Create sanitized branch name
    local branch_name="feature/$feature_name"
    
    echo "🔨 Generating code for: $input"
    echo "🌿 Creating feature branch: $branch_name"
    
    # Ensure we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ Not in a git repository. Please run 'git init' first."
        return 1
    fi
    
    # Stash any uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo "💾 Stashing uncommitted changes..."
        git stash push -m "Auto-stash before feature branch creation"
    fi
    
    # Switch to main/master branch and pull latest
    local main_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    if [ -z "$main_branch" ]; then
        main_branch="main"
        if ! git show-ref --verify --quiet refs/heads/main; then
            main_branch="master"
        fi
    fi
    
    echo "🔄 Switching to $main_branch branch..."
    git checkout "$main_branch" 2>/dev/null || git checkout -b "$main_branch"
    
    # Pull latest changes if remote exists
    if git remote | grep -q origin; then
        echo "⬇️  Pulling latest changes..."
        git pull origin "$main_branch" 2>/dev/null || echo "⚠️  Could not pull from remote"
    fi
    
    # Create and switch to feature branch
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo "⚠️  Branch $branch_name already exists. Switching to it..."
        git checkout "$branch_name"
    else
        echo "✨ Creating new branch: $branch_name"
        git checkout -b "$branch_name"
    fi
    
    # Generate code based on input type
    case $input_type in
        "url")
            generate_from_url "$input" "$context_data" "$language"
            ;;
        "file")
            generate_from_file "$input" "$context_data" "$language"
            ;;
        "directory")
            generate_from_directory "$input" "$context_data" "$language"
            ;;
        *)
            generate_from_feature "$input" "$language"
            ;;
    esac
    
    # Auto-stage generated files
    echo "📋 Staging generated files..."
    git add .
    
    echo "
🎉 Feature branch '$branch_name' created successfully!
📁 Generated files have been staged
🔍 Review the generated code and AI feedback
📝 When ready, run 'ai-commit' to commit and create merge request

Current status:
$(git status --short)
"
}

# Helper function to generate code from URL content
generate_from_url() {
    local url=$1
    local content=$2
    local language=$3
    
    echo "🤖 Analyzing URL content with Claude Code..."
    
    if command -v claude-code &> /dev/null; then
        # Create a temporary file with URL content for analysis
        local temp_file=$(mktemp)
        echo "URL: $url" > "$temp_file"
        echo "Content:" >> "$temp_file"
        echo "$content" >> "$temp_file"
        
        claude-code "Analyze this web content and generate appropriate $language code based on the requirements or API documentation found" < "$temp_file" --output ./src/
        rm "$temp_file"
        echo "✅ Claude Code generation from URL completed"
    fi
    
    # Get additional insights from Gemini
    if command -v gemini &> /dev/null; then
        echo "🔍 Getting implementation insights from Gemini..."
        echo "URL: $url\nContent:\n$content" | gemini "Analyze this web content and provide implementation recommendations for $language. Focus on API integration, data structures, and best practices." > "url_analysis_$(date +%s).md"
        echo "✅ Gemini analysis completed"
    fi
}

# Helper function to generate code from file content
generate_from_file() {
    local filepath=$1
    local content=$2
    local language=$3
    
    echo "🤖 Analyzing file content with Claude Code..."
    
    if command -v claude-code &> /dev/null; then
        claude-code "Analyze and improve this $language code, or generate complementary code based on this file" < "$filepath" --output ./src/
        echo "✅ Claude Code analysis completed"
    fi
    
    # Get improvement suggestions from Gemini
    if command -v gemini &> /dev/null; then
        echo "🔍 Getting improvement suggestions from Gemini..."
        echo "File: $filepath\nContent:\n$content" | gemini "Analyze this $language code and suggest improvements, optimizations, or complementary features. Provide specific code examples." > "file_analysis_$(date +%s).md"
        echo "✅ Gemini analysis completed"
    fi
}

# Helper function to generate code from directory analysis
generate_from_directory() {
    local dirpath=$1
    local content=$2
    local language=$3
    
    echo "🤖 Analyzing project structure with Claude Code..."
    
    if command -v claude-code &> /dev/null; then
        echo "$content" | claude-code "Analyze this project structure and generate missing components, tests, or improvements in $language" --output ./src/
        echo "✅ Claude Code project analysis completed"
    fi
    
    # Get project insights from Gemini
    if command -v gemini &> /dev/null; then
        echo "🔍 Getting project insights from Gemini..."
        echo "$content" | gemini "Analyze this project structure and suggest improvements, missing components, or architectural enhancements for a $language project." > "project_analysis_$(date +%s).md"
        echo "✅ Gemini project analysis completed"
    fi
}

# Helper function to generate code from feature description
generate_from_feature() {
    local feature=$1
    local language=$2
    
    echo "🤖 Generating code with Claude Code..."
    
    if command -v claude-code &> /dev/null; then
        claude-code generate --feature "$feature" --lang "$language" --output ./src/
        echo "✅ Claude Code generation completed"
    else
        echo "⚠️  Claude Code not available. Creating basic structure..."
        mkdir -p src
        echo "// TODO: Implement $feature" > "src/${feature// /_}.${language}"
    fi
    
    # Review and optimize with Gemini
    local latest_file=$(find ./src -name "*.${language}" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
    if command -v gemini &> /dev/null && [ -f "$latest_file" ]; then
        echo "🔍 Reviewing code with Gemini..."
        gemini "Review and optimize this $language code for production readiness, focusing on best practices, performance, and maintainability" < "$latest_file" > "gemini_review_$(date +%s).md"
        echo "✅ Gemini review completed"
    fi
}

# Test generation function
ai_test_gen() {
    local module=${1:-"all"}
    
    echo "🧪 Generating tests for module: $module"
    
    # Generate unit tests with Claude Code
    if command -v claude-code &> /dev/null; then
        claude-code test generate --module "$module" --coverage 90
        echo "✅ Unit tests generated"
    fi
    
    # Generate integration tests with Gemini
    if command -v gemini &> /dev/null; then
        gemini "Create comprehensive integration tests for module $module" --output ./tests/integration/
        echo "✅ Integration tests generated"
    fi
    
    # Run test suite
    echo "🏃 Running test suite..."
    if [ -f "package.json" ]; then
        npm test
    elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
        python -m pytest
    else
        echo "⚠️  No recognized test framework found"
    fi
}

# Code review function
ai_code_review() {
    local branch=${1:-"current"}
    
    echo "🔍 Starting AI code review for branch: $branch"
    
    # Static analysis with Claude Code
    if command -v claude-code &> /dev/null; then
        claude-code review --branch "$branch" --output claude_review.md
        echo "✅ Claude Code review completed"
    fi
    
    # Security scan with Gemini
    if command -v gemini &> /dev/null; then
        echo "🔒 Running security analysis..."
        find ./src -name "*.js" -o -name "*.py" -o -name "*.ts" | head -10 | while read file; do
            gemini "Perform security analysis on this code" < "$file" >> gemini_security.md
        done
        echo "✅ Security analysis completed"
    fi
    
    # Combine reports
    if [ -f "claude_review.md" ] && [ -f "gemini_security.md" ]; then
        cat claude_review.md gemini_security.md > final_review.md
        echo "📋 Combined review available in final_review.md"
    fi
}

# Documentation generation function
ai_docs_gen() {
    echo "📚 Generating comprehensive documentation..."
    
    # Generate API documentation with Claude Code
    if command -v claude-code &> /dev/null; then
        claude-code docs api --format openapi
        claude-code docs readme --comprehensive
        echo "✅ API documentation generated"
    fi
    
    # Create user guides with Gemini
    if command -v gemini &> /dev/null; then
        gemini "Generate comprehensive user documentation based on this codebase" --context ./src/ --output ./docs/user-guide.md
        echo "✅ User documentation generated"
    fi
}

# Deployment function
ai_deploy() {
    local environment=${1:-"staging"}
    
    echo "🚀 Preparing deployment to: $environment"
    
    # Generate deployment scripts with Claude Code
    if command -v claude-code &> /dev/null; then
        claude-code deploy generate --env "$environment"
        echo "✅ Deployment scripts generated"
    fi
    
    # Validate configuration with Gemini
    if command -v gemini &> /dev/null && [ -f "./deploy.sh" ]; then
        gemini "Review this deployment script for best practices and security" < ./deploy.sh > deployment_review.md
        echo "✅ Deployment review completed"
    fi
    
    echo "📋 Review deployment_review.md before proceeding with actual deployment"
}

# Enhanced Git workflow functions
ai_git_commit() {
    echo "📝 AI-powered commit and merge request creation..."
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ Not in a git repository"
        return 1
    fi
    
    # Get current branch info
    local current_branch=$(git branch --show-current)
    local main_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    if [ -z "$main_branch" ]; then
        main_branch="main"
        if ! git show-ref --verify --quiet refs/heads/main; then
            main_branch="master"
        fi
    fi
    
    echo "📍 Current branch: $current_branch"
    echo "🎯 Target branch: $main_branch"
    
    # Check if we're on a feature branch
    if [[ "$current_branch" == "$main_branch" ]] || [[ "$current_branch" == "master" ]]; then
        echo "⚠️  You're on the main branch. Please create a feature branch first with 'ai-code'"
        return 1
    fi
    
    # Check if there are staged changes
    if git diff-index --quiet --cached HEAD --; then
        echo "⚠️  No staged changes found. Please stage your changes first or run 'ai-code' to generate new features."
        return 1
    fi
    
    # Get git diff for AI analysis
    local staged_changes=$(git diff --cached --name-only)
    local diff_content=$(git diff --cached)
    
    echo "📊 Analyzing staged changes..."
    echo "Modified files: $staged_changes"
    
    # Generate commit message with Claude Code
    local commit_msg=""
    if command -v claude-code &> /dev/null; then
        echo "🤖 Generating commit message with Claude Code..."
        commit_msg=$(echo "$diff_content" | claude-code git commit-message --stdin 2>/dev/null || echo "")
        
        if [ -z "$commit_msg" ]; then
            # Fallback: analyze changes with file names
            commit_msg=$(claude-code "Generate a conventional commit message for changes in: $staged_changes" 2>/dev/null || echo "")
        fi
    fi
    
    # Fallback to Gemini if Claude Code fails
    if [ -z "$commit_msg" ] && command -v gemini &> /dev/null; then
        echo "🤖 Generating commit message with Gemini..."
        commit_msg=$(echo "Generate a conventional commit message for these changes:\nFiles: $staged_changes\n\nDiff:\n$diff_content" | gemini 2>/dev/null | head -1)
    fi
    
    # Final fallback to manual input
    if [ -z "$commit_msg" ]; then
        commit_msg="feat: implement ${current_branch#feature/}"
    fi
    
    echo "💬 Suggested commit message: $commit_msg"
    read -p "Use this message? (y/n/e for edit): " confirm
    
    case $confirm in
        [eE])
            read -p "Enter your commit message: " commit_msg
            ;;
        [nN])
            read -p "Enter your commit message: " commit_msg
            ;;
        *)
            # Use suggested message
            ;;
    esac
    
    # Commit the changes
    echo "💾 Committing changes..."
    git commit -m "$commit_msg"
    
    if [ $? -eq 0 ]; then
        echo "✅ Commit successful"
        
        # Push the feature branch
        echo "⬆️  Pushing feature branch to remote..."
        git push origin "$current_branch" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "✅ Branch pushed successfully"
            
            # Create merge request (different commands for different platforms)
            create_merge_request "$current_branch" "$main_branch" "$commit_msg"
        else
            echo "⚠️  Failed to push branch. You may need to set up remote or push manually:"
            echo "   git push origin $current_branch"
        fi
    else
        echo "❌ Commit failed"
        return 1
    fi
}

# Function to create merge requests on different platforms
create_merge_request() {
    local feature_branch=$1
    local target_branch=$2
    local commit_msg=$3
    
    echo "🔀 Creating merge request..."
    
    # Detect git hosting platform
    local remote_url=$(git remote get-url origin 2>/dev/null)
    
    if [[ "$remote_url" == *"github.com"* ]]; then
        create_github_pr "$feature_branch" "$target_branch" "$commit_msg"
    elif [[ "$remote_url" == *"gitlab"* ]]; then
        create_gitlab_mr "$feature_branch" "$target_branch" "$commit_msg"
    else
        echo "📋 Manual merge request creation required:"
        echo "   Feature branch: $feature_branch"
        echo "   Target branch: $target_branch"
        echo "   Commit message: $commit_msg"
        echo ""
        echo "🌐 Open your git hosting platform and create a merge request manually"
    fi
}

# GitHub Pull Request creation
create_github_pr() {
    local feature_branch=$1
    local target_branch=$2
    local commit_msg=$3
    
    # Check if GitHub CLI is available
    if command -v gh &> /dev/null; then
        echo "🐙 Creating GitHub Pull Request with GitHub CLI..."
        
        # Generate PR description with AI
        local pr_description=""
        if command -v gemini &> /dev/null; then
            pr_description=$(echo "Create a professional pull request description for: $commit_msg" | gemini 2>/dev/null)
        fi
        
        if [ -z "$pr_description" ]; then
            pr_description="Automated pull request for feature: ${feature_branch#feature/}"
        fi
        
        gh pr create --title "$commit_msg" --body "$pr_description" --base "$target_branch" --head "$feature_branch"
        
        if [ $? -eq 0 ]; then
            echo "✅ GitHub Pull Request created successfully!"
            gh pr view --web
        else
            echo "❌ Failed to create GitHub PR automatically"
        fi
    else
        echo "💡 GitHub CLI not installed. Manual PR creation:"
        echo "   Go to: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]//' | sed 's/.git$//')/compare/$target_branch...$feature_branch"
    fi
}

# GitLab Merge Request creation
create_gitlab_mr() {
    local feature_branch=$1
    local target_branch=$2
    local commit_msg=$3
    
    # Check if GitLab CLI is available
    if command -v glab &> /dev/null; then
        echo "🦊 Creating GitLab Merge Request with GitLab CLI..."
        
        # Generate MR description with AI
        local mr_description=""
        if command -v gemini &> /dev/null; then
            mr_description=$(echo "Create a professional merge request description for: $commit_msg" | gemini 2>/dev/null)
        fi
        
        if [ -z "$mr_description" ]; then
            mr_description="Automated merge request for feature: ${feature_branch#feature/}"
        fi
        
        glab mr create --title "$commit_msg" --description "$mr_description" --source-branch "$feature_branch" --target-branch "$target_branch"
        
        if [ $? -eq 0 ]; then
            echo "✅ GitLab Merge Request created successfully!"
        else
            echo "❌ Failed to create GitLab MR automatically"
        fi
    else
        echo "💡 GitLab CLI not installed. Manual MR creation available in GitLab web interface"
    fi
}

# Additional git workflow helpers
ai_git_status() {
    echo "📊 AI-Enhanced Git Status"
    echo "=========================="
    
    local current_branch=$(git branch --show-current)
    local main_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    
    echo "📍 Current branch: $current_branch"
    echo "🎯 Main branch: $main_branch"
    echo ""
    
    git status --short
    
    # Show branch relationship
    if [[ "$current_branch" != "$main_branch" ]]; then
        echo ""
        echo "🔄 Branch comparison with $main_branch:"
        git log --oneline "$main_branch".."$current_branch" 2>/dev/null || echo "   No commits ahead"
    fi
}

ai_git_cleanup() {
    echo "🧹 Cleaning up merged feature branches..."
    
    local main_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    
    # Switch to main branch
    git checkout "$main_branch"
    git pull origin "$main_branch" 2>/dev/null
    
    # Delete merged local branches
    git branch --merged | grep -v "\*\|$main_branch\|master" | xargs -n 1 git branch -d 2>/dev/null
    
    echo "✅ Cleanup completed"
}

# Export functions for use in other scripts
export -f ai-dev-flow ai_project_init ai_code_gen ai_test_gen ai_code_review ai_docs_gen ai_deploy ai_git_commit
EOF

# Make the functions file executable
chmod +x ~/.ai-dev-flow/bin/ai-dev-functions.sh
```

### Individual Script Files
Create separate files for each major function category:

```bash
# Code generation script
cat > ~/.ai-dev-flow/scripts/code-gen.sh << 'EOF'
#!/bin/bash
# Advanced code generation with multiple AI models
source ~/.ai-dev-flow/bin/ai-dev-functions.sh

# Add more specialized code generation functions here
EOF

# Testing script
cat > ~/.ai-dev-flow/scripts/test-automation.sh << 'EOF'
#!/bin/bash
# Comprehensive testing automation
source ~/.ai-dev-flow/bin/ai-dev-functions.sh

# Add more specialized testing functions here
EOF

# Make all scripts executable
chmod +x ~/.ai-dev-flow/scripts/*.sh
```

## 3. Shell Configuration Setup

### For Bash Users
Add to `~/.bashrc`:

```bash
# Add these lines to the end of ~/.bashrc
echo '
# AI Development Crew Configuration
export AI_DEV_FLOW_HOME="$HOME/.ai-dev-flow"
export PATH="$AI_DEV_FLOW_HOME/bin:$PATH"

# Load AI development functions
if [ -f "$AI_DEV_FLOW_HOME/bin/ai-dev-functions.sh" ]; then
    source "$AI_DEV_FLOW_HOME/bin/ai-dev-functions.sh"
fi

# AI Development aliases
alias ai-init="ai-dev-flow init"
alias ai-code="ai-dev-flow code"
alias ai-test="ai-dev-flow test"
alias ai-review="ai-dev-flow review"
alias ai-docs="ai-dev-flow docs"
alias ai-deploy="ai-dev-flow deploy"
alias ai-commit="ai_git_commit"
alias ai-status="ai_git_status"
alias ai-cleanup="ai_git_cleanup"
' >> ~/.bashrc
```

### For Zsh Users
Add to `~/.zshrc`:

```bash
# Add these lines to the end of ~/.zshrc
echo '
# AI Development Crew Configuration
export AI_DEV_FLOW_HOME="$HOME/.ai-dev-flow"
export PATH="$AI_DEV_FLOW_HOME/bin:$PATH"

# Load AI development functions
if [ -f "$AI_DEV_FLOW_HOME/bin/ai-dev-functions.sh" ]; then
    source "$AI_DEV_FLOW_HOME/bin/ai-dev-functions.sh"
fi

# AI Development aliases
alias ai-init="ai-dev-flow init"
alias ai-code="ai-dev-flow code"
alias ai-test="ai-dev-flow test"
alias ai-review="ai-dev-flow review"
alias ai-docs="ai-dev-flow docs"
alias ai-deploy="ai-dev-flow deploy"
alias ai-commit="ai_git_commit"
' >> ~/.zshrc
```

## 4. Environment Variables Setup

Create a dedicated environment file:

```bash
# Create environment variables file
cat > ~/.ai-dev-flow/config/.env << 'EOF'
# AI Development Crew Environment Variables
# Note: Claude Code and Gemini CLI are already configured in WSL2
export AI_DEV_FLOW_HOME="$HOME/.ai-dev-flow"
export AI_DEV_LOG_LEVEL="INFO"
export AI_DEV_AUTO_COMMIT="false"
export AI_DEV_AUTO_DEPLOY="false"

# Tool-specific configurations (using existing CLI tools)
export CLAUDE_CODE_MODEL="claude-sonnet-4"
export GEMINI_MODEL="gemini-pro"
export CLAUDE_CODE_CONTEXT_WINDOW="large"
export GEMINI_TEMPERATURE="0.3"

# Workflow preferences
export AI_DEV_DEFAULT_LANGUAGE="javascript"
export AI_DEV_DEFAULT_FRAMEWORK="react"
export AI_DEV_TEST_COVERAGE_TARGET="90"
export AI_DEV_AUTO_FORMAT="true"
EOF

# Source the environment file in your shell config
echo 'source ~/.ai-dev-flow/config/.env' >> ~/.bashrc  # or ~/.zshrc
```

## 5. Installation Verification Script

Create a verification script to ensure everything is set up correctly:

```bash
cat > ~/.ai-dev-flow/bin/verify-setup.sh << 'EOF'
#!/bin/bash

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
🎉 Setup verification complete!

Next steps:
1. Restart your shell or run: source ~/.bashrc (or ~/.zshrc)
2. Test with: ai-dev-flow init test-project
3. Verify Claude Code and Gemini CLI are working: claude-code --version && gemini --version
"
EOF

chmod +x ~/.ai-dev-flow/bin/verify-setup.sh
```

## 6. Quick Installation Commands

Run these commands to set up everything at once:

```bash
# Create directory structure
mkdir -p ~/.ai-dev-flow/{bin,config,scripts,templates,logs}
mkdir -p ~/.ai-dev-flow/scripts/{git,deploy,test,monitor}
mkdir -p ~/.ai-dev-flow/templates/{projects,workflows}
mkdir -p ~/.ai-dev-flow/config/{claude,gemini,shared}

# Download or create the configuration files (run the cat commands above)
# Then reload your shell configuration
source ~/.bashrc  # or source ~/.zshrc

# Verify setup
~/.ai-dev-flow/bin/verify-setup.sh
```

## 7. Usage Examples

After setup, you can use the system like this:

```bash
# Initialize a new AI-powered project
ai-init my-awesome-app web-app

# Generate code for a specific feature
ai-code "user authentication" javascript

# Run comprehensive testing
ai-test auth-module

# Perform AI code review
ai-review main

# Generate documentation
ai-docs

# AI-powered git commit
ai-commit

# Deploy with AI assistance
ai-deploy staging
```

This organization keeps everything modular, maintainable, and easy to extend. The functions are automatically available in any new shell session, and the configuration can be easily modified as your needs evolve.