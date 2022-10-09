import pygame as pg
from .utils import draw_text
import os

class Pannel:
    
    def __init__(self, width, height):
        
        self.width, self.height = width, height

        self.ressource_pannel_color = (204, 174, 132)
        self.building_pannel_color = (230, 162, 64)

        # Ressource pannel in the top of screen
        self.ressource_pannel = pg.Surface((self.width, self.height * 0.04))
        self.ressource_pannel.fill(self.ressource_pannel_color)

        # Building pannel in the right screen
        self.building_pannel = pg.Surface((self.width * 0.2, self.height * 0.96))
        self.building_pannel.fill(self.building_pannel_color)

        # Available building in building pannel
        self.buildings = self.load_images()
        self.tiles = self.create_building_pannel()

        # Selected building (defaultly, nothing is selected)
        self.selected_tile = None



    def create_building_pannel(self):

        render_pos = [self.width * 0.8 + 10, self.height * 0.04 + 500]
        object_width = self.building_pannel.get_width() // 3
        tiles = []

        for building_name, building_image in self.buildings.items():

            pos = render_pos.copy()
            building_image_tmp = building_image.copy()
            building_image_scale = self.scale_image(building_image_tmp, width=object_width)
            rect = building_image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": building_name,
                    "icon": building_image_scale,
                    "image": self.buildings[building_name],
                    "rect": rect
                }
            )


            if render_pos[0] + building_image_scale.get_width() + 10 >= self.width:
                
                render_pos = [self.width * 0.8 + 10, self.height * 0.04 + 500]
                render_pos[1] += building_image_scale.get_height() + 10
            
            else:
                render_pos[0] += building_image_scale.get_width() + 10 # update x for next item


        return tiles



    def draw(self, screen):

        if self.selected_tile != None:
            screen.blit(self.selected_tile['image'], pg.mouse.get_pos())
        
        screen.blit(self.ressource_pannel, (0, 0))

        screen.blit(self.building_pannel, (self.width * 0.8, self.height * 0.04))

        for tile in self.tiles:
            screen.blit(tile["icon"], tile["rect"])

        resource_pannel_text  = ['File', 'Options', 'Help', 'Advisor', 'Dn', 'Population']
        
        resource_pannel_text_pos = [20, 20]

        for text in resource_pannel_text:
            
            temp_pos = resource_pannel_text_pos.copy()

            draw_text(text, 42, screen, temp_pos)
            
            resource_pannel_text_pos[0] += 200

    
    def update(self):

        mouse_pos = pg.mouse.get_pos()

        mouse_action = pg.mouse.get_pressed()

        # if left is clicked => select graphical image
        for tile in self.tiles:
            if tile["rect"].collidepoint(mouse_pos):
                if mouse_action[0]:
                    self.selected_tile = tile
        # if right is clicked => unselect item
        if mouse_action[2]:
            self.selected_tile = None



    def load_images(self):
        
        path = 'assets/graphics'

        return {

            'tree': pg.image.load(os.path.join(path, 'Land1a_00041.png')).convert_alpha(),
            'rock': pg.image.load(os.path.join(path, 'Land1a_00290.png')).convert_alpha()

        }

    
    def scale_image(self, image, width=None, height=None): # Procedure function which scales up or down the image specified
                
        # Default case do nothing
        if (width == None) and (height == None):
            pass

        elif height == None: # scale only width
            scale = width / image.get_width()
            height = scale * image.get_height()
            image = pg.transform.scale(image, ( int(width), int(height) ))

        elif width == None: # scale only width
            scale = height / image.get_height()
            width = scale * image.get_width()
            image = pg.transform.scale(image, (int(width), int(height)))

        else:
            image = pg.transform.scale(image, (int(width), int(height)))

        return image