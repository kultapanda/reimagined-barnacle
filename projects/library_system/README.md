# Library System Project

A practical project demonstrating Python best practices, testing, and design decisions.

## Learning Objectives
- Function vs Class design decisions
- Unit testing with PyTest
- Code organization and structure
- Type hints and documentation
- SOLID principles application

## Project Structure
```
library_system/
├── src/
│   ├── models/         # Domain models
│   ├── services/       # Business logic
│   └── repositories/   # Data access
├── tests/             # Test directory
├── requirements.txt   # Dependencies
└── README.md         # This file
```

## Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Development Guidelines
1. Write tests first (TDD approach)
2. Use type hints
3. Follow PEP 8
4. Document all public interfaces
5. Run tests with `pytest`
6. Check types with `mypy`

## Key Concepts Demonstrated
- Pure functions vs classes with state
- Repository pattern
- Dependency injection
- Test fixtures and parametrization
- Error handling patterns 