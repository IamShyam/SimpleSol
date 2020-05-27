# Importing requisite packages
from vpython import *
import numpy as np

#---------------------------SIMULATION CONSTANTS------------------------------#

# The simulation takes a day as a unit of time to run through. this calls for
# a conversion from seconds to days very often.
day_scale = 24*60*60        # number of seconds in a day

# The scale of the canvas used for simulation is of the order of Astronomical
# Units (AU) = 1.4961e11 metres
dist_scale = 1.4961e11      # AU in m

# The value of G needs to be altered for the sake of the simulation
#       
#             G = 6.673e-11 N.m^2/kg^2
#               = 6.673e-11 m^3/kg.s^2
#
# Using the scaling values mentioned earlier, after converting seconds to days
# and metres to AU, we arrive at the result
G = 1.4878e-34      # AU^3/(day^2).kg

#--------------------------CELESTIAL OBJECT CLASS-----------------------------#
class SpaceObj(object):

    """
    Class used for the input of the attributes of the celestial object

    Parameters:
    mass: mass of the celestial object (kilograms)
    rad: radius of the object (metres)
    vel: velocity of the object at the periapsis of its orbit (meters/second)
    dist: distance between the object and the object it's orbitng (metres)

    Returns:
    A SpaceObj object with altered scaled values for simulation
    """

    def __init__(self, mass, rad, vel, dist):
        
        # the mass of the object is recorded in kilograms
        self.mass = mass
        
        # the given radius (in meters) are converted to AU
        self.radius = np.float(rad/dist_scale)

        # the given velocity (m/s) are converted to AU/day
        self.velocity = np.float((vel*day_scale)/dist_scale)

        # momentum as a reult has the units kg.AU/day
        self.momentum = self.mass*vector(0, self.velocity, 0)
        
        # the distance metric is converted to AU
        self.dist = np.float(dist/dist_scale)


#-----------------GRAVITTIONAL FORCE CALCULATOR FUNCTION----------------------#
def gravforce(body1, body2):

    """
    Helper Function to find the force vector using the Universal Gravitational 
    Law

    Parameters:
    body1, body2: initialised vpython sphere objects

    Returns:
    force_vec: a resultant force vector with direction in the form of vpython 
    vectors
    """

    dist_vec = (body1.pos - body2.pos)
    dist_mag = mag(dist_vec)
    dist_hat = dist_vec / dist_mag

    force_mag = (-1 * G * body1.mass * body2.mass)/dist_mag**2
    force_vec = force_mag * dist_hat

    return force_vec

#---------------GRAPHIC SPHERE OBJECT MAKING FUNCTION-------------------------#
def graphsphere(body, color):

    """
    Helper Function to initiate the graphical classes
    
    Parameters:
    body: An object of the SpaceObj Class defined
    color: a color defined by the palette in vpython
    trail: gives out trails of motion in the simulation; defaultly set as True

    Returns:
    A vpython sphere object with attributes: pos, radius, momentum, mass, 
    color
    """

    return sphere(
        pos = vector(body.dist, 0, 0),
        radius = 1 * body.radius,
        momentum = body.momentum,
        mass = body.mass,
        color = color
)

#-------------------------MAIN SIMULATION FUNCTION----------------------------#
def simulate(S, P, M):
    
    """
    The main simulate function of the entire program. Simulates the 3 body 
    system in the default web-browser using the vpython package

    Parameters:
    S: The Star object from the SpaceObj Class
    P: The Planet object from the SpaceObj Class
    M: The Moon object of the SpaceObj Class

    Returns:
    Nothing
    """
    
    # Alter the distance of the moon to fit in with the scale of the canvas
    M.dist = P.dist - M.dist
    M.momentum = M.mass*vector(0, P.velocity - M.velocity, 0)

    # Initialise the spheres on the canvas with the initial conditions applied
    star = graphsphere(S, color.yellow)
    attach_trail(star, color=star.color, type="points", pps=2, retain=100)
    planet = graphsphere(P, color.blue)
    attach_trail(planet, color=planet.color, type="points", pps=2, retain=100)
    moon = graphsphere(M, color.white)
    sim_lab = label(pos=vector(0,-0.35,0), text="Earth Day: 0")

    # the increment of time used in the simulation (in days)
    dt = 0.005
    time = 0

    while(True): 
        try:
            rate(1000)

            # Update the gravitational forces vectors
            star.force = gravforce(star, planet) + gravforce(star, moon)
            planet.force = gravforce(planet, star) + gravforce(planet, moon)
            moon.force = gravforce(moon, planet) + gravforce(moon, star)

            # Update the momentum using ECM (numerical differentiation)
            star.momentum = star.momentum + dt*star.force
            planet.momentum = planet.momentum + dt*planet.force
            moon.momentum = moon.momentum + dt*moon.force

            # Update the position using ECM (numerical differentiation)
            star.pos = star.pos + (dt*star.momentum)/star.mass
            planet.pos = planet.pos + (dt*planet.momentum)/planet.mass
            moon.pos = moon.pos + (dt*moon.momentum)/moon.mass

            time = time + dt
            sim_lab.text = "Earth Day: " + str(round(time, 2))

        except KeyboardInterrupt:
            print("shutting down simulation...")
            break

#-----------------------------DEMO RUN----------------------------------------#
if __name__ == "__main__":
    
    # Default values from Sun
    # star = SpaceObj(1.9885e30, 6.957e8, 0, 0)
    star = SpaceObj(1.9885e30, 0.2*dist_scale, 0, 0)
    
    # Default values from Earth
    # planet = SpaceObj(5.9724e24, 6.371e6, 3.029e4, 1.4709e11)
    planet = SpaceObj(5.9724e24, 0.03*dist_scale, 3.029e4, 1.4709e11)
    
    # Default values from Moon
    # moon = SpaceObj(7.346e22, 1.737e6, 1082, 3.633e8)
    moon = SpaceObj(7.346e22, 0.028*dist_scale, 1082, 3.633e8)

    simulate(star, planet, moon)
