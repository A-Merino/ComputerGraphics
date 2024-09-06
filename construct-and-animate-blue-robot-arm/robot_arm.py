from vedo import *
import kinemat as km

class RobArm:

    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.phi = p
        t01, t02, t03, t04, e = km.fk([p,0,0,0], [x, y, 105], 51.5, 246, [-235,0,32.5])

        base = Box([x,y,45], 180, 180, 90).texture(dataurl+'textures/wood3.jpg').color("blue")
        vent1 = Cylinder([x+90, y, 0], 75, 1, axis=[1,0,0]).color("black")
        vent3 = Cylinder([x-90, y, 0], 75, 1, axis=[1,0,0]).color("black")
        vent2 = Cylinder([x, y+90, 0], 75, 1, axis=[0,1,0]).color("black")
        vent4 = Cylinder([x, y-90, 0], 75, 1, axis=[0,1,0]).color("black")
        base_cyl = Cylinder([x,y,95], 90,10, axis=[0,0,1]).texture(dataurl+'textures/wood3.jpg').color("blue")

        self.b = Assembly((base, vent1, vent2, vent3, vent4, base_cyl))


        f1_turn = Cylinder([0,0,0], 90,10, axis=[0,0,1]).color("black")
        f1_tb = Cylinder([0,0,10], 90,10, axis=[0,0,1]).texture(dataurl+'textures/wood3.jpg').color("blue")
        f1_rec = Box([15,0,23.25], 120, 170, 16.5).texture(dataurl+'textures/wood3.jpg').color("blue")
        f1_h1 = Cylinder([0,60,51.5], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f1_h2 = Cylinder([0,-60,51.5], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f1_cov = Cylinder([0,68.5,51.5], 20, 2, axis=[0,1,0]).color('black')
        f1_cov2 = Cylinder([0,-68.5,51.5], 20, 2, axis=[0,1,0]).color('black')
        f1_mot = Box([105,0,46.5], 60, 170, 60).color('black')
        self.f1 = Assembly((f1_turn,f1_tb, f1_rec, f1_h1, f1_h2, f1_cov, f1_cov2, f1_mot)).apply_transform(t01)


        f2_base = Cylinder([0,0,0], 50, 105, axis=[0,1,0]).color('black')
        f2_arm = Cylinder([0,0,112.5], 25, 175, axis=[0,0,1]).color('grey')
        f2_h1 = Cylinder([0,60,246], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_h2 = Cylinder([0,-60,246], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_con = Box([0,0,200], 100, 135, 20).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_lid = Box([0,0,212.5], 50, 50, 25).color('black')
        f2_clasp = Cone([0,0,130], 65, 120, axis=[0,0,-1]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_cov = Cylinder([0,68.5,246], 20, 2, axis=[0,1,0]).color('black')
        f2_cov2 = Cylinder([0,-68.5,246], 20, 2, axis=[0,1,0]).color('black')

        self.f2 = Assembly((f2_base,f2_arm, f2_clasp, f2_h1, f2_h2, f2_cov, f2_cov2, f2_con, f2_lid)).apply_transform(t02)

        f3_base1 = Cylinder([0,45,0], 50, 15, axis=[0,1,0]).color('black')
        f3_base2 = Cylinder([0,-45,0], 50, 15, axis=[0,1,0]).color('black')
        f3_con = Cylinder([0,0,32.5], 5, 130, axis=[0,1,0]).color('black')
        f3_arm = Cylinder([-95,0,32.5], 25, 190, axis=[1,0,0]).color('grey')
        f3_ac = Cylinder([-42.5,0,32.5], 30, 100, axis=[1,0,0]).color('black')
        f3_joint = Box([10,0,40], 30, 50, 75).color('black')
        self.f3 = Assembly((f3_base1, f3_base2, f3_arm, f3_ac, f3_joint,f3_con)).apply_transform(t03)

        f4_box = Box([0,0,0], 15,30,30).color('black')
        f4_act = Box([17.5,52.5,0], 45,25,30).color('black')
        f4_cc = Box([35,-39,0], 10,2,30).texture(dataurl+'textures/wood3.jpg').color('blue')
        f4_cc2 = Box([35,39,0], 10,2,30).texture(dataurl+'textures/wood3.jpg').color('blue')
        f4_tw = Box([17.5,0,0], 20,60,30).color('black')
        f4_cov1 = Cylinder([17.5, -35,0], 20, 10, axis=(0,1,0)).texture(dataurl+'textures/wood3.jpg').color("blue") 
        f4_cov2 = Cylinder([17.5, 35,0], 20, 10, axis=(0,1,0)).texture(dataurl+'textures/wood3.jpg').color("blue") 
        f4_clasp = Cone([100,0,0], 41, 120, axis=[1,0,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f4_white = Box([35,0,0], 15,30,30).color('white')

        self.f4 = Assembly((f4_box,f4_clasp, f4_white, f4_tw, f4_cov1, f4_cov2, f4_cc, f4_cc2, f4_act)).apply_transform(t04)

    def fp(self):
        return Assembly((self.b, self.f1, self.f2, self.f3, self.f4))

    def move(self, p):
        t01, t02, t03, t04, e = km.fk([self.phi+p[0], p[1],p[2],p[3]], [self.x, self.y, 105], 51.5, 246, [-235,0,32.5])


        f1_turn = Cylinder([0,0,0], 90,10, axis=[0,0,1]).color("black")
        f1_tb = Cylinder([0,0,10], 90,10, axis=[0,0,1]).texture(dataurl+'textures/wood3.jpg').color("blue")
        f1_rec = Box([15,0,23.25], 120, 170, 16.5).texture(dataurl+'textures/wood3.jpg').color("blue")
        f1_h1 = Cylinder([0,60,51.5], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f1_h2 = Cylinder([0,-60,51.5], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f1_cov = Cylinder([0,68.5,51.5], 20, 2, axis=[0,1,0]).color('black')
        f1_cov2 = Cylinder([0,-68.5,51.5], 20, 2, axis=[0,1,0]).color('black')
        f1_mot = Box([105,0,46.5], 60, 170, 60).color('black')
        self.f1 = Assembly((f1_turn,f1_tb, f1_rec, f1_h1, f1_h2, f1_cov, f1_cov2, f1_mot)).apply_transform(t01)


        f2_base = Cylinder([0,0,0], 50, 105, axis=[0,1,0]).color('black')
        f2_arm = Cylinder([0,0,112.5], 25, 175, axis=[0,0,1]).color('grey')
        f2_h1 = Cylinder([0,60,246], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_h2 = Cylinder([0,-60,246], 50, 15, axis=[0,1,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_con = Box([0,0,200], 100, 135, 20).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_lid = Box([0,0,212.5], 50, 50, 25).color('black')
        f2_clasp = Cone([0,0,130], 65, 120, axis=[0,0,-1]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f2_cov = Cylinder([0,68.5,246], 20, 2, axis=[0,1,0]).color('black')
        f2_cov2 = Cylinder([0,-68.5,246], 20, 2, axis=[0,1,0]).color('black')

        self.f2 = Assembly((f2_base,f2_arm, f2_clasp, f2_h1, f2_h2, f2_cov, f2_cov2, f2_con, f2_lid)).apply_transform(t02)

        f3_base1 = Cylinder([0,45,0], 50, 15, axis=[0,1,0]).color('black')
        f3_base2 = Cylinder([0,-45,0], 50, 15, axis=[0,1,0]).color('black')
        f3_con = Cylinder([0,0,32.5], 5, 130, axis=[0,1,0]).color('black')
        f3_arm = Cylinder([-95,0,32.5], 25, 190, axis=[1,0,0]).color('grey')
        f3_ac = Cylinder([-42.5,0,32.5], 30, 100, axis=[1,0,0]).color('black')
        f3_joint = Box([10,0,40], 30, 50, 75).color('black')
        self.f3 = Assembly((f3_base1, f3_base2, f3_arm, f3_ac, f3_joint,f3_con)).apply_transform(t03)

        f4_box = Box([0,0,0], 15,30,30).color('black')
        f4_act = Box([17.5,52.5,0], 45,25,30).color('black')
        f4_cc = Box([35,-39,0], 10,2,30).texture(dataurl+'textures/wood3.jpg').color('blue')
        f4_cc2 = Box([35,39,0], 10,2,30).texture(dataurl+'textures/wood3.jpg').color('blue')
        f4_tw = Box([17.5,0,0], 20,60,30).color('black')
        f4_cov1 = Cylinder([17.5, -35,0], 20, 10, axis=(0,1,0)).texture(dataurl+'textures/wood3.jpg').color("blue") 
        f4_cov2 = Cylinder([17.5, 35,0], 20, 10, axis=(0,1,0)).texture(dataurl+'textures/wood3.jpg').color("blue") 
        f4_clasp = Cone([100,0,0], 41, 120, axis=[1,0,0]).texture(dataurl+'textures/wood3.jpg').color('blue')
        f4_white = Box([35,0,0], 15,30,30).color('white')

        self.f4 = Assembly((f4_box,f4_clasp, f4_white, f4_tw, f4_cov1, f4_cov2, f4_cc, f4_cc2, f4_act)).apply_transform(t04)