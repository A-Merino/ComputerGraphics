from vedo import *
from robot_arm import RobArm


plt = Plotter(axes=1)






f2_clasp = Pyramid([0,0,150], 125, 125, axis=[0,0,-1]).color('blue')




plt += [f2_clasp]

plt.initialize_interactor()
plt.show().close()
