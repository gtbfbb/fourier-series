import pygame
import pygame.gfxdraw
from pygame.locals import *
import vectorcalc
import math
import numpy



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen.fill((255, 255, 255))
        self.Prev_mouse_pos = self.prev_points = self.points = self.Mouse_pos = self.start_pos = (None, None)
        self.dt = 0
        self.sdt = 0
        self.funcx = []
        self.funcy = []
        self.finished = False
        self.distance = None
        self.coeff = []
        self.newd = []
        self.traceline = []

        

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.dt = self.clock.tick(60) / 1000.0

            self.Mouse_pressed = pygame.mouse.get_pressed(3)
            self.Mouse_pos = pygame.mouse.get_pos()

            self.start_drawing()
            self.draw()
            self.finish_drawing()

            if self.finished:
                self.update()
            
            pygame.display.flip()
            

            
        pygame.quit()



    def update(self):
        pvx, pvy = 400, 300
        cvx, cvy, cv = None, None, None
        speed = None
        self.screen.fill((255, 255, 255))

        
        drawing = []
        if (not self.funcx or len(self.funcx) < 2):
            return
        for i in range(len(self.funcx)):
            drawing.append((self.funcx[i], self.funcy[i]))
        # pygame.draw.lines(self.screen, (0, 0, 255), True, drawing)


        for i in range(len(self.coeff)):
            speed = math.ceil(i / 2)
            speed *= -1 if i % 2 == 0 else 1
            print(speed)
            rotate = math.e ** (2j * math.pi * speed * self.sdt)
            cvx = self.coeff[i][0] * rotate
            cvy = self.coeff[i][1] * rotate
            cv = cvx + cvy
            

            self.draw_line((round(pvx), round(pvy)), (round(cv.real+ pvx), round(cv.imag + pvy)), (255, 100, 0))
            pvx += cv.real
            pvy += cv.imag


        self.traceline.append((pvx, pvy))
        if len(self.traceline) > 1:
            pygame.draw.lines(self.screen, (0, 0, 0), False, self.traceline)
        if self.sdt > 1:
            self.traceline.clear()
            self.sdt = 0

            

        pygame.display.flip()
        self.sdt += self.dt / 10
        


    def start_drawing(self):
        if(pygame.mouse.get_just_pressed()[0]):
            self.finished = False
            self.traceline.clear()
            self.coeff.clear()
            self.funcx.clear()
            self.funcy.clear()
            self.newd.clear()

            self.screen.fill((255, 255, 255))
            self.prev_points = self.start_pos = self.Mouse_pos
            self.add_point(self.Mouse_pos)
            self.draw_circle(self.Mouse_pos, 3, (0, 0, 255))



    def draw(self):
        if (self.Mouse_pressed[0] == True):
            self.points = self.Mouse_pos
            if (self.prev_points == (None, None)):
                pass
    
            self.distance = self.get_distance(self.Mouse_pos, self.prev_points)
            if (self.distance > 10):
                self.add_point(self.Mouse_pos)
                self.draw_circle(self.Mouse_pos, 3, (0, 0, 255))
                self.distance = 0
                self.prev_points = self.points
    
            if (self.Prev_mouse_pos != (None, None)):
                self.draw_line(self.Prev_mouse_pos, self.Mouse_pos, (255, 0, 0))
            self.Prev_mouse_pos = self.Mouse_pos
        


    def finish_drawing(self):
        if (pygame.mouse.get_just_released()[0] == True):
            self.finished = True
            self.Prev_mouse_pos = (None, None)
            self.distance = self.get_distance(self.Mouse_pos, self.start_pos)
            self.draw_line(self.start_pos, self.Mouse_pos, (255, 0, 0))
            self.draw_circle(self.Mouse_pos, 3, (0, 0, 255))
            self.add_point(self.Mouse_pos)
            t = x = y = 0
    
            while (t < 1):
                if self.distance == 0:
                    break
                x = round(self.Mouse_pos[0] - (self.Mouse_pos[0] - self.start_pos[0]) * t)
                y = round(self.Mouse_pos[1] - (self.Mouse_pos[1] - self.start_pos[1]) * t)
                circles = (x, y)
                self.add_point(circles)
                self.draw_circle(circles, 3, (0, 0, 255))
                t += 10/self.distance
    
            self.distance = 0
            self.fdt = round(1 / len(self.funcx), 5)
            self.draw_vector(len(self.funcx) / 2, (400, 300))
            print(self.coeff)
            print(len(self.funcx))



    def draw_vector(self, number, origin):
        prev_vectorx = origin[0]
        prev_vectory = origin[1]
        current_vectorx = None
        current_vectory = None
        current_vector = None
        vector_num = 0
        radius = 0
        count = 0
        while vector_num <= number:
            current_vectorx = vectorcalc.summation(self.funcx, vector_num, self.fdt, 'x', prev_vectorx)
            current_vectory = vectorcalc.summation(self.funcy, vector_num, self.fdt, 'y', prev_vectory)
            current_vector = current_vectorx, current_vectory
            self.coeff.append(current_vector)
            prev_vectorx += current_vector[0]
            prev_vectory += current_vector[1]

            vector_num *= -1
            vector_num += 1 if not vector_num <  0 else 0

        
            

    def get_distance(self, ipos, fpos):
        dis = math.sqrt((abs(fpos[0] - ipos[0]) ** 2) + (abs(fpos[1] - ipos[1]) ** 2))
        return dis


    def draw_line (self, ipos, fpos, rgb):
        pygame.gfxdraw.line(self.screen, ipos[0], ipos[1], fpos[0], fpos[1], rgb)


    def draw_circle(self, pos, radius, rgb):
        pygame.gfxdraw.aacircle(self.screen, pos[0], pos[1], radius, rgb)


    def add_point(self, pos):
        self.funcx.append(pos[0])
        self.funcy.append(pos[1])


    def clear_points(self):
        if (self.button1.within()):
            print("cleared")
            self.funcx.clear()
            self.funcy.clear()


    def within(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.rect[0] or mouse_pos[0] > self.rect[0] + self.rect[2]:
            return
        if mouse_pos[1] < self.rect[1] or mouse_pos[1] > self.rect[1] + self.rect[3]:
            return

        if pygame.mouse.get_just_pressed()[0]:
            return True


game = Game()
game.run()

