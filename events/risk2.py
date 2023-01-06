import random as rd
import pygame as pg
from buildable import house, building
from game.game import Game
import time

class risk():
    def __init__(self, fire_risk, dest_risk,is_on_fire, is_destroyed):
        house.__init__(dest_risk, fire_risk)
        building.__init__(is_destroyed, is_on_fire)

        def riskprogress():
            clock = pg.time.Clock()
            t0 = pg.time.get_ticks()
            fire_risk_status = 0
            dest_risk_status = 0

            while is_on_fire == False:     #risk increases as soon as the building is created
                    seconds = (pg.time.get_ticks() - t0) / 1000  #timer using ticks
                    if seconds == 3:                            #risk has odds to increase every 3 seconds
                        if rd.randint(0, 100) < fire_risk:      #every type of building has different odds
                            fire_risk_status += 10
                        elif fire_risk_status == 100:           #if the fire risk has a value that exceeds 100, the building is on fire
                            is_on_fire = True
                            fire_risk_status = 0                #resetting the status of the building
                        t0 = pg.time.get_ticks()
                        seconds = (pg.time.get_ticks() - t0) / 1000 #resetting the timer




            while is_destroyed == False:  # risk increases as soon as the building is created
                seconds1 = (pg.time.get_ticks() - t1) / 1000  # timer using ticks
                if seconds1 == 3:  # risk has odds to increase every 3 seconds
                    if rd.randint(0, 100) < dest_risk:  # every type of building has different odds
                        dest_risk_status += 10
                    elif dest_risk_status == 100:  # if the fire risk has a value that exceeds 100, the building is on fire
                        is_destroyed = True
                        dest_risk_status = 0  # resetting the status of the building
                    t1 = pg.time.get_ticks()
                    seconds1 = (pg.time.get_ticks() - t1) / 1000  # resetting the timer
















