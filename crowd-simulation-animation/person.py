from vedo import *

class Person:
    def __init__(self, x, y):
        self.head = Sphere([x,y, 4], 1.5).color("red")
        self.body = Cone([x,y, 0], 2, 7.5).color("blue") 

    def move(self,x, y):
        self.head = Sphere([x,y,4], 1.5).color("red")
        self.body = Cone([x,y, 0], 2, 7.5).color("blue") 

    def fp(self):
        return self.head, self.body
