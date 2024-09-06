from vedo import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource 
from person import Person

video = Video("animation_2.mp4", fps=10)


def calc1():
    X, Y = np.meshgrid(np.arange(0,100), np.arange(0,100))

    goal = np.array([90.0, 50.0])

    Z = f(X, Y, goal)

    U, V = gradient(Z)
    all_cost = Z
    # plot_grad(X, Y, Z)
    # show_arr(X[40:60,80:100], Y[40:60,80:100], V[40:60,80:100], U[40:60,80:100], Z[40:60,80:100])
    all_obs = [([50,50], 10),([70,0], 5),([70,10], 5),([70,20], 5),([70,30], 5),([70,37], 5),([70,40], 5),([70,99], 5),([70,62], 5),([70,60], 5),([70,70], 5),([70,80], 5),([70,90], 5)]
    for ob in all_obs:
        rad = ob[1]
        cen_pos = np.array(ob[0])
        dist = f(X, Y, cen_pos)

        cost = obstacle(dist, rad)
        # plot_grad(X, Y, dist)
        all_cost += cost
        U1, V1 = gradient(all_cost)
        # show_arr(X,Y, V1, U1, all_cost)


    Ua, Va = gradient(all_cost)


    # plot_grad(X, Y, all_cost)

    # print(Ua[49,50])
    # show_arr(X[40:60,40:60], Y[40:60,40:60], Va[40:60,40:60], Ua[40:60,40:60], all_cost[40:60,40:60])
    # show_arr(X[40:60, 80:99], Y[40:60, 80:99], Va[40:60, 80:99], Ua[40:60, 80:99], all_cost[40:60, 80:99])

    p1 = np.array([3.0, 40.0])
    p2 = np.array([10.0, 60.0])
    p3 = np.array([10.0, 80.0])
    p4 = np.array([10.0, 20.0])
    p5 = np.array([10.0, 90.0])
    p6 = np.array([10.0, 10.0])

    p1p = desc(X, Y, p1, goal, all_cost)
    p2p = desc(X, Y, p2, goal, all_cost)
    p3p = desc(X, Y, p3, goal, all_cost)
    p4p = desc(X, Y, p4, goal, all_cost)
    p5p = desc(X, Y, p5, goal, all_cost)
    p6p = desc(X, Y, p6, goal, all_cost)
    coord = np.array(p6p).T
    # print(line)
    # plt.quiver(X, Y, Va, Ua, all_cost)
    # plt.plot(coord[0], coord[1])
    # plt.show()

    animate_1(p1p, p2p, p3p, p4p, p5p, p6p)


def calc2():
    X, Y = np.meshgrid(np.arange(0,100), np.arange(0,100))
    subgoal = np.array([50.0,20.0])
    goal = np.array([5.0, 20.0])
    # goal = np.array([90.0, 50.0])
    Z1 = f(X, Y, subgoal, step=True)
    Z2 = f(X, Y, goal)
    all_cost = Z1 + Z2

    all_obs = [([5, 5], 5),([10,5], 5),([15,5], 5),([20,5], 5),([25,5], 5),([30,5], 5),([35,5], 5),
               ([40,5], 5),([45,5], 5),([50,5], 5),([55,5], 5),([60,5], 5),([65,5], 5),([70,5], 5),
               ([75,5], 5),([80,5], 5),([85,5], 5),([90,5], 5),([95,5], 5),([99,5], 5),
               ([5, 35], 5),([10,35], 5),([15,35], 5),([20,35], 5),([25,35], 5),([30, 35], 5),([35,35], 5),
               ([40,35], 5),([65, 35], 5),([70,35], 5),
               ([75,35], 5),([80,35], 5),([85,35], 5),([90,35], 5),([95,35], 5),([99,35], 5),
               ([40,40], 5),([40,45], 5),([40,50], 5),([40,55], 5),([40,60], 5),([40, 65], 5),([40,70], 5),
               ([40,75], 5),([40,80], 5),([40,85], 5),([40,90], 5),([40,95], 5),([40, 100], 5),
               ([65,40], 5),([65,45], 5),([65,50], 5),([65,55], 5),([65,60], 5),([65, 65], 5),([65,70], 5),
               ([65,75], 5),([65,80], 5),([65,85], 5),([65,90], 5),([65,95], 5),([65, 99], 5)]
    for ob in all_obs:
        rad = ob[1]
        cen_pos = np.array(ob[0])
        dist = f(X, Y, cen_pos)

        cost = obstacle(dist, rad)
        # plot_grad(X, Y, dist)
        all_cost += cost
        # U1, V1 = gradient(all_cost)
        # show_arr(X,Y, V1, U1, all_cost)

    p1 = np.array([48.0, 80.0])
    p2 = np.array([53.0, 80.0])
    p3 = np.array([56.0, 80.0])
    p4 = np.array([90.0, 27.0])
    p5 = np.array([90.0, 21.0])
    p6 = np.array([90.0, 15.0])

    U, V = gradient(all_cost)
    p1p = desc(X, Y, p1, goal, all_cost)
    p2p = desc(X, Y, p2, goal, all_cost)
    p3p = desc(X, Y, p3, goal, all_cost)
    p4p = desc(X, Y, p4, goal, all_cost)
    p5p = desc(X, Y, p5, goal, all_cost)
    p6p = desc(X, Y, p6, goal, all_cost)
    # c1 = np.array(p1p).T
    # c2 = np.array(p2p).T
    # c3 = np.array(p3p).T
    # c4 = np.array(p4p).T
    # c5 = np.array(p5p).T
    # c6 = np.array(p6p).T
    # # print(line)
    # plt.quiver(X, Y, V, U, all_cost)
    # plt.plot(c1[0], c1[1])
    # plt.plot(c2[0], c2[1])
    # plt.plot(c3[0], c3[1])
    # plt.plot(c4[0], c4[1])
    # plt.plot(c5[0], c5[1])
    # plt.plot(c6[0], c6[1])
    # plt.show()


    # plot_grad(X, Y, all_cost)
    # show_arr(X,Y, V, U, all_cost)
    animate_1(p1p,p2p,p3p,p4p,p5p,p6p)


