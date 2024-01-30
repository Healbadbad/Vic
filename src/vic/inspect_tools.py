# Tools for inspecting objects
import inspect
from copy import deepcopy
import pprint

def get_attributes_list(var, ignore_builtins=True):
    variable_properties = []
    callables = []
    prop_values = []
    for i, prop in enumerate(dir(var)):
        if prop.startswith('__') and ignore_builtins:
            continue

        try:
            is_callable = callable(getattr(var, prop))
        except Exception as e:
            callables.append(f"{prop}: {Exception}")
            continue

        if is_callable:
            #callables.append(f"{prop}: {type(getattr(var, prop))}")
            callables.append(f"{prop}: {type(getattr(var, prop)).__name__:>5}")
        else:
            try:
                repr = pprint.pformat(getattr(var, prop), compact=True)
                repr = repr.replace('\n', ' ')
                variable_properties.append(f"{prop}: {repr}")
            except Exception as e:
                variable_properties.append(f"{prop}: {Exception}")

    return variable_properties, callables

def get_modules(locals, ignore_builtins=False):
    modules_list = []
    for local_var in list(locals):
        if inspect.isbuiltin(locals[local_var]) or local_var.startswith('__'):
            continue
        if inspect.ismodule(locals[local_var]):
            modules_list.append(local_var)
    return modules_list

def get_functions(locals, ignore_builtins=False):
    modules_list = []
    for local_var in list(locals):
        if inspect.isbuiltin(locals[local_var]) or local_var.startswith('__'):
            continue
        if callable(locals[local_var]):
            modules_list.append(local_var)
    return modules_list

def get_classes(locals, ignore_builtins=False):
    class_list = []
    for local_var in list(locals):
        if inspect.isbuiltin(locals[local_var]) or local_var.startswith('__'):
            continue
        if inspect.isclass(locals[local_var]):
            class_list.append(local_var)
    return class_list

def get_tensors(locals, ignore_builtins=False):
    tensor_list = []
    for local_var in list(locals):
        if inspect.isbuiltin(locals[local_var]) or local_var.startswith('__'):
            continue
        if hasattr(locals[local_var], 'T'):
            tensor_list.append(local_var)
    return tensor_list

def filter_builtins(lista, ignore_builtins=False):
    if ignore_builtins:
        return [item for item in lista if not item.startswith('__')]
    return lista

def list_uniques(lista, listb):
    # returns a list with the unique items of lista that aren't in listb
    return list(set(lista) - set(listb))


# Modules, local variables, 

# Callables
#  - Functions
#  - Methods
#  - Classes
#  - Builtins
#  - Other callables
