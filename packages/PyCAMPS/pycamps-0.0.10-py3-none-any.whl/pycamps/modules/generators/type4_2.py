from sympy import symbols, Function, simplify, Matrix, sin, cos, pprint
from pycamps.modules.module import Module

'''
This module contains the Type 4-2 model of a synchronous machine and its extension with Excitation Control.
'''

class Type4_2(Module):
    """
    Represents a standard Type 4-2 model of a synchronous machine.

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
        ParameterNames = ['Td0','xd','xdprime','Rs','efd','delta']
        StateVariableNames = ['eqprime']
        PortInputNames = ['vSd','vSq']
        PortStateNames = ['iSd','iSq']

        Units = ['V'] if BaseSpeed == 1 else ['units']

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))
        
        self.PortVoltages = self.PortInputs

        delta = self.Parameters[5]
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        Vmach = TN2M * Matrix([[self.PortInputs[0]], [self.PortInputs[1]]])
        xdprime, RS, eqprime = self.Parameters[2], self.Parameters[3], self.StateVariables[0]
        Imach = Matrix([[-xdprime, -RS], [-RS, xdprime]]).inv() * Matrix([[Vmach[1] - eqprime], [Vmach[0]]])
        self.PortCurrents = -simplify((TN2M.inv() * Imach)) # I'm skipping the transpose here

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: eqprime
        this.InputVariables: vSd,vSq
        this.Parameters: Td0,xd,xdprime,Rs,efd, delta
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [deqprimedt]

        Refer Chapter 5 Section 5.5.2  - Kevin Bachovchin, Xia Miao, Marija Ilic (co-editors), State Space Modelling 
        and Primary Control of Smart Grid Components,,Volume 2,
        Cambridge University Press for detailed model derivation
        '''
        eqprime = self.StateVariables[0]
        vSd, vSq = self.PortInputs
        Td0, xd, xdprime, Rs, efd, delta = self.Parameters

        # Reference Transformation matrix: From network to machine
        TN2M = Matrix([[sin(delta), -cos(delta)], [cos(delta), sin(delta)]])
        vmach = TN2M * Matrix([[vSd], [vSq]])
        vd, vq = vmach
        
        # State space of machine
        deqprimedt = (-eqprime*xd/xdprime + vq*(xd-xdprime)/xdprime + efd)/Td0

        StateSpace = Matrix([deqprimedt])
        return simplify(StateSpace)