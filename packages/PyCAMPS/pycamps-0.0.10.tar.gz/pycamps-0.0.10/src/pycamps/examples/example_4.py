import os
import matplotlib.pyplot as plt

from pycamps.modules import LongLine, RLLoad, SM7StateControl
from pycamps.simulation import PowerSystem, Dynamics
from pycamps.logger import configure_logging

# Specify name of power system (for saving files)
system_name = "SM7StateControl_LL_RLLoad"

# Configure logging
os.environ['LOG_LEVEL'] = 'INFO'
logger = configure_logging(log_file=f'{system_name}.log', log_to_console=True, log_to_file=True)

# Define base speed
wb = 377
SM1 = SM7StateControl('G22', BaseSpeed=wb)
TL1 = LongLine('TL_1_2', BaseSpeed=wb)
L1 = RLLoad('L1', BaseSpeed=wb)

Modules = [SM1, TL1, L1]
Bus1 = [[SM1], [TL1,'L']]
Bus2 = [[L1], [TL1,'R']]
Buses = [Bus1, Bus2]
PS = PowerSystem(system_name, Modules, Buses)

# 1: Writes state space equations and vector x
StateSpace = PS.StateSpace
StateSpace.write_equations()
StateSpace.write_vector_x()

params_dictionary = {'LSd_G22': 2.4,
                    'LSq_G22': 1.77,
                    'LF_G22': 2.861, 
                    'LRD_G22': 6.0878, 
                    'LRQ_G22': 1.9592, 
                    'Lad_G22': 2.35, 
                    'Laq_G22': 1.72, 
                    'Laf_G22': 2.35, 
                    'Ldf_G22': 2.35, 
                    'RS_G22': 0.009, 
                    'RF_G22': 0.0021, 
                    'Rkd_G22': 0.2343, 
                    'Rkq_G22': 0.0337, 
                    'H_G22': 0.3468, 
                    'F_G22': 0.0092,
                    'K1_G22': 1.7029,
                    'K2_G22': 23.8411,
                    'K3_G22': -5.5648,
                    'delta_G22_ref': 0,
                    'omega_G22_ref': 1,
                    'iF_G22_ref': 0.5195,
                    'Tm_G22_ref': 1.32,
                    'vF_G22_ref': -0.0011,
                    'RTL_TL_1_2': 0.02978336677167938, 
                    'CTL_TL_1_2': 0.001, 
                    'LTL_TL_1_2': 0.40681749584779936, 
                    'RL_L1': 2.3125, 
                    'LL_L1': 0.9588}

# 2. Solve for system equilibrium
Simulator = Dynamics(PS)
Simulator.load_new_params(params_dictionary=params_dictionary)
xf = Simulator.solve_equilibrium(method='hybr')

# 3. Perform linearized analysis
Simulator.linearized_analysis(xf=xf)

# 4. Simulate system trajectory
time, states = Simulator.simulate_trajectory(xf=xf, simulation_time=0.1, method='LSODA')

# 5. Plot the results
plt.figure()
for variable_name, array in states.items():
    plt.plot(time, array, label=variable_name)

plt.legend()
plt.show()

