# AI Development Crew

> The next level of AI-powered development: Building a GenAI development crew that works around the clock

An automated AI-powered software development workflow system that orchestrates multiple AI tools (Claude Code, Gemini CLI, Claude Desktop) to create a seamless development experience from ideation to deployment.

## 🚀 Quick Start

### Installation

1. **Run the setup script** (creates directory structure and configurations):
```bash
# Clone or download this repository
cd aisoft

# The system is already configured in ~/.ai-dev-flow/
# Just load the environment:
source ~/.bashrc

# Verify installation
~/.ai-dev-flow/bin/verify-setup.sh
```

2. **Available Commands**:
```bash
# Core workflow commands
ai-init <project-name> [type]     # Initialize new AI-powered project
ai-code <input> [language]        # Generate code from various inputs
ai-test [module]                  # Generate and run comprehensive tests
ai-review [branch]                # AI-powered code review
ai-docs                           # Generate documentation
ai-deploy [environment]           # Deployment assistance

# Git workflow commands  
ai-commit                         # AI-powered commit with merge request creation
ai-status                         # Enhanced git status with branch comparison
ai-cleanup                        # Clean up merged feature branches
```

## 💡 Use Case Example: Full-Stack Web Application

Based on the [GenAI Development Crew methodology](https://edisonideas.wordpress.com/2025/06/28/the-next-level-of-ai-powered-development-building-my-genai-development-crew/) and using [MCP Docker Toolkit](https://youtu.be/EmQzk2EVxGQ?si=G9MXPnkBUUvNobUz), here's how to build a complete web application:

### Step 1: Project Initialization
```bash
# Initialize a new React/Node.js project
ai-init my-web-app web-app
cd my-web-app
```

### Step 2: Feature Development with AI Crew

#### Scenario: Building a User Authentication System

**Primary Developer (Claude Code)** - Core Implementation:
```bash
# Generate authentication backend API
ai-code "user authentication API with JWT tokens" javascript

# Generate React login/signup components  
ai-code "React authentication UI components with form validation" typescript
```

**Quality Assurance Engineer (Gemini CLI)** - Review & Testing:
```bash
# Generate comprehensive tests
ai-test auth-module

# Perform security code review
ai-review feature/user-authentication-api
```

**DevOps Coordinator (Claude Desktop)** - Integration:
```bash
# Generate deployment configurations
ai-deploy staging

# Review and commit changes
ai-commit
```

### Step 3: Advanced Workflow Examples

#### Working with External APIs
```bash
# Analyze API documentation and generate integration code
ai-code "https://api.stripe.com/docs" javascript

# Generate payment processing components
ai-code "Stripe payment integration with error handling" typescript
```

#### Refactoring Existing Code
```bash
# Analyze existing codebase and suggest improvements
ai-code "./src/components/" typescript

# Review and optimize for production
ai-review main
```

#### Database Integration
```bash
# Create database models and migrations
ai-code "User model with authentication fields for MongoDB" javascript

# Generate API endpoints with proper validation
ai-code "RESTful API endpoints for user CRUD operations" typescript
```

## 🎯 AI Development Crew Roles

### 1. Claude Code - Primary Developer
- **Strengths**: Complex architectural decisions, refactoring large codebases
- **Responsibilities**: Core implementation, feature development, code generation
- **Usage**: Main code generation and development tasks

### 2. Gemini CLI - Quality Assurance Engineer  
- **Strengths**: Code review, testing, edge case detection
- **Responsibilities**: Second opinions on code quality, test generation, security analysis
- **Usage**: Code review and testing workflows

### 3. Claude Desktop with MCP - DevOps Coordinator
- **Strengths**: CI/CD coordination, GitHub integration, deployment pipelines
- **Responsibilities**: Infrastructure, deployments, workflow orchestration
- **Usage**: Deployment and integration management

## 🔧 Advanced Features

### Smart Input Processing
The system intelligently handles different input types:

```bash
# From web documentation
ai-code "https://docs.api.com/endpoints" 

# From existing files
ai-code "./existing-component.js"

# From directory analysis
ai-code "./src/components/"

# From feature descriptions
ai-code "shopping cart with persistence" react
```

### Automated Git Workflow
```bash
# Creates feature branch, generates code, stages changes
ai-code "user profile dashboard" react

# AI-generated commit messages and merge requests
ai-commit

# Intelligent branch management
ai-cleanup
```

### Multi-Language Support
```bash
ai-code "API rate limiting middleware" javascript
ai-code "user service layer" python  
ai-code "data models" typescript
ai-code "authentication service" go
```

## 📊 Benefits

- **24/7 Development**: Continuous development without human fatigue
- **Multi-Perspective Quality**: Built-in code review from multiple AI assistants
- **Cost Effective**: Augments human creativity with AI efficiency
- **Seamless Integration**: From ideation through deployment
- **Specialized Expertise**: Each AI tool focused on its strengths

## 🛠️ Configuration

### Environment Variables
Located in `~/.ai-dev-flow/config/.env`:
```bash
AI_DEV_DEFAULT_LANGUAGE="javascript"
AI_DEV_DEFAULT_FRAMEWORK="react"
AI_DEV_TEST_COVERAGE_TARGET="90"
```

### Tool Configuration
Located in `~/.ai-dev-flow/config/.ai-dev-config.yaml`:
```yaml
tools:
  claude_code:
    model: "claude-sonnet-4"
    context_window: "large"
  gemini_cli:
    model: "gemini-pro"
    temperature: 0.3
```

## 📈 Workflow Examples

### Complete Feature Development Cycle
```bash
# 1. Start new feature
ai-code "e-commerce checkout flow" react

# 2. Generate tests  
ai-test checkout-module

# 3. Security review
ai-review feature/checkout-flow

# 4. Generate documentation
ai-docs

# 5. Deploy to staging
ai-deploy staging

# 6. Commit and create PR
ai-commit
```

This system represents the future of software development: **augmenting human creativity and problem-solving with AI efficiency and consistency**, creating a development crew that never sleeps and consistently delivers high-quality code.
