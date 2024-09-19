from sympy import symbols, simplify, Matrix, sin, cos, Function
from pycamps.modules.module import Module

'''
This module contains the Type 4-1 model of a synchronous machine and its extension with Governor Control.
'''
class Type4_1(Module):
    """
    Represents a standard Type 4-1 model of a synchronous machine.

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
        ParameterNames = ['J', 'D', 'xdprime', 'RS', 'eqprime', 'Pm']
        StateVariableNames = ['delta', 'omega']
        PortInputNames = ['vSd', 'vSq']
        PortStateNames = ['iSd', 'iSq'] # These are not necessarily states. They are outputs instead
        SetPointNames = []

        Units = ['radians', 'rad/s'] if BaseSpeed == 1 else ['units', 'units']

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}

        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        self.Units = Units
        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames], real=True))
        self.StateVariables = Matrix(symbols([s + IndexName for s in StateVariableNames], real=True))
        self.SetPoints = Matrix(symbols([sp + IndexName + '_ref' for sp in SetPointNames], real=True))
        self.PortInputs = Matrix(symbols([p + IndexName for p in PortInputNames], real=True))
        self.PortStates = Matrix(symbols([p + IndexName for p in PortStateNames], real=True))

        self.PortVoltages = self.PortInputs
        
        delta = self.StateVariables[0]
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Vmach = TN2M * Matrix([[self.PortInputs[0]], [self.PortInputs[1]]])
        xdprime, RS, eqprime = self.Parameters[2], self.Parameters[3], self.Parameters[4]
        Imach = Matrix([[-xdprime, -RS], [-RS, xdprime]]).inv() * Matrix([[Vmach[1] - eqprime], [Vmach[0]]])
        self.PortCurrents = -simplify((TN2M.inv() * Imach)) # I'm skipping the transpose here

        self.PortOutputTypes = ['Current', 'Current']
        self.StateVariableDerivatives = Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives = Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: delta,omega, eqprime
        this.InputVariables: iSd,iSq
        this.Parameters: J,D,Td0,xd,xdprime,RS,Pm,efd
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
		this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [diSddt ; diSqdt ; diRdt ; domegadt ; dthetadt]

        Refer Chapter 5 Section 5.5.1  - Kevin Bachovchin, Xia Miao, Marija Ilic (co-editors), State Space Modelling 
        and Primary Control of Smart Grid Components,�,Volume 2,
        Cambridge University Press for detailed model derivation
        '''
        delta, omega = self.StateVariables
        # PortInputs not explicitly used by this model. 
        J, D, xdprime, RS, eqprime, Pm = self.Parameters
        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed

        Inet = Matrix(self.PortCurrents) # I'm skipping the transpose here
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Imach = simplify(TN2M.inv() * Inet)
        iq = Imach[1]
        ddeltadt = omega - dphidt
        domegadt = 1 / J * (Pm + eqprime * iq - D * (omega - dphidt)) # Rotor dynamics

        return simplify(wb * Matrix([ddeltadt, domegadt]))