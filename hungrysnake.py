# coding: utf8

import random
import sys
import os
import platform

class Snake:
    def __init__(self, coordinates=[(6,5),(5,5),(4,5)],direction="right", hunger=0):
        self.direction = direction
        self.hunger = hunger
        self.coordinates = coordinates
        self.isfeeding = False
        
    def eat(self):
        #du spiser og nultiller sulten
        self.isfeeding = True
        self.hunger = 0
    
    def starve(self):
        #vi fjerner den sidste del a slangen og nulstiller sult
        del(self.coordinates[-1])
        self.hunger = 0
        
    def turn(self, new_direction):
        if new_direction == self.direction:
            return
        if new_direction == "up" and self.direction == "down":
            return
        if new_direction == "down" and self.direction == "up":
            return
        if new_direction == "left" and self.direction == "right":
            return
        if new_direction == "right" and self.direction == "left":
            return
        if new_direction not in ["up", "down", "left", "right"]:
            if new_direction:
                print("du kan skrive up, down, left ,right eller 'wasd' for at gå i forskellige retninger")
            return
        self.direction = new_direction

    def move(self):
        headx,heady = self.coordinates[0]
        if self.direction == "up":
            heady += 1
        elif self.direction == "down":
            heady -= 1
        elif self.direction == "left":
            headx -= 1
        elif self.direction == "right":
            headx += 1

         #hver gang du rykker så vokser sulten med 1
        self.hunger += 1
        #når den når 15 kalder vi starve
        if self.hunger == 20:
            self.starve()

        self.coordinates =[(headx,heady)] + self.coordinates
        # er vi ved at spise?
        if self.isfeeding:
            #self.isfeeding true, så vi er ved at spise
            #vi vokser ved ikke at fjerne den sidste del
            self.isfeeding = False
        else:
            #her ser vi ingen mad, så vi tager en fra så vi ikke hele tiden bliver større
            del(self.coordinates[-1])

class Level:
    def __init__(self, length=36, height=9, delay=0.5):
        self.length = length
        self.height = height
        self.delay = delay
    def place_food(self, blocked_coordinates=[]):
        foodx = random.randint(0,self.length - 1)
        foody = random.randint(0,self.height - 1)
        if (foodx, foody) in blocked_coordinates:
            foodx, foody = self.place_food(blocked_coordinates = blocked_coordinates)
        self.food_location = (foodx, foody)
        return self.food_location
    
class Engine:
    def __init__(self, display_type, level=None, snake=None,):
        if level: 
            self.level = level
        else:
            self.level = Level()
        if snake:    
            self.snake = snake
        else:
            self.snake = Snake()
        self.display_type = display_type
        self.turns = 0
        self.score = 0
        #vi placerer maden, men kun i de felter som er fri.       
        self.level.place_food(blocked_coordinates=self.snake.coordinates)
        self.update_screen()
    def run_game(self):
        while True:
            
            print(f"Position: {self.snake.coordinates}") 
            print(f"Food: {self.level.food_location}")
            print(f"Hunger: {self.snake.hunger}")
            print(f"turns: {self.turns}")
            print(f"score: {self.score}")
            
            direction = input("hvilken vej?")
            #her har vi gjordt at man i stedet for at skrive up down osv. at man nu kan skrive 'wasd'
            if direction == "w":
                direction = "up"
            elif direction == "s":
                direction = "down"
            elif direction == "a":
                direction = "left"
            elif direction == "d":
                direction = "right"

            if direction != "":
                #hvis noget blev intastet, kald turn funktion.
                self.snake.turn(new_direction = direction)
            self.snake.move()

            
            if len(self.snake.coordinates) == 0:
                #slangen findes ikke mere. GAME OVER
                print("du døde a sult, GAME OVER, MUHAAHAHAHAHAHHA")
                break
                
                #i de næste linier tjekker vi hvis slangen er kommet uden for banen.
            if self.snake.coordinates[0][0] < 0 or self.snake.coordinates[0][1] < 0:
                print("du ramte en væg til venstre eller i bunden, AV, GAME OVER,")
                break
            elif self.snake.coordinates[0][0] > self.level.length - 1 or self.snake.coordinates[0][1] > self.level.height - 1:
                print("du ramte en væg til højre eller i toppen, AV, GAME OVER,")
                break
                
            if self.snake.coordinates[0] in self.snake.coordinates[1:]:
                print("du ramte dig selv din klodshans! GAME OVER")
                break
                
            if self.level.food_location == self.snake.coordinates[0]:
                #slanges hovedet står oven i maden
                self.snake.eat()
                self.level.place_food(blocked_coordinates=self.snake.coordinates)
                print("nomnomnom")
            self.turns +=1
            self.score = self.turns * len(self.snake.coordinates)

            
            self.update_screen()
                

    def update_screen(self):
        #vi opretter en frame fyldt med blank, som tegner vores bane op
        self.frame=[]
        for x in range(self.level.length):
            self.frame.append(["blank"] * self.level.height)

        chars = {"blank" : ".", "body" : "o", "head" : "O", "food" : "*"}

        #her siger vi at x,y er slangens hoved
        x,y = self.snake.coordinates[0]
        #og her tegner vi hovedet med hjælp fra teksten over
        self.frame[x][y] = "head"

        #vi laver kroppen til slangen
        for x,y in self.snake.coordinates[1:]:
            #her tenger vi resten af kroppen på banen
            self.frame[x][y] = "body"

        x,y = self.level.food_location
        self.frame[x][y] = "food"

        if self.display_type == "pc":
            #skærmen tømmes
            if platform.system() == "Windows":
                # brug "cls" på Windows
                os.system("cls")
            else:
                # brug "clear" på ikke-Windows
                os.system("clear")
            #vi laver en ordbog så vi nemt kan tegne de forskellige tegn.

            #her tager vi alle y'erne i reverese så vi for det ordenligt sat op.
            for y in reversed(range (self.level.height)):
                #her tager vi x'erne uden reverse for den skal i den normale retning.
                for x in range(self.level.length):
                    #her printer vi alle punkterne i x linjen et af gangen
                    print(chars[self.frame[x][y]], end="")
                print()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        my_engine = Engine(display_type="pc")
    else:
        my_engine = Engine(display_type="badge")

    my_engine.run_game()