def desc(x, y, pos, goal, grad):
    trace = []
    # s = []
    trace.append(np.copy(pos))
    count = 1
    u, v = gradient(grad)
    # while np.linalg.norm(pos - goal) > 0.85:
    while count < 200:
    # while count < 100:
        # show_arr(x, y, v, u, grad)
        # plt.show()
        pos[0], pos[1] = new_pos(pos[0], pos[1], u, v)
        # print(pos[0], pos[1])
        trace.append(np.copy(pos))
        count += 1

    return trace


def new_pos(x, y, u, v):
    if y % 1 == 0 and x % 1 == 0:
        return x + v[int(y)][int(x)], y + u[int(y)][int(x)]
    else:
        x_slope1 = (v[int(np.floor(y))][int(np.floor(x))] * (np.ceil(x) - x)) + (v[int(np.floor(y))][int(np.ceil(x))] * (x - np.floor(x)))
        x_slope2 = (v[int(np.ceil(y))][int(np.floor(x))] * (np.ceil(x) - x)) + (v[int(np.ceil(y))][int(np.ceil(x))] * (x - np.floor(x)))
        y_slope1 = (u[int(np.floor(y))][int(np.floor(x))] * (np.ceil(y) - y)) + (u[int(np.ceil(y))][int(np.floor(x))] * (y - np.floor(y)))
        y_slope2 = (u[int(np.floor(y))][int(np.ceil(x))] * (np.ceil(y) - y)) + (u[int(np.ceil(y))][int(np.ceil(x))] * (y - np.floor(y)))

        # print(x, y, v[int(np.floor(y))][int(np.floor(x))], u[int(np.floor(y))][int(np.floor(x))])
        # return x + ((x_slope1 + x_slope2)/2), y + ((y_slope1 + y_slope2)/2)
        return x + (v[int(np.floor(y))][int(np.floor(x))] * 1), y + (u[int(np.floor(y))][int(np.floor(x))] * 1)

def obstacle(d, r):
    inx = d == 0
    d[inx] = 0.0001
    peak = np.log((r / d) + r)
    peak[d > r] = 0
    return peak


def f(x, y, pos, step=False):
    px = np.copy(x)
    py = np.copy(y)
    px[:, :] = pos[0]
    py[:, :] = pos[1]
    if step:
        return np.sqrt(((x - px)**2) + ((y - py)**2)) / 3

    return np.sqrt(((x - px)**2) + ((y - py)**2))


def gradient(z):
    u, v = np.gradient(z) 
    neg = (-1) * np.eye(u.shape[0])
    return u @ neg, v @ neg


def plot_grad(x, y, z):
    ls = LightSource(90)
    rgb = ls.shade(z, cmap=plt.get_cmap("coolwarm"),blend_mode="soft")

    ax = plt.figure().add_subplot(projection="3d")
    ax.plot_surface(x, y, z, facecolors=rgb)
    plt.show()


def plot_a(u, v):
    plt.plot(u, v)
    plt.show()


def show_arr(x, y, u, v, z):
    plt.quiver(x, y, u, v, z)
    plt.show()

plane = Plotter()
floor = Box([50, 50, -5], 100, 100, 10)
# obs = Cylinder([50,50,5], 8, 10).color("purple")
wall1 = Box([50,5,5],100,8,10).color("purple")
wall2 = Box([22,35,5],44,8,10).color("purple")
wall3 = Box([80.5,35,5],39,8,10).color("purple")
wall4 = Box([40,67.5,5],8,65,10).color("purple")
wall5 = Box([65,67.5,5],8,65,10).color("purple")
plane += [floor, wall1, wall2, wall3, wall4, wall5]

def animate_1(a, b, c, d, e, f):
    global plane
    p1 = Person(a[0][0],a[1][0])
    p2 = Person(b[0][0],b[1][0])
    p3 = Person(c[0][0],c[1][0])
    p4 = Person(d[0][0],d[1][0])
    p5 = Person(e[0][0],e[1][0])
    p6 = Person(f[0][0],f[1][0])
    # obstacle
    # plane.initialize_interactor()
    for i in range(len(a)):
        p1.move(a[i][0], a[i][1])
        p2.move(b[i][0], b[i][1])
        p3.move(c[i][0], c[i][1])
        p4.move(d[i][0], d[i][1])
        p5.move(e[i][0], e[i][1])
        p6.move(f[i][0], f[i][1])
        # print(pos)
        plane.clear()
        plane += [floor, wall1, wall2, wall3, wall4, wall5,
                 p1.fp(), p2.fp(), p3.fp(), p4.fp(), p5.fp(), p6.fp()]
        plane.render()
        video.add_frame()

    

def looper(c):
    # calc1()
    calc2()


def main():
    plane.initialize_interactor()
    plane.add_callback("timer", looper)
    plane.timer_callback("start")
    plane.show(viewup='z').close()
    video.close()

# calc2()

main()