import inspect
from functools import wraps
from inspect import cleandoc
from typing import Callable, Literal

from .utils import rscompile, load_elf, populate_from_elf, elf_add_trampoline, asm_preamble

from .core import Raspsim


def _asm_or_c_decorator(
    fn: Callable[[], Raspsim],
    lang: Literal["c", "assembler"],
    code_formatter: Callable[[str], str] | None = None,
) -> Callable[[], Raspsim]:
    if not callable(fn):
        raise TypeError("Argument must be a function or a string")

    spec = inspect.getfullargspec(fn)
    if spec.args:
        raise TypeError("Function must not have arguments")

    ret = spec.annotations.get("return")
    if ret is None or not issubclass(ret, Raspsim):
        raise TypeError("Function must return a Raspsim instance")

    name = fn.__name__
    code = fn.__doc__
    if code is None:
        raise ValueError("Function must have a docstring")

    if code_formatter is not None:
        code = code_formatter(code)

    @wraps(fn)
    def wrapper() -> Raspsim:
        with rscompile(code, entry_label=name, lang=lang) as f:
            elf = load_elf(f)

        elf_add_trampoline(elf)
        sim = Raspsim()
        populate_from_elf(sim, elf)
        sim.run()
        return sim

    return wrapper


def asm(fn: Callable[[], Raspsim]) -> Callable[[], Raspsim]:
    """
    A decorator that formats a function's code as Intel syntax assembly and
    applies an assembler-specific decorator.
    Args:
        fn (Callable[[], Raspsim]): The function to be decorated.
    Returns:
        Callable[[], Raspsim]: The decorated function with assembly formatting.

    Example:
        @asm
        def one() -> Raspsim:
            \"\"\"
            mov rax, 1
            ret
            \"\"\"

        print(one().rax)
    """

    def formatter(code: str):
        return asm_preamble(fn.__name__) + code + "\n"

    return _asm_or_c_decorator(fn, "assembler", formatter)
