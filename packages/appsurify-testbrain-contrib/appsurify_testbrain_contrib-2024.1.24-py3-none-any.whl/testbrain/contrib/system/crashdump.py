import io
import os
import pathlib
import pprint
import sys
import time
import traceback
from types import FrameType, TracebackType
from typing import Any, Callable, Dict, Optional, Set, TextIO, Type, Union

from testbrain.contrib.system import platform

__all__ = ["dump_report_to_file", "dump_report", "format_report", "inject_excepthook"]


def _get_main_name(prog_name=None) -> str:
    import __main__  # noqa

    if prog_name is None:
        prog_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
    return prog_name


def _write_separator(
    f: TextIO, header: str = "", before: int = 1, after: int = 1
) -> int:
    if before > 0:
        before = before + 1

    after = after + 1

    sep = "=" * 88
    new_line = "\n"
    text = f"{sep}"
    if header:
        text += f"\n# {header.upper()}\n{sep}"
    banner = f"{new_line * before}{text}{new_line * after}"
    return f.write(banner)


def _exhaustive_vars(obj: Any) -> Dict[str, Any]:
    names = dir(obj)
    result = {}
    for name in names:
        try:
            result[name] = getattr(obj, name)
        except Exception as e:
            result[name] = f"<<Failed to getattr: {e.__class__.__qualname__}: {e}>>"
    return result


def _variable_summary(f: TextIO, vars: Dict[str, Any], indent: int = 0) -> None:  # noqa
    for name, value in vars.items():
        label = f"{' ' * indent}{name} => "
        total_indent = len(label)
        formatted = pprint.pformat(value)
        formatted = formatted.replace("\n", "\n" + " " * total_indent)
        f.write(f"{label}{formatted}\n")


_RECURSIVE_CUTOFF = 1


def _trace_exchaustive(
    result: TextIO,
    exc: BaseException,
    tb: Optional[TracebackType],
    show_locals: bool,
    show_globals: bool,
    seen: Set[int],
) -> None:
    if tb is None:
        return

    seen.add(id(exc))
    last_file = None
    last_line = None
    last_name = None
    count = 0
    cause = exc.__cause__

    if cause is not None and id(cause) not in seen:
        _trace_exchaustive(
            result, cause, cause.__traceback__, show_locals, show_globals, seen
        )
        result.write(
            "The above exception was the direct cause of the following exception:\n"
        )

    context = exc.__context__

    if context is not None and id(context) not in seen and not exc.__suppress_context__:
        _trace_exchaustive(
            result,
            context,
            context.__traceback__,
            show_locals,
            show_globals,
            seen,
        )
        result.write(
            "During handling of the above exception, another exception occurred:\n"
        )

    result.write("Following is an exhaustive stack trace (most recent call last) for ")
    result.write(repr(exc))
    _write_separator(result)

    frame: FrameType

    for frame, lineno in traceback.walk_tb(tb):
        co = frame.f_code
        filename = co.co_filename
        name = co.co_name
        summary = traceback.FrameSummary(filename, lineno, name, lookup_line=True)

        if (
            last_file is None
            or last_file != filename
            or last_line is None
            or last_line != lineno
            or last_name is None
            or last_name != name
        ):
            if count > _RECURSIVE_CUTOFF:
                count -= _RECURSIVE_CUTOFF
                result.write(
                    f"  [Previous frame repeated {count} more "
                    f"time{'s' if count > 1 else ''}]\n"
                )

            last_file = filename
            last_line = lineno
            last_name = name
            count = 0

        count += 1

        if count > _RECURSIVE_CUTOFF:
            _write_separator(result)
            continue

        result.write(f"File '{filename}', line {lineno}, in {name}\n")

        if summary.line:
            result.write(f"--->  {summary.line.strip()}\n\n")

        if frame.f_locals and show_locals:
            result.write("Local variables:\n")
            _variable_summary(result, frame.f_locals)

            if frame.f_globals and show_globals:
                result.write("\n")

        if frame.f_globals and show_globals:
            result.write("Global variables:\n")
            _variable_summary(result, frame.f_globals)

        _write_separator(result)

    if count > _RECURSIVE_CUTOFF:
        count -= _RECURSIVE_CUTOFF
        result.write(
            f"  [Previous frame repeated {count} more "
            f"time{'s' if count > 1 else ''}]\n"
        )


