"""
function serialize and deserialize 
"""

import inspect
from collections import defaultdict
from types import FunctionType                                                                                                                                                           
from types import ModuleType
from typing import Callable
from typing import Optional
from typing import Dict
from typing import Any
from dill.detect import globalvars, freevars

def serialize_function(func: Callable) -> str:
    """
    serialize function to code
    Args:
        func: function pointer
    returns:
        source code of function
    """
    if hasattr(func, "_code"):
        code = func._code
    else:
        code = _get_source(func)

    # serialize code by dill
    # code = dill.dumps(code)
    return code

def deserialize_function(
    code: str,
    name: str,
    globals_: Optional[Dict[str, Any]] = None, 
    locals_: Optional[Dict[str, Any]] = None,
) -> Callable:
    """
    deserialize code to function
    Args:
        code: source code of function
        name: name of function
        globals_: global variables of function
        locals_: local variables of function
    returns:
        function pointer
    """

    # deserialize code by dill
    # code = dill.loads(code)
    exec(code, globals_, locals_)
    func = eval(name, globals_, locals_)
    func._code = code
    return func

def _get_source(func):
    """
    get the source code of a function
    """
    imports = defaultdict(set)
    modules = set()
    code_lines = []
    seen_args = {}

    # file the func was defined in
    func_file = inspect.getfile(inspect.getmodule(func))

    def process_functiontype(name, obj, imports, modules, code_lines, seen_args):
        module = inspect.getfile(inspect.getmodule(obj))
        # TODO: decide if we should get the source code or just import the module
        if (
            obj.__module__ in ("__main__", None)
            or "<" in obj.__qualname__
        ):
            objs = globalvars(obj, recurse=False)
            objs.update(freevars(obj))
            default_objs = {}
            for param in inspect.signature(obj).parameters.values():
                if param.default != inspect.Parameter.empty:
                    default_objs[param.name] = param.default
                    objs.pop(param.name, None)
            # need to sort the keys since globalvars ordering is non-deterministic
            for dependency, dep_obj in sorted(objs.items()):
                recurse(dependency, dep_obj, imports, modules, code_lines, seen_args, write_codelines=True)
            for dependency, dep_obj in sorted(default_objs.items()):
                recurse(dependency, dep_obj, imports, modules, code_lines, seen_args, write_codelines=False)
            fdef = inspect.getsource(obj)
            fdef = fdef[fdef.find("def ") :]
            code_lines.append(fdef)
        else:
            imports[obj.__module__].add(obj.__name__)

    def recurse(name, obj, imports, modules, code_lines, seen_args, write_codelines):                                                                                                    
        def _add_codeline(line):
            if write_codelines:
                code_lines.append(line)

        # prevent processing same dependency object multiple times, even if
        # multiple dependent objects exist in the tree from the original
        # func
        seen_key = str(name) + str(obj)
        if seen_args.get(seen_key) is True:
            return
        seen_args[seen_key] = True

        # Confusingly classes are subtypes of 'type'; non-classes are not
        if isinstance(obj, type):
            if obj.__module__ == "__main__":
                msg = f"Cannot serialize class {obj.__name__} from module __main__"
                raise Exception(msg)
            imports[obj.__module__].add(obj.__name__)
        elif isinstance(obj, FunctionType):
            process_functiontype(name, obj, imports, modules, code_lines, seen_args)
        elif isinstance(obj, ModuleType):
            module_file = inspect.getfile(obj)
            # skip this check for functions written by Tecton
            if f"{obj.__package__}.{name}" == obj.__name__:
                imports[obj.__package__].add(name)
            else:
                modules.add(obj.__name__)
        # TODO: based on the type of obj we need to add the code and import
        # statements for that type
        # elif isinstance(obj, xxx):
        #     _add_codeline(f"xxx")
        #     imports["xxx"].add("xxx")
        #     modules.add("xxx")
        else:
            try:
                repr_str = f"{name}={repr(obj)}"
                exec(repr_str)
                _add_codeline(repr_str)
            except Exception:
                msg = f"Cannot evaluate object {obj} of type '{type(obj)}' for serialization"
                raise Exception(msg)

    recurse(func.__name__, func, imports, modules, code_lines, seen_args, write_codelines=True)

    for module in sorted(imports):
        import_line = f"from {module} import "
        import_line += ", ".join(sorted(imports[module]))
        code_lines.insert(0, import_line)

    for module in sorted(modules):
        code_lines.insert(0, f"import {module}")

    return "\n".join(code_lines)
