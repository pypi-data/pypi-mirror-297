from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class ShortLine(Module):
    """
    Represents a short transmission line model with series impedance.

    Args:
        IndexName (str): A unique identifier for the module. This is used to create names for parameters and state variables.
        RefFrameAngle (Optional[Symbol]): The angle of the reference frame. Defaults to a symbolic variable 'phi' if not provided.
        RefFrameSpeed (Optional[Symbol]): The speed of the reference frame. Defaults to a symbolic variable 'dphidt' if not provided.
        BaseSpeed (float): The base speed of the system. Defaults to 1. This affects the units of the state variables.
        ParamMap (Optional[dict]): A dictionary mapping parameter names to their values. Keys should be in the format '[ParameterName]_IndexName'.

    Attributes:
        Refer to the attributes of the Module class.
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['RTL', 'LTL']
        StateVariableNames = ['iTLMd', 'iTLMq']
        PortInputNames = ['vTLLd', 'vTLLq', 'vTLRd', 'vTLRq']
        PortStateNames = ['iTLMd', 'iTLMq', 'iTLMd', 'iTLMq']
        ControllableInputNames = []

        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs =  Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = Matrix([self.PortStates[0], self.PortStates[1], -self.PortStates[2], -self.PortStates[3]])
        self.PortVoltages = self.PortInputs
        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current', 'Current', 'Current']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        iTLMd, iTLMq = self.StateVariables
        vTLLd, vTLLq, vTLRd, vTLRq = self.PortInputs
        RTL, LTL = self.Parameters

        wb = self.BaseSpeed
        dphidt = self.RefFrameSpeed

        # Transmission Line Dynamics
        diTLMddt = dphidt * iTLMq - (vTLRd - vTLLd + RTL * iTLMd) / LTL
        diTLMqdt = -dphidt * iTLMd - (vTLRq - vTLLq + RTL * iTLMq) / LTL

        StateSpace = wb * Matrix([diTLMddt, diTLMqdt])
        StateSpace = simplify(StateSpace) # what does simplyfy() do?
        return StateSpace