def _recursive_exc_var_dump(
    file: TextIO, exc: BaseException, seen: Set[int], indent: int = 0
) -> None:
    seen.add(id(exc))
    vars = _exhaustive_vars(exc)  # noqa
    cause = vars.pop("__cause__")
    context = vars.pop("__context__")
    show_cause = cause is not None and id(cause) not in seen
    show_context = (
        context is not None and id(context) not in seen and not exc.__suppress_context__
    )
    _variable_summary(file, vars, indent)
    if show_cause:
        file.write(" " * indent + "__cause__ =>\n")
        _recursive_exc_var_dump(file, cause, seen, indent + 13)
    else:
        _variable_summary(file, {"__cause__": cause}, indent)
    if show_context:
        file.write(" " * indent + "__context__ =>\n")
        _recursive_exc_var_dump(file, context, seen, indent + 15)
    else:
        _variable_summary(file, {"__context__": context}, indent)


def dump_report_to_file(
    file: Union[TextIO, str],
    etype: Optional[Type[BaseException]],
    value: Optional[BaseException],
    tb: Optional[TracebackType],
    *,
    show_locals: bool = True,
    show_globals: bool = True,
    show_main_globals: bool = True,
    show_sys: bool = True,
    show_simple_tb: bool = True,
    show_exception_vars: bool = True,
    show_exc_vars_recur: bool = True,
    custom_values: Optional[Dict[str, Union[Any, Callable[[], Any]]]] = None,
) -> None:
    if isinstance(file, str):
        with open(file, "w") as fp:
            dump_report_to_file(
                fp,
                etype,
                value,
                tb,
                show_locals=show_locals,
                show_globals=show_globals,
                show_main_globals=show_main_globals,
                show_sys=show_sys,
                show_simple_tb=show_simple_tb,
                show_exception_vars=show_exception_vars,
                show_exc_vars_recur=show_exc_vars_recur,
                custom_values=custom_values,
            )
            return

    if value is None:
        value = sys.exc_info()[1]

    if value is None:
        return

    import __main__  # noqa

    etype = type(value)

    if tb is None:
        tb = value.__traceback__

    # Write name and date and additional info
    _write_separator(file, header="Main", before=0)

    argv = " ".join(sys.argv[1:])
    python_version = sys.version.replace("\n", "")

    file.write(
        # f"PKG: {testbrain.__name__} ({testbrain.__version__})\n"
        # f"PROG: {testbrain.__prog__}\n"
        f"BIN LOCATE: '{__main__.__file__}'\n"
        f"BIN ARGV: '{argv}'\n"
        f"DATE: {time.strftime('%Y-%m-%dT%H:%M:%S%z')} "
        f"({time.strftime('%F %H:%M:%S %Z')})\n"
        f"PLATFORM: {platform.platform()}\n"
        f"OS: {platform.os()}\n"
        f"VER: {platform.version()}\n"
        f"SYSTEM: {platform.system()}\n"
        f"RELEASE: {platform.release()}\n"
        f"MACHINE: {platform.machine()}\n"
        f"PROCESSOR: {platform.processor()}\n"
        f"PYTHON VER (SYS): {python_version}\n"
        f"PYTHON VER: {platform.python_version()}\n"
        f"PYTHON IMPLEMENTATION: {platform.python_implementation()}\n"
        f"PYTHON COMPILE: {platform.python_compiler()}\n"
        f"PYTHON BUILD: {platform.python_build()}\n"
        f"PYTHON REV: {platform.python_revision()}\n"
    )

    _write_separator(file, header="Traceback")

    # Write traceback
    if show_simple_tb:
        tb_lines = traceback.format_exception(etype, value, tb)
        file.write("".join(tb_lines))

    _write_separator(file, header="Custom values")

    # Prepare summary
    if custom_values is None:
        custom_values = {
            "os.getcwd()": os.getcwd,
            "os.environ": (lambda: dict(os.environ)),
        }

    for key, custom_value in custom_values.items():
        if callable(custom_value):
            custom_values[key] = custom_value()

    _variable_summary(file, custom_values)

    # _write_separator(file)

    _write_separator(file, header="Summary of exception variables")

    # Write the contents of the exception
    if show_exception_vars:
        # file.write("Summary of exception variables:\n")

        if show_exc_vars_recur:
            _recursive_exc_var_dump(file, value, set())
        else:
            _variable_summary(file, _exhaustive_vars(value))

        # _write_separator(file)

    show_exhaustive = show_locals or show_globals

    # Write an exhaustive stack trace that shows all
    # locals and globals (configurable) of the entire stack
    _write_separator(file, header="Exhaustive stack trace")
    if show_exhaustive:
        _trace_exchaustive(file, value, tb, show_locals, show_globals, set())

    # Write the main globals for the program
    # This is included in the exhaustive stack trace,
    # so we don't show it when we show an exhastive stack trace.
    elif show_main_globals:
        file.write("Summary of __main__ globals:\n")
        _variable_summary(file, _exhaustive_vars(__main__))
        _write_separator(file)

    # Write the contents of sys
    _write_separator(file, header="Summary of sys variables")
    if show_sys:
        # file.write("Summary of sys variables:\n")
        _variable_summary(file, _exhaustive_vars(sys))
        _write_separator(file)


