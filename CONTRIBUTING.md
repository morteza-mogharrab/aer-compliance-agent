# Contributing to AER Compliance Agent

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first
- Describe the feature and use case
- Explain why it would be valuable

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/aer-compliance-agent.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   python3 test_agent.py
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: Feature description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Adding New Tools

To add a new agent tool:

1. **Define in `agent_tools.py`**
   ```python
   @tool
   def your_tool_name(param: str) -> str:
       """
       Clear description that the LLM reads.
       Explain when to use this tool.
       """
       # Implementation
       return result
   ```

2. **Add to tools list**
   ```python
   audit_tools.append(your_tool_name)
   ```

3. **Test it**
   ```python
   python3 agent_core.py "Use my new tool"
   ```

## Questions?

Feel free to open an issue or contact:
- Email: morteza.mgb@gmail.com
- LinkedIn: [Morteza Mogharrab](https://linkedin.com/in/morteza-mogharrab)

Thank you for contributing! 🚀