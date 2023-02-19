from random import random
import numpy as np
import math


class Particle:
    def __init__(self, domain, dimensions) -> None:
        self.x_min = domain[0]
        self.x_max = domain[1]
        self.n = dimensions

        #current position #[x1, x2 ... xn] 
        self.position = np.array([self.x_min + (self.x_max)*(random()) for _ in range(dimensions)]) 
        #current velocity #[v1, v2 ... vn] 
        self.velocity = np.array([self.x_min + (self.x_max)*(random()) for _ in range(dimensions)])  
        self.p = self.position #best position of particle #has lowest cost
        self.min_cost = math.inf #cost value at p



class ParticleSwarmOptimisation :
    def __init__(self, epochs, cost_function ,domain, dim, S, w , c1, c2) -> None:
        self.x_min = domain[0]
        self.x_max = domain[1]
        self.n = dim #number of dimensions

        self.cost = cost_function #reference to the cost function

        self.epochs = epochs
        self.S = S #num of particles in the swarm
        self.swarm = [Particle(domain, dim) for _ in range(S)] #list of particles in the swarm

        self.w = w
        self.c1 = c1
        self.c2 = c2
        
        self.g = self.swarm[0].position #globally best position #global minima
        self.min_cost = math.inf #cost at g


    def run(self):
        for _ in range(self.epochs) :
            #move all the particles to the new position
            self.move_particles() #updates position, velocity of all particles

            #is the particle's new position the particle's best position yet?
            self.update_p() #update local optima

            #is any particle's new position the best position yet?
            self.update_g() #update global optima
            
        #solution found
        print(f"Function has min value {self.min_cost} for point {self.g}")


    #move all particles in the swarm
    def move_particles(self):
        for particle in self.swarm:
            ##### calculate velocity #####
            memory = (self.w)*(particle.velocity)
            attractor = (self.c1)*(random())*(particle.p - particle.position)
            repellant = (self.c2)*(random())*(self.g - particle.position)

            new_velocity = memory + attractor + repellant
            particle.velocity = new_velocity

            ##### calculate new position #####
            new_position = particle.position + particle.velocity

            #this new position should be w/in domain
            for i in range(self.n):
                new_position[i] = max(self.x_min , new_position[i])
                new_position[i] = min(self.x_max , new_position[i])

            ##### move particle to new position #####
            particle.position = new_position


    #update local minima for each particle
    def update_p(self) :
        for particle in self.swarm:
            particle_cost = self.cost(particle.position)

            if particle_cost < particle.min_cost :
                #new minima of the cost function found
                particle.min_cost = particle_cost
                particle.p = particle.position


    #update global minima
    def update_g(self) :
        #check all particles's local optimas
        #the best local optima is the global optimum
        for particle in self.swarm:
            particle_cost = self.cost(particle.position)

            if particle_cost < self.min_cost :
                #new minima of the cost function found
                self.min_cost = particle_cost
                self.g = particle.position

        

###########################################################

#function whose minima is to be found
def f(x):
    return (x+1)*(x+1)*np.sin(x)
# f(x) = ((x+1)^2)*(sinx)
#aka cost function

dimensions = 1
domain = (-4, 2) #(x_min , x_max)

#hyperparameters
epochs = 100
cost = f #cost function
S = 70
w = 0.7
c1 = 2
c2 = 1

pso = ParticleSwarmOptimisation(epochs, cost, domain, dimensions, S , w, c1, c2)
pso.run()