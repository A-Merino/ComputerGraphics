#!/usr/bin/env python
# coding: utf-8

import cvxopt
from cvxopt import matrix, printing

from vedo import *

import time



class RobotArm():
	'''
		Robot arm.
	'''
	
	def __init__(self, partLengths, arm_location):
 

		# Arm location (position of the first frame)
		self.arm_location = arm_location

		# Lentghs of the parts 
		self.L1, self.L2, self.L3, self.L4 = partLengths
		


	def buildAllParts(self):
		'''
			Build the robot mesh with all parts. 
			Robot is created in its neutral pose. 
		'''

		# Construct the arm parts 
		self.Part1 = self.createArmPartMesh(self.L1)	
		self.Part2 = self.createArmPartMesh(self.L2)			
		self.Part3 = self.createArmPartMesh(self.L3)			
		self.Part4 = self.createCoordinateFrameMesh()  # End effector (not an actual frame part)			



	def setPose(self, Phi):
		'''
			Set pose of the robot arm.  
		'''

		# Obtain local-to-global matrices from forward kinematics
		T_01, T_02, T_03, T_04, e = self.forward_kinematics(Phi)

		# Re-create robot in its neural position
		self.buildAllParts()

		# Transforms parts to position it at its correct
		# location and orientation. 
		self.Part1.apply_transform(T_01)  
		self.Part2.apply_transform(T_02)  
		self.Part3.apply_transform(T_03)  
		self.Part4.apply_transform(T_04)  




	def RotationMatrix(self, theta, axis_name):
	    """ calculate single rotation of $theta$ matrix around x,y or z
	        code from: https://programming-surgeon.com/en/euler-angle-python-en/
	    input
	        theta = rotation angle(degrees)
	        axis_name = 'x', 'y' or 'z'
	    output
	        3x3 rotation matrix
	    """

	    c = np.cos(theta * np.pi / 180)
	    s = np.sin(theta * np.pi / 180)
		
	    if axis_name =='x':
	        rotation_matrix = np.array([[1, 0,  0],
	                                    [0, c, -s],
	                                    [0, s,  c]])
	    if axis_name =='y':
	        rotation_matrix = np.array([[ c,  0, s],
	                                    [ 0,  1, 0],
	                                    [-s,  0, c]])
	    elif axis_name =='z':
	        rotation_matrix = np.array([[c, -s, 0],
	                                    [s,  c, 0],
	                                    [0,  0, 1]])
	    return rotation_matrix




	def createCoordinateFrameMesh(self):
	    """Returns the mesh representing a coordinate frame
	    Args:
	      No input args
	    Returns:
	      F: vedo.mesh object (arrows for axis)
	      
	    """         
	    _shaft_radius = 0.05
	    _head_radius = 0.10
	    _alpha = 1
	    
	    
	    # x-axis as an arrow  
	    x_axisArrow = Arrow(start_pt=(0, 0, 0),
	                        end_pt=(1, 0, 0),
	                        s=None,
	                        shaft_radius=_shaft_radius,
	                        head_radius=_head_radius,
	                        head_length=None,
	                        res=12,
	                        c='red',
	                        alpha=_alpha)

	    # y-axis as an arrow  
	    y_axisArrow = Arrow(start_pt=(0, 0, 0),
	                        end_pt=(0, 1, 0),
	                        s=None,
	                        shaft_radius=_shaft_radius,
	                        head_radius=_head_radius,
	                        head_length=None,
	                        res=12,
	                        c='green',
	                        alpha=_alpha)

	    # z-axis as an arrow  
	    z_axisArrow = Arrow(start_pt=(0, 0, 0),
	                        end_pt=(0, 0, 1),
	                        s=None,
	                        shaft_radius=_shaft_radius,
	                        head_radius=_head_radius,
	                        head_length=None,
	                        res=12,
	                        c='blue',
	                        alpha=_alpha)
	    
	    originDot = Sphere(pos=[0,0,0], 
	                       c="black", 
	                       r=0.10)


	    # Combine the axes together to form a frame as a single mesh object 
	    F = x_axisArrow + y_axisArrow + z_axisArrow + originDot
	        
	    return F


	def getLocalFrameMatrix(self, R_ij, t_ij): 
	    """Returns the matrix representing the local frame
	    Args:
	      R_ij: rotation of Frame j w.r.t. Frame i 
	      t_ij: translation of Frame j w.r.t. Frame i 
	    Returns:
	      T_ij: Matrix of Frame j w.r.t. Frame i. 
	      
	    """             
	    # Rigid-body transformation [ R t ]
	    T_ij = np.block([[R_ij,                t_ij],
	                     [np.zeros((1, 3)),       1]])
	    
	    return T_ij


	def createArmPartMesh(self, L):

		# Create a sphere to show as an example of a joint
		radius = 0.4
		sphere1 = Sphere(r=radius).pos(0,0,0).color("gray").alpha(.8)
		
		# Create the coordinate frame mesh and transform
		Frame1Arrows = self.createCoordinateFrameMesh()
		
		# Now, let's create a cylinder and add it to the local coordinate frame
		link1_mesh = Cylinder(r=0.4, 
		                      height=L, 
		                      pos = (L/2+radius,0,0),
		                      c="white", 
		                      alpha=.8, 
		                      axis=(1,0,0)
		                      )
		
		# Combine all parts into a single object 
		Part = Frame1Arrows + link1_mesh + sphere1
		
		return Part
	

	def forward_kinematics(self, Phi):
		
		# Radius of the sphere representing the joint
		radius = 0.4

		
		# Joint angle 
		phi1 =  Phi[0]    # Rotation angle of part 1 in degrees
		
		# Matrix of Frame 1 (written w.r.t. Frame 0, which is the previous frame) 
		R_01 = self.RotationMatrix(phi1, axis_name = 'z')   # Rotation matrix
		t_01 = self.arm_location                            # Frame's origin (w.r.t. previous frame)
		
		T_01 = self.getLocalFrameMatrix(R_01, t_01)         # Matrix of Frame 1 w.r.t. Frame 0 


		

		# Joint angle 
		phi2 = Phi[1]    # Rotation angle of part 2 in degrees

		# Matrix of Frame 2 (written w.r.t. Frame 1, which is the previous frame) 	
		R_12 = self.RotationMatrix(phi2, axis_name = 'z')   # Rotation matrix
		t_12 = np.array([[self.L1+2*radius],[0.0], [0.0]])  # Frame's origin (w.r.t. previous frame)
		
		T_12 = self.getLocalFrameMatrix(R_12, t_12)         # Matrix of Frame 2 w.r.t. Frame 1 
		
		# Matrix of Frame 2 w.r.t. Frame 0 (i.e., the world frame)
		T_02 = T_01 @ T_12

			


		phi3 = Phi[2]    # Rotation angle of the end-effector in degrees
			
		# Matrix of Frame 3 (written w.r.t. Frame 2, which is the previous frame) 	
		R_23 = self.RotationMatrix(phi3, axis_name = 'z')   # Rotation matrix
		t_23   = np.array([[self.L2+2*radius],[0.0], [0.0]])  # Frame's origin (w.r.t. previous frame)
		
		# Matrix of Frame 3 w.r.t. Frame 2 
		T_23 = self.getLocalFrameMatrix(R_23, t_23)
		
		# Matrix of Frame 3 w.r.t. Frame 0 (i.e., the world frame)
		T_03 = T_01 @ T_12 @ T_23
		



		phi4 = Phi[3]
			
		# Matrix of Frame 3 (written w.r.t. Frame 2, which is the previous frame) 	
		R_34 = self.RotationMatrix(phi4, axis_name = 'z')   # Rotation matrix
		t_34   = np.array([[self.L3+radius],[0.0], [0.0]])  # Frame's origin (w.r.t. previous frame)
		
		# Matrix of Frame 3 w.r.t. Frame 2 
		T_34 = self.getLocalFrameMatrix(R_34, t_34)
		
		# Matrix of Frame 3 w.r.t. Frame 0 (i.e., the world frame)
		T_04 = T_01 @ T_12 @ T_23 @ T_34

		e = T_04[0:3,-1]    # Last column of the last frame matrix

		return T_01, T_02, T_03, T_04, e





