from sympy import symbols, simplify, Matrix, sin, cos, I, re, im, Function, pi, sqrt
from pycamps.modules.module import Module

class SMOneAxisV2GcEc(Module):
    """
    Implements governor and excitation control on one axis model of synchronous machine. 
    The model treats stator currents as port inputs and voltages as port states.

    Args:
        IndexName (str): A unique identifier for the module. This is used to create names for parameters and state variables.
        RefFrameAngle (Optional[Symbol]): The angle of the reference frame. Defaults to a symbolic variable 'phi' if not provided.
        RefFrameSpeed (Optional[Symbol]): The speed of the reference frame. Defaults to a symbolic variable 'dphidt' if not provided.
        BaseSpeed (float): The base speed of the system. Defaults to 1. This affects the units of the state variables.
        ParamMap (Optional[dict]): A dictionary mapping parameter names to their values. Keys should be in the format '[ParameterName]_IndexName'.

    Attributes:
        Refer to the attributes of the Module class.
    
    Example:
        >>> from sympy import symbols
        >>> from pycamps.modules import SMOneAxisV2GcEc
        >>> sm = SMOneAxisV2GcEc('G1', RefFrameAngle=symbols('phi'), RefFrameSpeed=symbols('dphidt'), BaseSpeed=377)

    Created by Xia Miao for ONR project - extracted and modified by Rupa on Nov 4, 2020
    """
    def __init__(self, IndexName, RefFrameAngle=None, RefFrameSpeed=None, BaseSpeed=1, ParamMap=None):
        super().__init__()
        self.ModuleName = IndexName
        ParameterNames = ['H','F','Td0','xd','xdprime','rs']
        StateVariableNames = ['delta','omega','eqprime','Pm','omegaInt','a','Vr','efd','Vf']
        PortInputNames = ['iSd','iSq']
        PortStateNames = ['vSd','vSq']
        ControllerGainNames = ['Tg','Kt','r','Kp','Ki','Tu','Ka','Ta','Ke','Te','Tf']
        SetPointNames = ['omega','Vt','P']

        Units = ['radians','rad/s','W','W','A','A','rad/s','W','W','A','A'] if BaseSpeed == 1 else ['units']*11

        IndexName = '_' + IndexName # TODO: Properly implement index names without leading underscore
        self.ParameterMap = ParamMap if ParamMap is not None and all(
            key in [p + IndexName for p in ParameterNames] for key in ParamMap.keys()) else {}
        
        self.RefFrameAngle = RefFrameAngle if RefFrameAngle is not None else symbols('phi', real=True)
        self.RefFrameSpeed = RefFrameSpeed if RefFrameSpeed is not None else symbols('dphidt', real=True)
        self.BaseSpeed = BaseSpeed
        self.Units = Units

        self.Parameters = Matrix(symbols([p + IndexName for p in ParameterNames]))
        self.StateVariables =  Matrix(symbols([s + IndexName for s in StateVariableNames]))
        self.ControllerGains =  Matrix(symbols([c + IndexName for c in ControllerGainNames]))
        self.PortInputs =  Matrix(symbols([p + IndexName for p in PortInputNames]))
        self.PortStates =  Matrix(symbols([p + IndexName for p in PortStateNames]))

        self.PortCurrents = self.PortInputs
        delta, eqprime = self.StateVariables[:2]
        TN2M = Matrix([[sin(delta), cos(delta)], [-cos(delta), sin(delta)]])

        # Get eqprime in network reference
        E = (TN2M.inv() * Matrix([[0], [eqprime]]))
        vSd, vSq = E
        self.PortVoltages = Matrix([vSd, vSq])

        self.StateVariableDerivatives =  Matrix(symbols(['d' + s + IndexName + 'dt' for s in StateVariableNames]))
        self.PortStateDerivatives =  Matrix(symbols(['d' + p + IndexName + 'dt' for p in PortStateNames]))
        self.PortStates_Time = Matrix([Function(p + IndexName + '_t')(symbols('t', real=True)) for p in PortStateNames])
        self.SetPoints =  Matrix(symbols([p + IndexName + '_ref' for p in SetPointNames]))
        self.PortOutputTypes = ['Current', 'Current']
        self.StateSpaceEquations = self.dynamics()

    def dynamics(self):
        '''
        Inputs:
        this.StateVariables: delta, omega,eqprime, Pm, omegaInt, a, Vr, efd, Vf;
        this.InputVariables: iSd,iSq
        this.ControllerGains: Tg,Kt,r,Kp,Ki,Tu,Ka,Ta,Ke,Te,Tf
        this.SetPoints: omega_ref, Vt_ref, P_ref; 
        this.Parameters: H,F,Td0,xd,xdprime,rs
        this.RefFrameAngle: angle of rotating reference frame
        this.RefFrameSpeed: speed of rotating reference frame
        this.BaseSpeed: Base speed
            
        Outputs:
        StateSpace: [diSddt ; diSqdt ; diRdt ; domegadt ; dthetadt]
        ControlInputEquations

        Refer Ilic, Marija D and Zaborszky, John, Dynamics and control
        of large electric power systems,2000, Wiley New York for
        detailed open-loop model derivation
        The governor and exciter controllers are standard IEEE-TYPE 1. Refer Chapter 5 Section 5.5.2  - Kevin Bachovchin, Xia Miao, Marija Ilic (co-editors), State Space Modelling 
        and Primary Control of Smart Grid Components,,Volume 2,
        Cambridge University Press for governor and excitation controllers
        '''
        delta, omega, eqprime, Pm, omegaInt, a, Vr, efd, Vf = self.StateVariables
        iSd, iSq = -self.PortInputs
        H, D, Td0, xd, xdprime, Rs = self.Parameters
        Tg, Kt, r, Ki, Kp, Tu, Ka, Ta, Ke, Te, Tf = self.ControllerGains
        omega0, Vref, Pmref = self.SetPoints

        dphidt = self.RefFrameSpeed
        wb = self.BaseSpeed
        
        # Reference Transformation matrix: From network to machine
        TN2M = Matrix([[sin(delta), cos(delta)], [-cos(delta), sin(delta)]])
        imach = TN2M * Matrix([[iSd], [iSq]])
        id, iq = imach

        # Get eqprime in network reference
        E = (TN2M.inv() * Matrix([[0], [eqprime]]))
        vSd, vSq = E

        # machine dynamics 
        ddeltadt = -wb*(delta -pi/2)
        domegadt = 1/(2*H)*(Pm + Pmref - eqprime*iq - D*(omega - dphidt))
        deqprimedt = 1/Td0*(-eqprime -(xd - xdprime)*id +efd)

        # Governor control
        dPmdt = (-Pm + Kt*a)/Tu
        domegaIntdt = (omega-omega0)
        dadt = (-Kp*(omega-omega0) - Ki*omegaInt - a*r)/Tg

        # Exciter control - IEEE Type 1
        Vt = sqrt(vSd**2 + vSq**2)
        # Vt = eqprime
        dVrdt = (-Vr + Ka*(Vref - Vt - Vf))/Ta
        defddt = (-Ke*efd + Vr)/Te
        dVfdt = (-Vf + 0*defddt)/Tf
        
        StateSpace = Matrix([ddeltadt, domegadt, deqprimedt, dPmdt, domegaIntdt, dadt, dVrdt, defddt, dVfdt])
        StateSpace = simplify(StateSpace)
        return StateSpace