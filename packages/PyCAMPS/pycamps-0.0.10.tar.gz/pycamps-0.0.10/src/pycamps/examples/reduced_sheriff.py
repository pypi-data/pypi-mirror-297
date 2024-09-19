import os
import matplotlib.pyplot as plt

from pycamps.modules import LongLine, RLLoad, SM7StateControl, PVSOAControl
from pycamps.simulation import PowerSystem, Dynamics
from pycamps.logger import configure_logging

# Specify name of power system (for saving files)
system_name = "SM7StateControl_LL_RLLoad"

# Configure logging
os.environ['LOG_LEVEL'] = 'INFO'
logger = configure_logging(log_file=f'{system_name}.log', log_to_console=True, log_to_file=True)

# Define base speed
wb = 377
# Generators
G22 = SM7StateControl('G22', BaseSpeed=wb)
G23 = SM7StateControl('G23', BaseSpeed=wb)
PV21 = PVSOAControl('PV21', BaseSpeed=wb)

# Transmission Lines
TL_1_21 = LongLine('TL_1_21', BaseSpeed=wb)
TL_1_22 = LongLine('TL_1_22', BaseSpeed=wb)
TL_1_23 = LongLine('TL_1_23', BaseSpeed=wb)

# Loads
L1 = RLLoad('L1', BaseSpeed=wb)
L21 = RLLoad('L21', BaseSpeed=wb)
L22 = RLLoad('L22', BaseSpeed=wb)
L23 = RLLoad('L23', BaseSpeed=wb)

# Modules
Modules = [PV21,G22,G23,L1,L21,L22,L23,TL_1_21,TL_1_22,TL_1_23]
    
# Buses
Bus1 = [[L1],[TL_1_21, 'L'],[TL_1_22, 'L'],[TL_1_23, 'L']]
Bus21 = [[PV21], [L21],[TL_1_21,'R']]
Bus22 = [[G22], [L22],[TL_1_22,'R']]
Bus23 = [[G23], [L23],[TL_1_23,'R']]

Buses = [Bus1, Bus21, Bus22, Bus23]
PS = PowerSystem(system_name, Modules, Buses)

# 1: Writes state space equations and vector x
StateSpace = PS.StateSpace
StateSpace.write_equations()
StateSpace.write_vector_x()

# 2. Solve for system equilibrium
Simulator = Dynamics(PS)
Simulator.load_new_params(params_directory = '/Users/anishravichandran/Documents/PyCAMPS/src/pycamps/examples/parameters')
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

