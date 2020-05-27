import sys
import subprocess
import pkg_resources

required = {'numpy', 'vpython'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing],
                    stdout=subprocess.DEVNULL)

import numpy as np
from vpython import *
from simulation import *

print("\nNOTE: The length details entered will be converted into AU for the",
        "simulation.")

print("\nEnter the details of the host star:")
s_mass = np.float(input("Mass (kg): "))

print("\nEnter the attributes of the planet wrt the star:")
p_mass = np.float(input("Mass (kg): "))
p_dist = np.float(input("Peripsis distance from the star (m): "))
p_vel = np.float(input("Periapsis velocity (m/s): "))

print("\nEnter the attributes of the moon wrt the planet:")
m_mass = np.float(input("Mass (kg): "))
m_dist = np.float(input("Peripsis distance from the planet (m): "))
m_vel = np.float(input("Periapsis velocity wrt the planet (m/s): "))

S = SpaceObj(s_mass, 0.2*dist_scale, 0, 0)
P = SpaceObj(p_mass, 0.03*dist_scale, p_vel, p_dist)
M = SpaceObj(m_mass, 0.028*dist_scale, m_vel, m_dist)

simulate(S, P, M)
