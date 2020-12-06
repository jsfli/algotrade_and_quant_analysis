# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a python script for DryWall Calculator
"""

panel_sides_adj = {"+": -10, "-": -5, "*": -20, "TP": 40}

from math import pi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import requests
import yfinance as yf
import re

class DryWall(object):
    def __init__(self,
                 panel_number,
                 panel_model,
                 width_design_mm,
                 height_design_mm,
                 thickness_design_mm,
                 holes
                 ):
        # DryWall identifications
        self.panel_number = panel_number
        self.panel_model = panel_model
        
        #DryWall design dimension
        self.width_design_mm = width_design_mm
        self.height_design_mm = height_design_mm
        self.m2_design = (self.width_design_mm / 1000) * (self.height_design_mm / 1000)
        self.thickness_mm = thickness_design_mm
        self.m3_design = self.m2_design * (self.thickness_mm / 1000)
        
        #DryWall manufacturing actual dimension
        self.width_actual_mm = self.width_design_mm
        
        #actual width adjustment based on below logic
        if "+" in panel_model:
            self.width_actual_mm += panel_sides_adj["+"]
        if "-" in panel_model:
            self.width_actual_mm += panel_sides_adj["-"]
        if "*" in panel_model:
            self.width_actual_mm += panel_sides_adj["*"]
        if "TP" in panel_model:
            self.width_actual_mm += panel_sides_adj["TP"]
        
        self.height_actual_mm = self.height_design_mm - 50
        self.m2_actual = (self.width_actual_mm / 1000) * (self.height_actual_mm / 1000)
        
        #full length count as 1, half length count as 0.5
        self.holes = int(holes)
        
        
        if not "TP" in panel_model:
            #hole radius is 16mm
            self.holes_total_actual_volume_m3 = pi * 0.016 * 0.016 * (self.height_actual_mm / 1000) * self.holes 
        else:
            self.holes_total_actual_volume_m3 = pi * 0.016 * 0.016 * (self.width_actual_mm / 1000) * self.holes
            
        
        self.m3_actual = self.m2_actual * (self.thickness_mm / 1000) - self.holes_total_actual_volume_m3
        
        if re.findall(r'\dG', self.panel_model) == []:
            self.gang_total = 0 
        else:
            self.gang_total = int(re.findall(r'\dG', self.panel_model)[0][0])
        
        self.gang_single = self.gang_total
        self.gang_double = 0
        
    def has_gang_double(self): # each panel can only have 1 double gang
            if self.gang_single > 0:
                self.gang_double = 1
                self.gang_single = self.gang_total - self.gang_double
            print("Confirmed panel {} has double gang.".format(self.panel_number))
    
    def __str__(self):                
        return "Panel Number: \t\t{0}\n"\
               "Panel Model: \t\t{1}\n"\
               "Design Width (mm): \t{2}\n"\
               "Design Height (mm): \t{3}\n"\
               "Design Area (m2): \t{4}\n"\
               "Production Width (mm): \t{5}\n"\
               "Production Height (mm) {6}\n"\
               "Production Area (m2): \t{7}\n"\
               "Production Volume (m3):{8}\n"\
               "Single gang(s): \t{9}\n"\
               "Double gang: \t\t{10}\n"\
               .format(self.panel_number,
               self.panel_model,
               self.width_design_mm,
               self.height_design_mm,
               self.m2_design,
               self.width_actual_mm,
               self.height_actual_mm,
               self.m2_actual,
               self.m3_actual,
               self.gang_single,
               self.gang_double
               )

    def production_volume_adjustment(self, width, height, depth):
        """
        This is a function that adjust the production volume by
        subtracting the volume of the L shapes that are cut out
        from productions.
        """
        self.m3_actual = self.m3_actual - ((width / 1000) * (height / 1000) * (depth / 1000))
        self.m2_actual = self.m2_actual - ((width / 1000) * (height / 1000))
        print("{0} m3 has been adjusted to {1} m3".format(self.panel_model, self.m3_actual))
        print("{0} m2 has been adjust to {1} m2".format(self.panel_model, self.m2_actual))
                                           
                                           
class Group():
    def __init__(self, group_name, drywalls):
        self.group_name = group_name
        self.drywalls = drywalls
        self.panel_num = len(drywalls)

class Room(Group):
    def __init__(self, room_number, left_right, group_name, drywalls):
        self.room_number = room_number
        self.left_right = left_right
        Group.__init__(self, group_name, drywalls)
    
    def m2_production(self):
        total_m2_production = 0
        for drywall in self.drywalls:
            total_m2_production += drywall.m2_actual
        return total_m2_production
    
    def m3_production(self):
        total_m3_production = 0
        for drywall in self.drywalls:
            total_m3_production += drywall.m3_actual
    
    def m2_design(self):
        total_m2_design = 0
        for drywall in self.drywalls:
            total_m2_design += drywall.m2_design
        return total_m2_design
    
    def drywall_details(self):
        for drywall in self.drywalls:
            print(drywall)
            
class Level():
    def __init__(self, level, rooms):
        self.level = level
        self.rooms = rooms
        
class Block():
    def __init__(self, block, levels):
        self.block = block
        self.levels = levels
    
# group C1, D1 individual drywalls

A1S1 = DryWall("A1(S1)", "600-*(HS)(S1)", 600, 2590, 85, 4)
A2S1 = DryWall("A2(S1)", "500+L(1G)(S1)", 500, 2590, 85, 4.5)
A3 = DryWall("A3", "900TP1", 900, 440, 85, 4)
B1 = DryWall("B1", "600-*(2G)", 600, 2590, 85, 6)
B2 = DryWall("B2", "700+-", 700, 2590, 85, 6)
B3 = DryWall("B3", "700+T(HS)(2G)", 700 ,2590, 85, 2)
B3.has_gang_double() 
C1 = DryWall("C1", "690-(4G)", 690, 2590, 85, 2)
C1.has_gang_double() 
C2 = DryWall("C2", "450+-", 450, 2590, 85, 6)
C3 = DryWall("C3", "500+(2G)", 500, 2590, 85, 4)
T1 = DryWall("T1", "(2535)730[]*L(2G)", 730, 2535, 85, 6)
T2 = DryWall("T2", "(385)910TP1", 910, 385, 85, 4)

#group C2, D2 type drywalls
A1S2 = DryWall("A1(S2)", "600-*(HS)(S2)", 600, 2590, 85, 4)
A2S2 = DryWall("A2(S2)", "500+L(1G)(S2)", 500, 2590, 85, 4.5)
