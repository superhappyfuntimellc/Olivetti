# Contributing to Olivetti

Thank you for your interest in contributing to Olivetti! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Olivetti.git
   cd Olivetti
   ```

2. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and single-purpose

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage

```bash
# Run tests
pytest tests/ -v

# Run specific test file
pytest tests/test_basic.py -v
```

## Adding New Features

### Adding a New Writing Command

1. Add method to `WritingAssistant` class in `olivetti/assistant.py`
2. Add CLI command in `olivetti/cli.py`
3. Add tests in `tests/`
4. Update README.md with examples

### Adding a New AI Provider

1. Create engine class in `olivetti/ai_engine.py` inheriting from `AIEngine`
2. Update `create_engine()` factory function
3. Update documentation

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Write/update tests
4. Run tests and ensure they pass
5. Update documentation if needed
6. Commit with clear message: `git commit -m "Add feature: description"`
7. Push to your fork: `git push origin feature/your-feature`
8. Open a Pull Request

## Areas for Contribution

- **New AI Providers**: Add support for more AI services
- **Writing Commands**: Add new creative writing features
- **Voice Analysis**: Improve voice profile learning
- **Documentation**: Improve guides and examples
- **Tests**: Increase test coverage
- **UI/UX**: Improve CLI interface or add GUI
- **Performance**: Optimize AI calls and caching
- **Integration**: Add plugins for editors (VS Code, etc.)

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on the work, not the person
- Assume good intentions

## Questions?

Feel free to open an issue for:
- Bug reports
- Feature requests
- Questions about usage or development
- Suggestions for improvement

Thank you for contributing to Olivetti! 🎉
