#!/usr/bin/env python3
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
# Notes:
# random.randrange returns an int
# random.uniform returns a float
# p for pause
# j for toggle showing FPS
# o for frame advance whilst paused

import pygame
import sys
import os
import random
from pygame.locals import *
from util.vectorsprites import *
from ship import *
from stage import *
from soundManager import *


class Lander():

    explodingTtl = 180

    def __init__(self):
        self.stage = Stage('Atari Lunar Lander', (1024, 768))
        self.paused = False
        self.showingFPS = False
        self.gameState = "attract_mode"
        self.secondsCount = 1
        self.score = 0
        self.ship = None

    def initialiseGame(self):
        self.gameState = 'playing'
        self.createNewShip()
        self.score = 0
        self.secondsCount = 1

    def createNewShip(self):
        if self.ship:
            [self.stage.spriteList.remove(debris)
             for debris in self.ship.shipDebrisList]
        self.ship = Ship(self.stage)
        self.stage.addSprite(self.ship.thrustJet)
        self.stage.addSprite(self.ship.FuelBox)
        self.stage.addSprite(self.ship.Rocket)
        self.stage.addSprite(self.ship.lLeg)
        self.stage.addSprite(self.ship.rLeg)
        self.stage.addSprite(self.ship)

    def playGame(self):

        clock = pygame.time.Clock()

        frameCount = 0.0
        timePassed = 0.0
        self.fps = 0.0

        # Main loop
        while True:
            # calculate fps
            timePassed += clock.tick(60)
            frameCount += 1
            if frameCount % 10 == 0:  # every 10 frames
                # nearest integer
                self.fps = round((frameCount / (timePassed / 1000.0)))
                # reset counter
                timePassed = 0
                frameCount = 0
            # add 1 second
            self.secondsCount += 1

            # get events list (keys)
            self.input(pygame.event.get())

            # pause routine
            if self.paused:
                self.displayPaused()
                continue

            # screen routine
            self.stage.screen.fill((10, 10, 10))
            self.stage.moveSprites()
            self.stage.drawSprites()
            self.displayScore()
            if self.showingFPS:
                self.displayFps()

            # Process ship keys
            if self.gameState == 'playing':
                self.playing()
            elif self.gameState == 'exploding':
                self.exploding()
            else:
                self.displayText()

            # Double buffer draw
            pygame.display.flip()

    def playing(self):
        self.processKeys()  # ship keys
        # self.checkCollisions()

    # explode routine
    def exploding(self):
        self.explodingCount += 1
        if self.explodingCount > self.explodingTtl:
            self.gameState = 'playing'
            [self.stage.spriteList.remove(debris)
             for debris in self.ship.shipDebrisList]
            self.ship.shipDebrisList = []
            self.createNewShip()
    # text screen

    def displayText(self):
        font1 = pygame.font.Font('../res/Hyperspace.otf', 50)
        font2 = pygame.font.Font('../res/Hyperspace.otf', 20)
        font3 = pygame.font.Font('../res/Hyperspace.otf', 30)

        titleText = font1.render('Lunar Lander', True, (180, 180, 180))
        titleTextRect = titleText.get_rect(centerx=self.stage.width/2)
        titleTextRect.y = self.stage.height/2 - titleTextRect.height*2
        self.stage.screen.blit(titleText, titleTextRect)

        keysText = font2.render(
            '(C) 1979 Atari INC.', True, (255, 255, 255))
        keysTextRect = keysText.get_rect(centerx=self.stage.width/2)
        keysTextRect.y = self.stage.height - keysTextRect.height - 20
        self.stage.screen.blit(keysText, keysTextRect)

        instructionText = font3.render(
            'Push start to Play', True, (200, 200, 200))
        instructionTextRect = instructionText.get_rect(
            centerx=self.stage.width/2)
        instructionTextRect.y = self.stage.height/2 - instructionTextRect.height
        self.stage.screen.blit(instructionText, instructionTextRect)

    def displayScore(self):
        font1 = pygame.font.Font('../res/Hyperspace.otf', 30)
        scoreStr = str("%02d" % self.score)
        scoreText = font1.render(scoreStr, True, (200, 200, 200))
        scoreTextRect = scoreText.get_rect(centerx=100, centery=45)
        self.stage.screen.blit(scoreText, scoreTextRect)

    def displayPaused(self):
        if self.paused:
            font1 = pygame.font.Font('../res/Hyperspace.otf', 30)
            pausedText = font1.render("Paused", True, (255, 255, 255))
            textRect = pausedText.get_rect(
                centerx=self.stage.width/2, centery=self.stage.height/2)
            self.stage.screen.blit(pausedText, textRect)
            pygame.display.update()

    # Should move the ship controls into the ship class
    def input(self, events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                # ESC key QUIT
                if event.key == K_ESCAPE:
                    sys.exit(0)
                # J key Toggle FPS
                if event.key == K_j:
                    if self.showingFPS:  # (is True)
                        self.showingFPS = False
                    else:
                        self.showingFPS = True
                # F key toggle Full Screen
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()

                if self.gameState == 'attract_mode':
                    # Start a new game
                    if event.key == K_RETURN:
                        self.initialiseGame()
                elif self.gameState == 'playing':
                    # P key PAUSE
                    if event.key == K_p:
                        if self.paused:  # (is True)
                            self.paused = False
                        else:
                            self.paused = True
                    # K key suicide
                    if event.key == K_k:
                        self.killShip()
                    # Q quite
                    if event.key == K_q:
                        pygame.mixer.stop()
                        self.stage.removeSprite(self.ship)
                        self.stage.removeSprite(self.ship.thrustJet)
                        self.stage.removeSprite(self.ship.FuelBox)
                        self.stage.removeSprite(self.ship.Rocket)
                        self.stage.removeSprite(self.ship.lLeg)
                        self.stage.removeSprite(self.ship.rLeg)
                        self.gameState = 'attract_mode'

    def processKeys(self):
        key = pygame.key.get_pressed()

        if key[K_LEFT] or key[K_z]:
            self.ship.rotateLeft()
        elif key[K_RIGHT] or key[K_x]:
            self.ship.rotateRight()

        if key[K_UP] or key[K_n]:
            self.ship.increaseThrust()
            self.ship.thrustJet.accelerating = True
        else:
            self.ship.thrustJet.accelerating = False

    # Check for ship hitting the rocks etc.
    # def checkCollisions(self):

        # Ship hit something?
        #shipHit = False
        # if shipHit:
            # self.killShip()

            # comment in to pause on collision
            # self.paused = True

    def killShip(self):
        stopSound("thrust")
        playSound("explode")
        self.explodingCount = 0
        self.stage.removeSprite(self.ship)
        self.stage.removeSprite(self.ship.thrustJet)
        self.stage.removeSprite(self.ship.FuelBox)
        self.stage.removeSprite(self.ship.Rocket)
        self.stage.removeSprite(self.ship.lLeg)
        self.stage.removeSprite(self.ship.rLeg)
        self.gameState = 'exploding'
        self.ship.explode()

    def createDebris(self, sprite):
        for _ in range(0, 25):
            position = Vector2d(sprite.position.x, sprite.position.y)
            debris = Debris(position, self.stage)
            self.stage.addSprite(debris)

    def displayFps(self):
        font2 = pygame.font.Font('../res/Hyperspace.otf', 15)
        fpsStr = str(self.fps)+(' FPS')
        scoreText = font2.render(fpsStr, True, (255, 255, 255))
        scoreTextRect = scoreText.get_rect(
            centerx=(self.stage.width/2), centery=15)
        self.stage.screen.blit(scoreText, scoreTextRect)


# Script to run the game
if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

initSoundManager()
game = Lander()  # create object game from class LLander
game.playGame()

####
