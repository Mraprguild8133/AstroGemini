# Contributing to Multi-AI Telegram Bot

Thank you for your interest in contributing to the Multi-AI Telegram Bot! This document provides guidelines and information for contributors.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Contributing Process](#contributing-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Be collaborative and constructive
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Git
- Basic understanding of Telegram bots
- Familiarity with AI APIs (Gemini AI, Together AI)

### Areas for Contribution
- **Bug Fixes**: Help fix reported issues
- **New Features**: Add new functionality to the bot
- **AI Integration**: Add support for new AI services
- **Documentation**: Improve guides and documentation
- **Testing**: Add tests and improve test coverage
- **Performance**: Optimize bot performance and resource usage
- **Deployment**: Improve deployment guides and configurations

## Development Environment Setup

1. **Fork the repository:**
   ```bash
   git clone https://github.com/yourusername/multi-ai-telegram-bot.git
   cd multi-ai-telegram-bot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements_external.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your development API keys
   ```

5. **Test the setup:**
   ```bash
   python -c "import bot; print('Setup successful')"
   ```

## Contributing Process

### 1. Create an Issue
Before starting work, create an issue describing:
- The problem you're solving
- Your proposed solution
- Any breaking changes

### 2. Fork and Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number
```

### 3. Make Changes
- Follow the coding standards below
- Add tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 4. Commit Changes
Use clear, descriptive commit messages:
```bash
git add .
git commit -m "Add support for new AI service integration"
```

### 5. Push and Create PR
```bash
git push origin your-branch-name
```
Create a Pull Request using the provided template.

## Coding Standards

### Python Style
- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 88 characters (Black formatter)
- Use descriptive variable and function names

### Code Organization
- Keep functions focused and small
- Use docstrings for all public functions
- Organize imports: standard library, third-party, local
- Use meaningful comments for complex logic

### Example:
```python
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

async def process_user_message(
    user_id: int, 
    message: str, 
    ai_service: str = "gemini"
) -> Optional[str]:
    """
    Process a user message with the specified AI service.
    
    Args:
        user_id: Telegram user ID
        message: User's message text
        ai_service: AI service to use ("gemini" or "together")
        
    Returns:
        AI-generated response or None if processing fails
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Error processing message for user {user_id}: {e}")
        return None
```

### File Structure
- New AI services: Create separate service files following the pattern
- Bot commands: Add to the main bot class
- Configuration: Update `config.py` and environment examples
- Documentation: Update relevant `.md` files

## Testing Guidelines

### Running Tests
```bash
# Test bot functionality
python dual_ai_demo.py

# Test feature demonstration  
python demo_bot_features.py

# Test Docker build
docker build -t test-bot .
```

### Writing Tests
- Test new functionality with example scenarios
- Test error handling and edge cases
- Verify AI service integrations work correctly
- Test environment variable configurations

### Test Coverage
- Aim for comprehensive test coverage
- Test both success and failure cases
- Mock external API calls for reliable testing

## Documentation

### What to Document
- New features and commands
- Configuration changes
- API integrations
- Deployment procedures
- Troubleshooting information

### Documentation Files
- `README.md`: Main project documentation
- `DEPLOYMENT.md`: Deployment guides
- `docker-deployment-guide.md`: Docker-specific deployment
- Code comments: Inline documentation

### Documentation Style
- Use clear, concise language
- Provide examples and code snippets
- Include troubleshooting information
- Keep documentation up-to-date with code changes

## Specific Contribution Areas

### Adding New AI Services
1. Create a new service file (e.g., `openai_service.py`)
2. Follow the existing service pattern
3. Add configuration options
4. Update bot command handling
5. Add to deployment documentation

### Bot Commands
1. Add command handlers to `bot.py`
2. Follow existing command patterns
3. Add help text and examples
4. Update command documentation

### Deployment Improvements
1. Test on different platforms
2. Update deployment guides
3. Add configuration examples
4. Document troubleshooting steps

## Review Process

### Pull Request Reviews
- Code quality and style
- Functionality testing
- Documentation completeness
- Breaking change assessment
- Performance impact

### Approval Process
- At least one maintainer review required
- All tests must pass
- Documentation must be updated
- No unresolved conversations

## Getting Help

### Resources
- [Project Documentation](README.md)
- [Issue Templates](.github/ISSUE_TEMPLATE/)
- [Deployment Guides](DEPLOYMENT.md)

### Communication
- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Email: [Contact information]

### Common Questions

**Q: How do I test with real API keys?**
A: Use your own development API keys in the `.env` file. Never commit real API keys to the repository.

**Q: Can I add support for other AI services?**
A: Yes! Follow the existing service patterns and create a new service file.

**Q: How do I test webhook functionality?**
A: Use ngrok or similar tools for local testing, or deploy to a test environment.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributor statistics

Thank you for contributing to the Multi-AI Telegram Bot! 🚀