from vpython import *
import numpy as np

#---------------------------SIMULATION CONSTANTS------------------------------#
day_scale = 24*60*60        # number of seconds in a day
dist_scale = 1.4961e11      # Astronomical Unit in m
G = 1.4878e-34

#--------------------------CELESTIAL OBJECT CLASS-----------------------------#
class SpaceObj(object):

    """
    Class used for the input of the attributes of the celestial object
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
    Helper Function to find the force of gravity
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
    """

    return sphere(
        pos = vector(body.dist, 0, 0),
        radius = 1 * body.radius,
        momentum = body.momentum,
        mass = body.mass,
        color = color,
        make_trail = True
)

#-------------------------MAIN SIMULATION FUNCTION----------------------------#
def simulate(S, P, M):
    
    M.dist = P.dist - M.dist
    M.momentum = M.mass*vector(0, P.velocity - M.velocity, 0)
    star = graphsphere(S, color.yellow)
    planet = graphsphere(P, color.blue)
    moon = graphsphere(M, color.white)

    dt = 0.01
    time = 0

    while(True): 
        try:
            rate(1000)
            star.force = gravforce(star, planet) + gravforce(star, moon)
            planet.force = gravforce(planet, star) + gravforce(planet, moon)
            moon.force = gravforce(moon, planet) + gravforce(moon, star)

            star.momentum = star.momentum + dt*star.force
            planet.momentum = planet.momentum + dt*planet.force
            moon.momentum = moon.momentum + dt*moon.force

            star.pos = star.pos + (dt*star.momentum)/star.mass
            planet.pos = planet.pos + (dt*planet.momentum)/planet.mass
            moon.pos = moon.pos + (dt*moon.momentum)/moon.mass

            print(time)
            time = time + dt
            
        except KeyboardInterrupt:
            print("shutting down simulation...")
            break

#-----------------------------DEMO RUN----------------------------------------#
if __name__ == "__main__":
    
    # Default values from Sun
    star = SpaceObj(1.9885e30, 6.957e8, 0, 0)
    
    # Default values from Earth
    planet = SpaceObj(5.9724e24, 6.371e6, 3.029e4, 1.4709e11)
    
    # Default values from Moon
    moon = SpaceObj(7.346e22, 1.737e6, 1082, 3.633e8)

    simulate(star, planet, moon)