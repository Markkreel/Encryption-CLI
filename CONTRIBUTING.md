# Contributing to FileLock

Thank you for your interest in contributing to FileLock! We welcome contributions from the community to help make this project better.

## Development Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/YOUR-USERNAME/FileLock.git
   cd FileLock
   ```
2. **Set up Python Environment**

   - Python 3.9 or higher is required
   - Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: .\venv\Scripts\activate
     ```
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## Development Workflow

1. **Create a Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make Changes**

   - Write your code
   - Add tests for new functionality
   - Ensure all tests pass:
     ```bash
     python -m pytest tests/
     ```
3. **Code Style**

   - Follow PEP 8 guidelines
   - Use meaningful variable and function names
   - Add docstrings for functions and classes
   - Keep functions focused and concise
4. **Commit Changes**

   - Write clear, concise commit messages
   - Use present tense ("Add feature" not "Added feature")
   - Reference relevant issue numbers

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Ensure all tests pass and add new tests for new functionality
3. Update documentation if needed
4. Submit a pull request with a clear description of the changes

## Reporting Issues

- Use the GitHub issue tracker
- Include steps to reproduce the issue
- Include expected and actual behavior
- Include Python version and operating system

## Code of Conduct

Please note that this project is released with a Code of Conduct. By participating in this project you agree to abide by its terms.

## License

By contributing to FileLock, you agree that your contributions will be licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Thank you for contributing to FileLock! Your efforts help make this project better for everyone.
