#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Image


class Feladatok():

    def __init__(self):
        # tégla
        self.ev3 = EV3Brick()
        # motorok
        self.jm = Motor(Port.B)
        self.bm = Motor(Port.C)
        self.km = Motor(Port.A)
        # szenzorok
        self.cs = ColorSensor(Port.S3)
        self.ts = TouchSensor(Port.S1)
        self.gs = GyroSensor(Port.S2)
        self.us = UltrasonicSensor(Port.S4)
        #self.ir = InfraredSensor(Port.S4)

        # dupla motorkezelő
        self.robot = DriveBase(self.jm, self.bm, 55, 115)

        # stopper óra
        self.ido = StopWatch()

    def csipog(self):
        self.ev3.speaker.beep()
        
    """def vonalkovet(self):
        #felvátva hajtom a motorokat egyik gyorsabb másik lassabb ha letér csere
        while True:
            if self.cs.reflection() > 35:
                self.bm.run(200)
                self.jm.run(100)
            else:
                self.jm.run(200)
                self.bm.run(100)"""

    def scanner(self):
        #2. A robotképernyőn szeretném ha megjelenne a függőleges vonalak a mintának megfelelően.(scanner)
        # Fényviszonyok:
        # fekete vonal: 9
        # szürke asztal: 55
        # asztalról le: 0
        # félig asztalról le: 22
        self.robot.drive(100,0)
        self.ido.reset()
        hol = 0
        while self.ido.time() < 3000:
            if self.cs.reflection() < (55+9)/2:
                self.ev3.screen.draw_line(hol,0,hol, 127)
            hol += 1
            wait(3000/178)
        self.robot.stop(Stop.BREAK)
        wait(10000)

    def feladat1a(self):
        # nem lát feketét addig megy
        while self.cs.reflection() >(55+9)/2-26:
            self.robot.drive(100,0)
        self.robot.stop(Stop.BREAK)
        # addig megy amíg feketét lát
        while self.cs.reflection() <(55+9)/2-26:
            self.robot.drive(100,0)
        self.robot.stop(Stop.BREAK)
    
    def feladat2(self):
        vege = False
        fekete = False
        self.robot.drive(100,0)
        while not vege:
            if self.cs.reflection() < (55+9)/2-18:
                fekete = True
            if fekete and self.cs.reflection() > (55+9)/2-9:
                vege = True
        self.robot.stop(Stop.BRAKE)

    def hanyvonal(self, db, seb, hatar):
        for vonalakSzama in range(db):
            vege = False
            fekete = False
            self.robot.drive(seb,0)
            while not vege:
                if self.cs.reflection() < hatar:
                    fekete = True
                if fekete and self.cs.reflection() > hatar+9:
                    vege = True
            self.robot.stop(Stop.BRAKE)

    def feladatB(self):
        hatar = (55+9)/2-18
        self.hanyvonal(3, 100, hatar)

    def feladatC(self):
        hatar = (55+9)/2-18
        self.hanyvonal(3, -100, hatar)

    def feladatD(self):
        hosszok = []
        self.robot.drive(50,0)
        for vonalakSzama in range(3):
            vege = False
            fekete = False
            self.ido.reset()
            self.robot.drive(50,0)
            while not vege:
                if self.cs.reflection() < (55+9)/2-17 and not fekete:
                    fekete = True
                    self.ido.reset()
                if fekete and self.cs.reflection() > (55+9)/2-9:
                    vege = True
                    hossz = self.ido.time()
                    hosszok.append(hossz)
            self.robot.stop(Stop.BRAKE)
            print(hossz)
        print(hosszok)