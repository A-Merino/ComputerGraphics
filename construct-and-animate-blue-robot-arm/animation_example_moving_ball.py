"""A ball moving in space with constant velocity"""
# Adapted from: https://github.com/marcomusy/vedo/blob/master/examples/simulations/gyroscope1.py
# E. Ribeiro, 2024. 
from vedo import *

#------------------- parameters
dt = 0.05  # time step

x = np.array([0,0,0])

dx_dt = 0.5

#------------------- the scene
plt = Plotter()
plt += __doc__

ball = Sphere([0, 0, 0], r=0.1).c("red")

plt += [ball]       # add it to Plotter.

plt += Box(pos=(0, 0.5, 0), length=2.6, width=3, height=2.6).wireframe().c("gray",0.2)

# ############################################################ the physics
def loop_func(event):
    global  x, dx_dt

    # Motion equation (dt varies implicitly in vedo animation framework)
    # Motion equation with constant velocity 
    x = x + dx_dt * dt 

    # set next position of the ball  
    ball.pos(x)

    if np.linalg.norm(x) > 1: 
        dx_dt = (-1) * dx_dt 


    plt.render()

#-----------------------------------------------------
#  main 
#-----------------------------------------------------
plt.initialize_interactor()
plt.add_callback("timer", loop_func)
plt.timer_callback("start")
plt.show().close()


