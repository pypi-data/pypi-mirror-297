from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class PVSOAControlV2(Module):
    """
    Represents a solar PV model with SOA control.

    Args:
        IndexName (str): A unique identifier for the module. This is used to create names for parameters and state variables.
        RefFrameAngle (Optional[Symbol]): The angle of the reference frame. Defaults to a symbolic variable 'phi' if not provided.
        RefFrameSpeed (Optional[Symbol]): The speed of the reference frame. Defaults to a symbolic variable 'dphidt' if not provided.
        BaseSpeed (float): The base speed of the system. Defaults to 1. This affects the units of the state variables.
        Mode (str): The mode of operation. Defaults to 'PQ'. Options are 'PQ' or 'Vt'.
        ParamMap (Optional[dict]): A dictionary mapping parameter names to their values. Keys should be in the format '[ParameterName]_IndexName'.

    Attributes:
        Refer to the attributes of the Module class.
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, Mode='PQ', ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['Rf', 'Lf', 'Vs', 'KV']
        StateVariableNames = ['iPVd', 'iPVq']
        PortStateNames = ['iPVd', 'iPVq']
        PortInputNames = ['vPVd', 'vPVq']
        ControllableInputNames = ['Sd', 'Sq']
        SetPointNames = ['P', 'Q'] if Mode == 'PQ' else ['Vt']
        self.Mode = Mode

        if BaseSpeed == 1:
            Units = ['A', 'A', 'V', 'V']
        else:
            Units = ['units']*4

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        # If optional parameter ParamMap is given, set this.ParameterMap
        # equal to ParamMap. Otherwise, set it to an empty array.
        if ParamMap is None:
            self.ParameterMap = []
        else:
            if not all([key in ParameterNames + [IndexName] for key in ParamMap.keys()]):
                raise ValueError('One or more keys in the Parameter Map do not match the parameter names')
            else:
                self.ParameterMap = ParamMap
        
        self.Units = Units
        
        self.Parameters = symbols([name + IndexName for name in ParameterNames])
        self.StateVariables = symbols([name + IndexName for name in StateVariableNames])
        self.ControllableInputs = symbols([name + IndexName for name in ControllableInputNames])
        self.PortInputs = symbols([name + IndexName for name in PortInputNames])
        self.PortStates = symbols([name + IndexName for name in PortStateNames])
        self.PortVoltages = self.PortInputs
        self.PortCurrents = [-state for state in self.PortStates]
        self.StateVariableDerivatives = symbols(['d' + name + IndexName + 'dt' for name in StateVariableNames])
        self.PortStateDerivatives = symbols(['d' + name + IndexName + 'dt' for name in PortStateNames])
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.SetPoints = symbols([name + IndexName + '_ref' for name in SetPointNames])
        self.StateSpace, self.ControlInputEquations = self.dynamics()

    def dynamics(self):
        iPVd = self.StateVariables[0]
        iPVq = self.StateVariables[1]
        
        vPVd = self.PortInputs[0]
        vPVq = self.PortInputs[1]
        
        Rf = self.Parameters[0]
        Lf = self.Parameters[1]
        Vs = self.Parameters[2]
        Kv = self.Parameters[3]
        
        if self.Mode == 'PQ':
            Pref = self.SetPoints[0]
            Qref = self.SetPoints[1]
        else:
            Vref = self.SetPoints[0]
        
        Sd = self.ControllableInputs[0]
        Sq = self.ControllableInputs[1]
        
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed
        
        if self.Mode == 'PQ':
            Vmag2 = vPVd**2 + vPVq**2
            iPVdref = (Pref*vPVd + Qref*vPVq)/Vmag2
            iPVqref = (-Qref*vPVd + Pref*vPVq)/Vmag2
        else:
            vPVdref = Vref
            vPVqref = 0
            iPVdref = - Kv*(vPVd - vPVdref)
            iPVqref = - Kv*(vPVq - vPVqref)
        
        # Open loop equations
        diPVddt = -(Rf/Lf)*iPVd + (Vs*Sd - vPVd)/Lf + dphidt*iPVq
        diPVqdt = -(Rf/Lf)*iPVq + (Vs*Sq - vPVq)/Lf - dphidt*iPVd
        
        Sd = (vPVd - dphidt*Lf*iPVq + Rf*iPVdref)/Vs
        Sq = (vPVq + dphidt*Lf*iPVd + Rf*iPVqref)/Vs
        
        StateSpace = wb*[diPVddt, diPVqdt]
        ControlInputEquations = [Sd, Sq]
        StateSpace = simplify(StateSpace)
        ControlInputEquations = simplify(ControlInputEquations)
        
        return StateSpace, ControlInputEquations