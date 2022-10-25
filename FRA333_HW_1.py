#!/usr/bin/python3
from re import X
from turtle import forward, position
from trackbeebot import BeeBot
import matplotlib.pyplot as plt 
from matplotlib.patches import Polygon
import numpy as np
import math

class MyBeeBot(BeeBot):
    def __init__(self,a_i):
        super().__init__(a_i)
        self.a_i = a_i
        self.ww = 0
        self.x = 0
        self.y = 0
        self.forward_x = 0
        self.forward_y = 0
        self.a_0 = np.array([]) 
        self.a_1 = np.array([])
        self.p_0 = np.array([]) 
        self.p_1 = np.array([])
    
    def checkwall(self,i):
        #change position to index for check wall #linear Equation
        checkk = 0
        A = np.array([[math.sqrt(3)/2,math.sqrt(3)/2],[3/2,-3/2]])
        C = np.array([[self.x,self.y]]).T
        B = np.linalg.inv(A).dot(C)
        if (np.around(B[0]) == self.ww[0]).any():   
            result = np.where(self.ww[0] == np.around(B[0])) 
            if (self.ww[1][result[0]] == np.around(B[1])).any():        #wall
                if i == '1':
                    self.x -= self.forward_x
                    self.y -= self.forward_y 
                elif i == '2':
                    self.x += self.forward_x
                    self.y += self.forward_y 
                checkk = 1
        if checkk == 0:
            self.a_0 = np.append(self.a_0,int(np.around(B[0])))
            self.a_1 = np.append(self.a_1,int(np.around(B[1])))
            self.p_0 = np.append(self.p_0,self.x)
            self.p_1 = np.append(self.p_1,self.y)
    
    def trackBeeBot(self, c, W):
    
        self.ww = np.array([W[0],W[1]])

        #index a_i = [m,n]
        m = self.a_i[0]
        n = self.a_i[1]

        #position p = [x,y]
        self.x = math.sqrt(3)/2*(m+n)
        self.y = (3/2)*(m-n)
        self.forward_x = math.sqrt(3)
        self.forward_y = 0
        self.a_0 = np.append(self.a_0,m)
        self.a_1 = np.append(self.a_1,n)
        self.p_0 = np.append(self.p_0,self.x)
        self.p_1 = np.append(self.p_1,self.y)

        for i in c:
            #'0'->stop
            if i == '0':
                pass

            #'1'->forward         
            elif i == '1':
                self.x += self.forward_x
                self.y += self.forward_y
                self.checkwall(i)
            
            #'2'->backward  
            elif i == '2':
                self.x -= self.forward_x
                self.y -= self.forward_y
                self.checkwall(i)

            #'3'->turn left  #'4'->turn right
            elif i == '3' or i == '4':
                if i == '3':
                    theta = np.radians(-60)
                elif i == '4':
                    theta = np.radians(60)
                c,s = np.cos(theta), np.sin(theta)
                rotation = np.array(((c,-s,0),(s,c,0),(0,0,1))).dot(np.array([[self.forward_x],[self.forward_y],[1]]))
                self.forward_x,self.forward_y = rotation[0][0],rotation[1][0]
        A = np.array([self.a_0,self.a_1])  
        A = np.int64(A)
        P = np.array([self.p_1,self.p_0])  
        return A,P


        



            



            

        

    

   