def dump_report(
    etype: Optional[Type[BaseException]],
    value: Optional[BaseException],
    tb: Optional[TracebackType],
    *,
    show_locals: bool = True,
    show_globals: bool = True,
    show_main_globals: bool = True,
    show_sys: bool = True,
    show_simple_tb: bool = True,
    show_exception_vars: bool = True,
    show_exc_vars_recur: bool = True,
    custom_values: Optional[Dict[str, Union[Any, Callable[[], Any]]]] = None,
    prog_name: Optional[str] = None,
) -> str:
    """Dumps a report to a file named {main_filename}-%Y-%m-%d-%H-%M-%S.dump

    Returns
    -------
    The filename the report was dumped to"""

    try:
        pathlib.Path(".crashdumps").mkdir(parents=True, exist_ok=True)
        report_dir = pathlib.Path(".crashdumps").resolve()
    except Exception:  # noqa
        report_dir = pathlib.Path("..").resolve()

    _main_name = _get_main_name(prog_name=prog_name)
    filename = f"{_main_name}-{time.strftime('%Y-%m-%d-%H-%M-%S')}.dump"
    filename = os.path.join(report_dir, filename)

    dump_report_to_file(
        filename,
        etype,
        value,
        tb,
        show_locals=show_locals,
        show_globals=show_globals,
        show_main_globals=show_main_globals,
        show_sys=show_sys,
        show_simple_tb=show_simple_tb,
        show_exception_vars=show_exception_vars,
        show_exc_vars_recur=show_exc_vars_recur,
        custom_values=custom_values,
    )

    return filename


def format_report(
    etype: Optional[Type[BaseException]],
    value: Optional[BaseException],
    tb: Optional[TracebackType],
    *,
    show_locals: bool = True,
    show_globals: bool = True,
    show_main_globals: bool = True,
    show_sys: bool = True,
    show_simple_tb: bool = True,
    show_exception_vars: bool = True,
    show_exc_vars_recur: bool = True,
    custom_values: Optional[Dict[str, Union[Any, Callable[[], Any]]]] = None,
) -> str:
    """Returns a report in string form

    Returns
    -------
    The string value of the report"""
    result = io.StringIO()

    dump_report_to_file(
        result,
        etype,
        value,
        tb,
        show_locals=show_locals,
        show_globals=show_globals,
        show_main_globals=show_main_globals,
        show_sys=show_sys,
        show_simple_tb=show_simple_tb,
        show_exception_vars=show_exception_vars,
        show_exc_vars_recur=show_exc_vars_recur,
        custom_values=custom_values,
    )

    return result.getvalue()


def inject_excepthook(
    callback: Optional[
        Callable[
            [Type[BaseException], BaseException, TracebackType, Optional[str]],
            Any,
        ]
    ] = None,
    *,
    show_locals: bool = True,
    show_globals: bool = True,
    show_main_globals: bool = True,
    show_sys: bool = True,
    show_simple_tb: bool = True,
    show_exception_vars: bool = True,
    show_exc_vars_recur: bool = True,
    custom_values: Optional[Dict[str, Union[Any, Callable[[], Any]]]] = None,
    prog_name: Optional[str] = None,
    quiet: Optional[bool] = False,
) -> Callable[[Type[BaseException], BaseException, TracebackType], Any]:
    _original_excepthook = sys.excepthook

    def excepthook(etype, value, tb):
        if issubclass(etype, Exception) or issubclass(etype, BaseException):
            dest = dump_report(
                etype,
                value,
                tb,
                show_locals=show_locals,
                show_globals=show_globals,
                show_main_globals=show_main_globals,
                show_sys=show_sys,
                show_simple_tb=show_simple_tb,
                show_exception_vars=show_exception_vars,
                show_exc_vars_recur=show_exc_vars_recur,
                custom_values=custom_values,
                prog_name=prog_name,
            )

            if callback is not None:
                callback(etype, value, tb, dest)

            if quiet:
                sys.exit(0)

            sys.exit(1)

        elif callback is not None:
            callback(etype, value, tb, None)

        _original_excepthook(etype, value, tb)

    sys.excepthook = excepthook
    return _original_excepthook
