from vedo import *
import numpy as np
from robot_arm import RobArm, Trail
import kinemat as km
import gc
import jacobian as jb
import matplotlib.pyplot as pltt

plt = Plotter()

# video = Video("animation.mp4", fps=20)

# Create Robot arms and floor
arm1 = RobArm(320, 0, 0)
arm2 = RobArm(320*np.cos(2*np.pi / 3), 320*np.sin(2*np.pi / 3), 120)
arm3 = RobArm(320*np.cos(4*np.pi / 3), 320*np.sin(4*np.pi / 3), 240)
floor = Box([0,0, -150], 1000, 1000, 300).color("green3")

ball = Sphere([0, 0, 300], 20).color("red")


light =  Light((-700, 0, 500), (0,0,300), c = None, intensity=1)
light2 = Light((700,0,500), (0,0,300), c = None, intensity=1)

# Add objects to Plot
plt += [arm1.fp(), arm2.fp(), arm3.fp(), floor, light, light2, ball]

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


xg = [[0],[-20],[-8]]
uv_g = jb.f2(xg, arm1.x, arm1.y)
# print(uv_g)
x1 = [[0],[0],[90]]
phit1, t1 = jb.graddesc2(x1, uv_g, arm1.x, arm1.y)

it = 0

trail = Trail()


def loop_func2(event):
    global xg, x1, uv_g, phit1, it, plt


    arm1.move([phit1[0][it],phit1[1][it],phit1[2][it]])
    arm2.move([phit1[0][it],phit1[1][it],phit1[2][it]])
    arm3.move([phit1[0][it],phit1[1][it],phit1[2][it]])
    trail.add(Sphere(arm1.reg_e(),5).color("yellow"))
    trail.add(Sphere(arm2.reg_e(),5).color("yellow"))
    trail.add(Sphere(arm3.reg_e(),5).color("yellow"))

    plt.clear()
    plt += [arm1.fp(), arm2.fp(), arm3.fp(), floor, ball, trail.s()]
    plt.render()
    # video.add_frame()


    it += 10


#-----------------------------------------------------
#  main 
#-----------------------------------------------------
plt.initialize_interactor()
plt.add_callback("timer", loop_func2)
plt.timer_callback("start")
plt.show(viewup='z').close()
# video.close()
