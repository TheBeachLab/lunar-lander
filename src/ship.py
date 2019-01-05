#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright (C) 2018  Francisco Sanchez Arroyo
#

import random
from util.vectorsprites import *
from math import *
from soundManager import *


class Vehicle(VectorSprite):
    def __init__(self, position, heading, pointlist, stage):
        VectorSprite.__init__(self, position, heading, pointlist)
        self.stage = stage


class Ship(Vehicle):
    # Class attributes
    acceleration = 0.02
    decelaration = -0.005
    maxVelocity = 5
    turnAngle = 5
    reduce = 3

    def __init__(self, stage):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.thrustJet = ThrustJet(stage, self)
        self.FuelBox = FuelBox(stage, self)
        self.Rocket = Rocket(stage, self)
        self.rLeg = rLeg(stage, self)
        self.lLeg = lLeg(stage, self)
        self.shipDebrisList = []
        self.visible = True
        pointlist = [(6, -15), (15, -4.5), (15, 4.5), (6, 15),
                     (-6, 15), (-15, 4.5), (-15, -4.5), (-6, -15)]

        Vehicle.__init__(self, position, heading, pointlist, stage)

    def draw(self):
        if self.visible:
            VectorSprite.draw(self)
        return self.transformedPointlist

    def rotateLeft(self):
        self.angle += self.turnAngle
        self.thrustJet.angle += self.turnAngle
        self.FuelBox.angle += self.turnAngle
        self.Rocket.angle += self.turnAngle
        self.rLeg.angle += self.turnAngle
        self.lLeg.angle += self.turnAngle

    def rotateRight(self):
        self.angle -= self.turnAngle
        self.thrustJet.angle -= self.turnAngle
        self.FuelBox.angle -= self.turnAngle
        self.Rocket.angle -= self.turnAngle
        self.rLeg.angle -= self.turnAngle
        self.lLeg.angle -= self.turnAngle

    def increaseThrust(self):
        playSoundContinuous("thrust")
        if math.hypot(self.heading.x, self.heading.y) > self.maxVelocity:
            return

        dx = self.acceleration * math.sin(radians(self.angle)) * -1
        dy = self.acceleration * math.cos(radians(self.angle)) * -1
        self.changeVelocity(dx, dy)

    def decreaseThrust(self):
        stopSound("thrust")
        if (self.heading.x == 0 and self.heading.y == 0):
            return

        dx = self.heading.x * self.decelaration
        dy = self.heading.y * self.decelaration
        self.changeVelocity(dx, dy)

    def changeVelocity(self, dx, dy):
        self.heading.x += dx
        self.heading.y += dy
        self.thrustJet.heading.x += dx
        self.thrustJet.heading.y += dy
        self.FuelBox.heading.x += dx
        self.FuelBox.heading.y += dy
        self.Rocket.heading.x += dx
        self.Rocket.heading.y += dy
        self.rLeg.heading.x += dx
        self.rLeg.heading.y += dy
        self.lLeg.heading.x += dx
        self.lLeg.heading.y += dy

    def move(self):
        VectorSprite.move(self)
        self.decreaseThrust()

    # Break the shape of the ship down into several lines
    # Ship shape - [(0, -10), (6, 10), (3, 7), (-3, 7), (-6, 10)]
    def explode(self):
        pointlist = [(0, -10), (6, 10)]
        self.addShipDebris(pointlist)
        pointlist = [(6, 10), (3, 7)]
        self.addShipDebris(pointlist)
        pointlist = [(3, 7), (-3, 7)]
        self.addShipDebris(pointlist)
        pointlist = [(-3, 7), (-6, 10)]
        self.addShipDebris(pointlist)
        pointlist = [(-6, 10), (0, -10)]
        self.addShipDebris(pointlist)

    # Create a peice of ship debris

    def addShipDebris(self, pointlist):
        heading = Vector2d(0, 0)
        position = Vector2d(self.position.x, self.position.y)
        debris = VectorSprite(position, heading, pointlist, self.angle)

        # Add debris to the stage
        self.stage.addSprite(debris)

        # Calc a velocity moving away from the ship's center
        centerX = debris.boundingRect.centerx
        centerY = debris.boundingRect.centery

        # Alter the random values below to change the rate of expansion
        debris.heading.x = ((centerX - self.position.x) +
                            0.1) / random.uniform(20, 40)
        debris.heading.y = ((centerY - self.position.y) +
                            0.1) / random.uniform(20, 40)
        self.shipDebrisList.append(debris)


# Rocket
class Rocket(VectorSprite):
    pointlist = [(9, 18), (15, 30), (-15, 30), (-9, 18)]

    def __init__(self, stage, ship):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.ship = ship
        VectorSprite.__init__(self, position, heading, self.pointlist)

    def draw(self):
        self.color = (255, 255, 255)
        VectorSprite.draw(self)
        return self.transformedPointlist


# Right Leg
class rLeg(VectorSprite):
    pointlist = [(19.5, 33), (30, 33), (24, 33), (15, 18), (24, 33)]

    def __init__(self, stage, ship):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.ship = ship
        VectorSprite.__init__(self, position, heading, self.pointlist)

    def draw(self):
        self.color = (255, 255, 255)
        VectorSprite.draw(self)
        return self.transformedPointlist


# Left Leg
class lLeg(VectorSprite):
    pointlist = [(-19.5, 33), (-30, 33), (-24, 33), (-15, 18), (-24, 33)]

    def __init__(self, stage, ship):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.ship = ship
        VectorSprite.__init__(self, position, heading, self.pointlist)

    def draw(self):
        self.color = (255, 255, 255)
        VectorSprite.draw(self)
        return self.transformedPointlist


# Fuel Box
class FuelBox(VectorSprite):
    pointlist = [(15, 15), (15, 18), (-15, 18), (-15, 15)]

    def __init__(self, stage, ship):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.ship = ship
        VectorSprite.__init__(self, position, heading, self.pointlist)

    def draw(self):
        self.color = (255, 255, 255)
        VectorSprite.draw(self)
        return self.transformedPointlist


# Exhaust jet when ship is accelerating
class ThrustJet(VectorSprite):
    pointlist = [(15, 30), (0, 132), (-15, 30)]

    def __init__(self, stage, ship):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.accelerating = False
        self.ship = ship
        VectorSprite.__init__(self, position, heading, self.pointlist)

    def draw(self):
        if self.accelerating:
            self.color = (255, 255, 255)
        else:
            self.color = (10, 10, 10)

        VectorSprite.draw(self)
        return self.transformedPointlist
