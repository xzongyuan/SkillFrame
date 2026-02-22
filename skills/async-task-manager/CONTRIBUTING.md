# Contributing to Async Task Manager

Welcome! We're excited that you're interested in contributing to the Async Task Manager skill.

## Development Setup

1. Clone the SkillFrame repository
2. Navigate to the async-task-manager skill directory
3. Install any required dependencies (if needed)

## Testing

Before submitting changes, please test your modifications:

```bash
# Test task registration
python3 task_manager.py register --name "test" --command "echo 'test'"

# Test status checking
python3 task_manager.py status --name "test"

# Test listing
python3 task_manager.py list
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions and classes
- Handle errors gracefully
- Keep functions focused and single-purpose

## Pull Requests

1. Create a new branch for your feature/fix
2. Make your changes
3. Test thoroughly
4. Submit a pull request with a clear description of what you changed and why

## Issues

If you find a bug or have a feature request, please open an issue in the main SkillFrame repository.

Thank you for contributing!