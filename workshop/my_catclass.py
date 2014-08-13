import pygame
import random

# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
yellow   = ( 255,   255, 0)
purple   = ( 255,   0, 255)

class Caterpillar:
    def __init__(self):
        self.face_xcoord = random.randrange(0,1000)
        self.face_ycoord = 250
        self.body = SegmentQueue()
        self.food = FoodList()
        if random.randrange(0,2):
            self.travel_direction = 'left'
        else:
            self.travel_direction = 'right'
           
    def grow(self):
        if self.travel_direction == 'right':
            if self.body.is_empty():
                x = self.face_xcoord - 35
            else:
                x = self.body.last.xcoord - 35
        else:
            if self.body.is_empty():
                x = self.face_xcoord + 40
            else:
                x = self.body.last.xcoord + 35
        y = self.face_ycoord
        self.body.add_segment(x, y)

    def shrink(self):
        self.body.head = self.body.head.next
        self.body.length -= 1
        if self.travel_direction == 'left':
            self.face_xcoord += 35
        else:
            self.face_xcoord -= 35

    def eat_food(self, food):
        if food.foodtype == 'nice':
            if self.body.length <= 10:
                self.grow()
        elif self.body.length >= 1:
            self.shrink()

    def reverse(self):
        if self.travel_direction == 'right':
            self.travel_direction = 'left'
            self.face_xcoord -= 35*self.body.length + 40
        else:
            self.travel_direction = 'right'
            self.face_xcoord += 35*self.body.length + 40
        
        self.body.reverse_queue()
    
    def move_forward(self):
        mod = -1 if self.travel_direction == 'left' else 1
        x = self.face_xcoord

        # collision checking
        # food
        previous_item = None
        current_item = self.food.head
        while current_item is not None:
            if self.travel_direction == 'left':
                if abs(current_item.xcoord - x) <= 5:
                    self.food.remove_item(previous_item)
                    self.eat_food(current_item)
            else:
                if abs(current_item.xcoord - (x + 40)) <= 5:
                    self.food.remove_item(previous_item)
                    self.eat_food(current_item)
            previous_item = current_item
            current_item = current_item.next

        # walls        
        if self.travel_direction == 'left' and x-2 < 0:
            self.reverse()
            return
        elif self.travel_direction == 'right' and x+42 > 1000:
            self.reverse()
            return

        self.face_xcoord += 2*mod

        current_segment = self.body.head
        while current_segment is not None:
            current_segment.xcoord += 2*mod
            current_segment = current_segment.next
                
    def drop_food(self):
        x = random.randrange(0, 1000)
        y = self.face_ycoord + 20
        foodtype = 'nasty' if random.randrange(0, 2) else 'nice'
        
        self.food.add_item(x, y, foodtype)
        
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
        # traverse the segment queue
        current_segment = self.body.head
        while current_segment is not None:
            current_segment.draw_segment(screen) 
            current_segment = current_segment.next 
           
    def draw_food(self, screen):
        # traverse the food queue
        current_item = self.food.head
        while current_item is not None:
            current_item.draw_fooditem(screen)
            current_item = current_item.next
    
class SegmentQueue:
    def __init__(self):
        self.length = 0
        self.head = None
        self.last = None
      
    def is_empty(self):
        return self.length == 0
      
    def add_segment(self, x, y):
        new_segment = BodySegment(x, y)
        if self.is_empty():
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

class BodySegment:
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
        
class FoodList:
    def __init__(self):
        self.length = 0
        self.head = None
        
    def add_item(self, x, y, kind): 
        next_item = self.head
        self.head = FoodItem(x, y, kind)
        self.head.next = next_item
        self.length += 1

    def remove_item(self, previous_item):
        # if the previously checked item was None,
        # the FoodItem is at the start of the list
        if previous_item == None:
            self.head = self.head.next
        else:
            previous_item.next = previous_item.next.next

        self.length -= 1
    
class FoodItem:
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

