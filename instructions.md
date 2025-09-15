# Development Instructions

## Code Documentation Guidelines

### Procedure Summary Comments

**IMPORTANT:** For every new procedure, function, or method that you create, always add a comprehensive summary comment at the beginning. This comment should include:

1. **Purpose**: What does this procedure do?
2. **Parameters**: What inputs does it accept (if any)?
3. **Return Value**: What does it return (if applicable)?
4. **Dependencies**: Any external libraries or modules required
5. **Usage Example**: A brief example of how to call/use the procedure

### Comment Format

Use the following format for Python functions:

```python
def function_name(parameters):
    """
    Summary: Brief description of what this function does
    
    Purpose: Detailed explanation of the function's purpose and behavior
    
    Parameters:
    - param1 (type): Description of parameter 1
    - param2 (type): Description of parameter 2
    
    Returns:
    - return_type: Description of what is returned
    
    Dependencies:
    - List any required imports or external dependencies
    
    Example:
    result = function_name(arg1, arg2)
    """
    # Function implementation here
```

### Why This Matters

- **Maintainability**: Makes code easier to understand and modify later
- **Collaboration**: Helps other developers understand your code quickly
- **Documentation**: Serves as built-in documentation for the codebase
- **Debugging**: Makes it easier to trace issues and understand code flow

### Enforcement

This guideline applies to:
- All new functions and methods
- Class definitions
- Complex code blocks or algorithms
- Any reusable code components

Always prioritize clear, concise documentation that explains both the "what" and the "why" of your code.
