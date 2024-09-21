import inspect

def create_form(arguments: dict) -> dict:
    """ create_form: creates a dictionary out of supplied arguments (derived
    from locals()); resulting dict is in form {"arg1", arg1, ... "argN", argN}

    Args:
        arguments (dict): function arguments supplied with locals()

    Returns:
        dict: constructed dictionary/form
    """
    return {k: v for k, v in arguments.items()
            if v is not None and k != "self"}

def call_with_filtered_kwargs(func, kwargs):
    # Get the function's parameter names
    func_args = inspect.signature(func).parameters

    # Filter out kwargs that are not in the function's parameters
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in func_args}

    # Call the function with the filtered kwargs
    return func(**filtered_kwargs)