def main():

	# Create a robot arm 
	L = [5, 8, 3, 0]                 				# Lentghs of the parts
	arm_location = np.array([[2],[3], [3.0]])    	# Arm location (position of the first frame)
	myRobot = RobotArm(L, arm_location)             # The robot arm 


	# A short sequence of poses 
	Poses = np.array([[  0,  0,  0,  0],
					  [-30, 50, 30,  0],
					  [ 30,-50,-30,  0],
					  [  0,  0,  0,  0]])



	# Open a video file and force it to last 3 seconds in total. 
	# Creating a tmp file because the Vedo's video function creates 
	# a video that might not show in all players. So, we will call 
	# ffmpeg ourselves to modify the file to play in more players. 
	# See os.system() call at the end of this script.
	video = Video("tmp.mp4", 
	#              duration=4, 
	              backend='ffmpeg', 
	              fps = 4
	             ) 




	# Set the limits of the graph x, y, and z ranges 
	axes = Axes(xrange=(0,25), yrange=(-2,10), zrange=(0,6))
	# declare the class instance
	plt = Plotter(bg='beige', bg2='lb', axes=10, offscreen=False, interactive=False)

	plt.show(axes, viewup="z")


	for Phi in Poses:
		# Set robot pose 
		myRobot.setPose(Phi)
		# Clear plot before showing new iteration
		plt.clear()
		# All objects to Plotter.
		plt += axes
		plt += [myRobot.Part1, myRobot.Part2, myRobot.Part3, myRobot.Part4]

		# Show scene    
		plt.render()    #  What is the difference between render() and show()? 

		video.add_frame()

		# Sleep a bit 
		time.sleep(1)



	plt.show(axes, viewup="z").interactive().close()



	video.close()                         # merge all the recorded frames

	# Convert the video file to play on a wider range of video players 
	if os.path.exists("./animation.mp4"):
	    os.system("rm animation.mp4")
	    
	os.system("ffmpeg -i tmp.mp4 -pix_fmt yuv420p animation.mp4")
	os.system("rm tmp.mp4")




if __name__ == '__main__':
    main()



