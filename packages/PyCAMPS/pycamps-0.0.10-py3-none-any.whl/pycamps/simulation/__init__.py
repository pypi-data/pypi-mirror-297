"""
This module contains the tools to construct and simulate power system models.
"""

import importlib

def lazy_import(name):
    module_name = name.lower()
    if module_name == 'powersystem': # Have to change this to match the actual module name
        module_name = 'power_system'
    elif module_name == 'statespace':
        module_name = 'state_space'
    elif module_name == 'numericalintegration':
        module_name = 'numerical_integration'
    return importlib.import_module(f'.{module_name}', __name__)

class LazyLoader:
    def __init__(self, name):
        self._name = name
        self._module = None

    def __getattr__(self, name):
        if self._module is None:
            self._module = lazy_import(self._name)
        return getattr(self._module, name)

    def __call__(self, *args, **kwargs):
        if self._module is None:
            self._module = lazy_import(self._name)
        return getattr(self._module, self._name)(*args, **kwargs)

Dynamics = LazyLoader('Dynamics')
PowerSystem = LazyLoader('PowerSystem')
StateSpace = LazyLoader('StateSpace')
NumericalIntegration = LazyLoader('NumericalIntegration')

__all__ = ['Dynamics', 'PowerSystem', 'StateSpace', 'NumericalIntegration']