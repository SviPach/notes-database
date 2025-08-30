import builtins

def indented_io(prefix="    "):
    def decorator(func):
        def wrapper(*args, enable=True, **kwargs):
            old_print = builtins.print
            old_input = builtins.input

            if enable:
                builtins.print = lambda *a, **k: old_print(
                    prefix, *a, **k, sep=''
                )
                builtins.input = lambda prompt="": old_input(prefix + prompt)

            try:
                return func(*args, **kwargs)
            finally:
                if enable:
                    builtins.print = old_print
                    builtins.input = old_input
        return wrapper
    return decorator
