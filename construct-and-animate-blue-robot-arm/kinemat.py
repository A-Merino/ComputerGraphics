import numpy as np

def RotationMatrix(theta, axis_name):
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

def getLocalFrameMatrix(R_ij, t_ij): 
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
   

def fk(phi, L1, L2, L3, L4):

 # Matrix of Frame 1 (written w.r.t. Frame 0, which is the previous frame) 
    R_01 = RotationMatrix(phi[0], axis_name = 'z')   # Rotation matrix
    p1   = np.array([[L1[0]],[L1[1]], [L1[2]]])              # Frame's origin (w.r.t. previous frame)
    t_01 = p1                                      # Translation vector

    T_01 = getLocalFrameMatrix(R_01, t_01)         # Matrix of Frame 1 w.r.t. Frame 0 (i.e., the world frame)


    # Matrix of Frame 2 (written w.r.t. Frame 1, which is the previous frame)   
    R_12 = RotationMatrix(phi[1], axis_name = 'y')   # Rotation matrix
    p2   = np.array([[0], [0.0], [L2]])           # Frame's origin (w.r.t. previous frame)
    t_12 = p2                                      # Translation vector

    # Matrix of Frame 2 w.r.t. Frame 1 
    T_12 = getLocalFrameMatrix(R_12, t_12)

    # Matrix of Frame 2 w.r.t. Frame 0 (i.e., the world frame)
    T_02 = T_01 @ T_12



    # Matrix of Frame 3 (written w.r.t. Frame 2, which is the previous frame)   
    R_23 = RotationMatrix(phi[2], axis_name = 'y')   # Rotation matrix
    p3   = np.array([[0.0],[0.0], [L3]])           # Frame's origin (w.r.t. previous frame)
    t_23 = p3                                      # Translation vector

    # Matrix of Frame 3 w.r.t. Frame 2 
    T_23 = getLocalFrameMatrix(R_23, t_23)

    # Matrix of Frame 3 w.r.t. Frame 0 (i.e., the world frame)
    T_03 = T_02 @ T_23


    R_34 = RotationMatrix(phi[3], axis_name = 'x')   # Rotation matrix
    p4   = np.array([[L4[0]],[L4[1]], [L4[2]]])           # Frame's origin (w.r.t. previous frame)
    t_34 = p4                                      # Translation vector

    # Matrix of Frame 3 w.r.t. Frame 2 
    T_34 = getLocalFrameMatrix(R_34, t_34)

    # Matrix of Frame 3 w.r.t. Frame 0 (i.e., the world frame)
    T_04 = T_03 @ T_34



    return T_01, T_02, T_03, T_04, T_04[:-1,-1]
