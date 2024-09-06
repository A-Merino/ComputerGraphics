from vedo import *
import numpy as np
from robot_arm import RobArm
import kinemat as km
import gc

plt = Plotter()


# Create Robot arms and floor
arm1 = RobArm(320, 0, 0)

arm2 = RobArm(320*np.cos(2*np.pi / 3), 320*np.sin(2*np.pi / 3), 120)

arm3 = RobArm(320*np.cos(4*np.pi / 3), 320*np.sin(4*np.pi / 3), 240)

floor = Box([0,0, -150], 1000, 1000, 300).color("green3")


light =  Light((-700, 0, 500), (0,0,300), c = None, intensity=1)
light2 = Light((700,0,500), (0,0,300), c = None, intensity=1)

# Add objects to Plot
plt += [arm1.fp(), arm2.fp(), arm3.fp(), floor, light, light2]

dt = 0.25  # time step

p0 = 0.0
dp0_dt = 3.0

p1 = 0.0
dp1_dt = 0.0

p2 = 0.0
dp2_dt = 0.0

p3 = 0.0
dp3_dt = 3.6

m = 0



def loop_func(event):
    global  p0, dp0_dt, p1, dp1_dt, p2, dp2_dt, p3, dp3_dt, m, plt

    # Motion equation (dt varies implicitly in vedo animation framework)
    # Motion equation with constant velocity 
    p0 = p0 + dp0_dt * dt 
    p1 = p1 + dp1_dt * dt 
    p2 = p2 + dp2_dt * dt 
    p3 = p3 + dp3_dt * dt 


    arm1.move([p0, p1, p2, p3])
    arm2.move([p0, p1, p2, p3])
    arm3.move([p0, p1, p2, p3])

    plt.clear()
    plt += [arm1.fp(), arm2.fp(), arm3.fp(), floor]
    plt.render()
    if m == 0 and p0 >= 30:
        dp0_dt = 0
        dp1_dt = 2
        dp2_dt = 6
        m += 1
    if m == 1 and p1 >= 30:
        dp0_dt = 10
        dp1_dt = 0
        dp2_dt = 0
        m += 1
    if m == 2 and p0 >= 170:
        dp0_dt = -20
        dp1_dt = -3
        dp2_dt = -2.5
        m += 1
    if m == 3 and p0 <= -330:
        dp0_dt = 0
        dp1_dt = 4
        dp2_dt = 0.25
        m += 1
    if m == 4 and p1 >= -30:
        dp0_dt = 15
        dp1_dt = 0.5
        dp2_dt = -3
        m += 1
    if m == 5 and p0 >= 0:
        dp0_dt = 0
        dp1_dt = 2
        dp2_dt = 4
        m += 1
    if m == 6 and p2 >= 0:
        gc.collect()
        dp0_dt = 4
        dp1_dt = 0
        dp2_dt = 0
        p0 = 0.0
        p1 = 0.0
        p2 = 0.0
        p3 = 0.0
        m = 0



#-----------------------------------------------------
#  main 
#-----------------------------------------------------
plt.initialize_interactor()
plt.add_callback("timer", loop_func)
plt.timer_callback("start")
plt.show(viewup='z').close()