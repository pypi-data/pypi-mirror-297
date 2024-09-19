from sympy import symbols, Function, simplify, Matrix
from pycamps.modules.module import Module

class PVSOAControl(Module):
    """
    Represents a solar PV model with SOA control.

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
        ParameterNames = ['Rf', 'Lf', 'Vs']
        StateVariableNames = ['iPVd', 'iPVq']
        PortInputNames = ['vPVd', 'vPVq']
        PortStateNames = ['iPVd', 'iPVq']
        ControllableInputNames = ['Sd', 'Sq']
        SetPointNames = ['P', 'Q']

        Units = ['A', 'A'] if BaseSpeed == 1 else ['units', 'units']

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllableInputs = Matrix(symbols([c + IndexName for c in ControllableInputNames]))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortVoltages = self.PortInputs
        self.PortCurrents = -self.PortStates
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.SetPoints = Matrix(symbols([s + IndexName + '_ref' for s in SetPointNames]))
        self.StateSpaceEquations, self.ControlInputEquations = self.dynamics()

    def dynamics(self):
        iPVd, iPVq = self.StateVariables
        vPVd, vPVq = self.PortInputs
        Rf, Lf, Vs = self.Parameters
        Pref, Qref = self.SetPoints
        Sd, Sq = self.ControllableInputs
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed
        
        # Control Design
        # I = (Pref + 1i*Qref)/(vPVd + 1i*vPVq);
        # iPVdref = real(I); iPVqref = imag(I);
        iPVdref = (Pref*vPVd + Qref*vPVq)/(vPVd**2 + vPVq**2) # Assuming Pref, Qref, vPVd, vPVq are real quantities
        iPVqref = (Qref*vPVd - Pref*vPVq)/(vPVd**2 + vPVq**2)
        Sd_eq = 1/Vs*(vPVd - Lf*dphidt*iPVq + Rf*iPVd - Lf*(iPVd-iPVdref))
        Sq_eq = 1/Vs*(vPVq + Lf*dphidt*iPVd + Rf*iPVq - Lf*(iPVq-iPVqref))
        
        # Load Dynamics
        diPVddt = - Rf*iPVd/Lf + dphidt*iPVq + (Vs*Sd - vPVd)/Lf
        diPVqdt = - Rf*iPVq/Lf - dphidt*iPVd + (Vs*Sq - vPVq)/Lf
        
        StateSpaceEquations = wb*Matrix([diPVddt, diPVqdt])
        ControlInputEquations = Matrix([Sd_eq, Sq_eq])
        StateSpaceEquations = simplify(StateSpaceEquations)
        ControlInputEquations = simplify(ControlInputEquations)
        return StateSpaceEquations, ControlInputEquations