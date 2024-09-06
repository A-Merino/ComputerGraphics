import numpy as np
import kinemat as km



def f(x):
    # Assign the x and y coordinates 
    xi = x[0][0]   # x-value 
    yi = x[1][0]   # y-value 
    zi = x[2][0]
    
    # Calculate the value of the function at (x,y)
    ui = xi      # u-value
    vi = yi      # v-value
    wi = zi
    
    u = np.array([[ui],[vi],[wi]])     
    return u

def japrx(x, dx, dy, dz):
    """Computes the Jacobian numerically 
    
    Args:
        x (np.ndarray): A 2x1 column matrix containing (x,y)
 
    Returns:
        u (np.ndarray): A 2x2 matrix containing the Jacobian
    """
    
    xi = x[0][0]   # x-value 
    yi = x[1][0]   # y-value
    zi = x[2][0]
    
    
    delta_x = np.array([[dx],[0],[0]]) 
    delta_y = np.array([[0],[dy],[0]])
    delta_z = np.array([[0],[0],[dz]])
    
    DuDx = (f(x + delta_x) - f(x)) / dx 
    DuDy = (f(x + delta_y) - f(x)) / dy
    DuDz = (f(x + delta_z) - f(x)) / dz
    
    J = np.concatenate((DuDx,DuDy, DuDz), axis=1)

    return J


def graddesc(x, uv_g):

    xtrace = x
    delta_f = uv_g - f(x)           # Difference between predicted and target 
    dist = np.linalg.norm(delta_f)  # Error measure (distance)
    table = []                      # Table to store the iteration results                        

    it = 0                          # Iteration count 

    # Delta f 
    while dist > 0.1:    
        delta_f = uv_g - f(x)
        dist = np.linalg.norm(delta_f)

        # Jacobian at x
        J = japrx(x, .1, .1,.1)       # Numerica Jacobian 

        # Inverse Jacobian
        Jinv = np.linalg.inv(J)

        # Delta x for the Delta f using the inverse Jacobian
        delta_x_mapped = Jinv @ delta_f

        # Predicted function f(x + delta_x)
        f_predicted = f(x + delta_x_mapped)


        # Scale down the step for delta x 
        delta_x_mapped_slow = 0.05 * delta_x_mapped

        # Function value at updated scaled down location  
        f_predicted_slow = f(x + delta_x_mapped_slow)
        
        table.append([dist, uv_g, f_predicted,x])

        x = x + delta_x_mapped_slow
        

        xtrace = np.append(xtrace, x, axis=1)
        it +=1
    return xtrace, table


def f2(phi, x, y):

	# Assign the x and y coordinates 
    # print(phi)
    w1,w2,w3,w4, e = km.fk(phi, [x, y, 105], 51.5, 246, [-235,0,32.5])


    # Calculate the value of the function at (x,y)
    ui = e[0]     # u-value
    vi = e[1]      # v-value
    wi = e[2]
    
    u = np.array([[phi[0][0]],[phi[1][0]],[phi[2][0]]])     
    return u


def japrx2(phi, dp1, dp2, dp3, x, y):
    """Computes the Jacobian numerically 
    
    Args:
        x (np.ndarray): A 2x1 column matrix containing (x,y)
 
    Returns:
        u (np.ndarray): A 2x2 matrix containing the Jacobian
    """
    
    phi1 = phi[0][0]   # x-value 
    phi2 = phi[1][0]   # y-value
    phi3 = phi[2][0]
    
    
    delta_p1 = np.array([[dp1],[0],[0]]) 
    delta_p2 = np.array([[0],[dp2],[0]])
    delta_p3 = np.array([[0],[0],[dp3]])
    
    DuDp1 = (f2(phi + delta_p1, x, y) - f2(phi, x, y)) / (dp1 * (np.pi / 180))
    DuDp2 = (f2(phi + delta_p2, x, y) - f2(phi, x, y)) / (dp2 * (np.pi / 180))
    DuDp3 = (f2(phi + delta_p3, x, y) - f2(phi, x, y)) / (dp3 * (np.pi / 180))
    
    J = np.concatenate((DuDp1,DuDp2, DuDp3), axis=1)

    return J

def graddesc2(phi, uv_g, x, y):

    phitrace = phi
    delta_f = uv_g - f2(phi, x, y)           # Difference between predicted and target 
    dist = np.linalg.norm(delta_f)  # Error measure (distance)
    table = []                      # Table to store the iteration results                        

    it = 0                          # Iteration count 

    # Delta f 
    while dist > 0.1:  
        # print(f2(phi, x, y))  
        delta_f = uv_g - f2(phi, x, y)
        dist = np.linalg.norm(delta_f)

        # Jacobian at x
        J = japrx2(phi, .1, .1,.1, x, y)       # Numerica Jacobian 

        # Inverse Jacobian
        Jinv = np.linalg.inv(J)

        # Delta x for the Delta f using the inverse Jacobian
        delta_p_mapped = Jinv @ delta_f
        # print(delta_f)

        # Predicted function f(x + delta_x)
        f_predicted = f2(phi + delta_p_mapped, x, y)


        # Scale down the step for delta x 
        delta_p_mapped_slow = 0.05 * delta_p_mapped

        # Function value at updated scaled down location  
        f_predicted_slow = f2(phi + delta_p_mapped_slow, x, y)
        
        table.append([dist, uv_g, f_predicted,phi])
        # print(phi)
        phi = phi + delta_p_mapped_slow
        

        phitrace = np.append(phitrace, phi, axis=1)
        it +=1
    return phitrace, table