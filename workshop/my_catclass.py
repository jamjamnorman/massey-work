import pygame
import random

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
yellow   = ( 255,   255, 0)
purple   = ( 255,   0, 255)

class caterpillar:
    def __init__(self):
        x = random.randrange(0,1000)
        self.face_xcoord = x
        self.face_ycoord = 250
        self.body = segment_queue()
        self.food = food_list()
        td = random.randrange(0,2)
        if td == 0:
            self.travel_direction = 'left'
        else:
            self.travel_direction = 'right'
           
    def grow(self):
        if self.travel_direction == 'right':
            if self.body.isEmpty():
                x = self.face_xcoord - 35
            else:
                x = self.body.last.xcoord - 35*mod
        else:
            if self.body.isEmpty():
                x = self.face_xcoord + 40
            else:
                x = self.body.last.xcoord - 35*mod
        y = self.face_ycoord
        self.body.addSegment(x, y)

    def reverse(self):
        if self.travel_direction == 'right':
            self.travel_direction = 'left'
            mod = -1
        else:
            self.travel_direction = 'right'
            mod = 1
        self.face_xcoord += (35*(self.body.length+1))*mod
        self.body.reverse_queue()
    
    def move_forward(self):
        mod = -1 if self.travel_direction == 'left' else 1
        self.face_xcoord += 2*mod
        current_node = self.body.head
        while current_node is not None:
            current_node.xcoord += 2*mod
            current_node = current_node.next 
                
    def drop_food(self):
        return
        
    def draw_caterpillar(self, screen):
        self.draw_face(screen)
        self.draw_body(screen)
        self.draw_food(screen)

    def draw_face(self, screen):
        x = self.face_xcoord 
        y = self.face_ycoord
        pygame.draw.ellipse(screen,red,[x, y, 40, 45])
        pygame.draw.ellipse(screen,black,[x+6, y+10, 10, 15])
        pygame.draw.ellipse(screen,black,[x+24, y+10, 10, 15])
        if self.travel_direction == 'right':
            pygame.draw.line(screen,black, (x+11, y), (x+9, y-10), 3)
            pygame.draw.line(screen,black, (x+20, y), (x+20, y-10), 3)
        else:
            pygame.draw.line(screen,black, (x+16, y), (x+16, y-10), 3)
            pygame.draw.line(screen,black, (x+25, y), (x+26, y-10), 3)

    def draw_body(self, screen):
        #traverse the segment queue
        current_node = self.body.head
        while current_node is not None:
            current_node.draw_segment(screen) 
            current_node = current_node.next 
           
    def draw_food(self, screen):
        #traverse the segment queue
        current_node = self.food.head
        a = None
        while current_node is not None:
            a = current_node
            if a.next is None:
                break
            current_node = current_node.next
            current_node.draw_fooditem(screen)
        self.last = a
        
             
    
class segment_queue:
    def __init__(self):
        self.length = 0
        self.head = None
        self.last = None
      
    def isEmpty(self):
        return self.length == 0
      
    def addSegment(self, x, y):
        new_segment = body_segment(x, y)
        if self.isEmpty():
            self.head = new_segment
        else:
            self.last.next = new_segment
        self.last = new_segment
        self.length += 1
    
    def reverse_queue(self):
        last_segment = None
        current_segment = self.head
        self.last = self.head

        while current_segment is not None:
            next_segment = current_segment.next
            current_segment.next = last_segment
            last_segment = current_segment
            current_segment = next_segment

        self.head = last_segment

class body_segment:
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y
        self.next = None
        
    def draw_segment(self, screen):
        x = self.xcoord
        y = self.ycoord
        pygame.draw.ellipse(screen,green,[x, y, 35, 40])
        pygame.draw.line(screen,black, (x+8, y+35), (x+8, y+45), 3)
        pygame.draw.line(screen,black, (x+24, y+35), (x+24, y+45), 3)
        
class food_list:
    def __init__(self):
        self.length = 0
        self.head = None
        
    def addItem(self, x, y, kind): 
        return
    
class food_item:
    def __init__(self, x, y, kind):
        self.xcoord = x
        self.ycoord = y
        self.foodtype = kind
        self.next = None   
        
    def draw_fooditem(self, screen):
        x = self.xcoord
        y = self.ycoord
        if self.foodtype == 'nice':
            pygame.draw.ellipse(screen,yellow,[x, y, 15, 15])
        else:
            pygame.draw.ellipse(screen,purple,[x, y, 15, 15])

