# Contributing to AI Customer Support Chatbot

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Specify your environment (OS, Python version, etc.)
- Provide error messages and logs

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Explain how it would work

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## 📋 Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/AI-Customer-Support-Chatbot.git
cd AI-Customer-Support-Chatbot

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/
```

## 🎨 Code Style

- Follow PEP 8 guidelines
- Use `black` for formatting
- Use `flake8` for linting
- Add type hints where possible
- Write docstrings for functions/classes

```bash
# Format code
black src/ app.py

# Check linting
flake8 src/ app.py

# Type checking
mypy src/
```

## ✅ Testing

- Write tests for new features
- Maintain test coverage above 80%
- Run tests before submitting PR

```bash
pytest tests/ -v --cov=src
```

## 📝 Documentation

- Update README.md if needed
- Add docstrings to functions
- Update relevant docs in `docs/`
- Include examples for new features

## 🏷️ Commit Messages

Follow conventional commits:
```
feat: Add new feature
fix: Bug fix
docs: Documentation changes
style: Code style changes
refactor: Code refactoring
test: Test additions/changes
chore: Maintenance tasks
```

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing! 🎉

