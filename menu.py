# coding:utf-8
import pygame
# import math
pygame.init()

# créer la fenetre du jeu

#icone = pygame.image.load('Sierra.ico')
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)  # Taille de la fenetre
pygame.display.set_caption("Caesar III")   # Nom de la fenetre

x = screen.get_size()
background = pygame.image.load('assets/menu_sprites/Background_Init.png')
background = pygame.transform.scale(background, x)


logo = pygame.image.load('assets/menu_sprites/Caesar3.png')
logo = pygame.transform.scale(logo, (440, 130))


start_new_career = pygame.image.load('assets/menu_sprites/start new career.png')
start_new_career_rect = start_new_career.get_rect()
start_new_career_rect.x = 625
start_new_career_rect.y = 350
load_saved_game = pygame.image.load('assets/menu_sprites/load saved game.png')
options = pygame.image.load('assets/menu_sprites/options.png')
exit_button = pygame.image.load('assets/menu_sprites/exit.png')
exit_rect = exit_button.get_rect()
exit_rect.x = 625
exit_rect.y = 500

def affichage_menu():
    screen.blit(logo, (560, 200))
    screen.blit(start_new_career, (625, 350))
    screen.blit(load_saved_game, (625, 400))
    screen.blit(options, (625, 450))
    screen.blit(exit_button, (625, 500))
    pygame.display.flip()

def survole(bouton, pos):
    if bouton.x < pos[0] < bouton.x + bouton.width:
        if bouton.y < pos[1] < bouton.y + bouton.height:
            return True
    return False



interface_menu = False
game = False
launched = True

while launched:  # boucle tant que cette condition est vraie
    screen.blit(background, (0, 0))
    
    # si le joueur ferme cette fenetre
    if interface_menu:
        affichage_menu()

    for event in pygame.event.get():

        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            launched = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                launched = False
                pygame.quit()
        if event.type == pygame.MOUSEMOTION:
            #boutons_dynamiques(start_new_career, exit_button)
            if survole(start_new_career_rect, pos):
                start_new_career = pygame.image.load('assets/menu_sprites/start new career mouse on.png')
            elif not survole(start_new_career_rect, pos):
                start_new_career = pygame.image.load('assets/menu_sprites/start new career.png')
            if survole(exit_rect, pos):
                exit_button = pygame.image.load('assets/menu_sprites/exit mouse on.png')
            elif not survole(exit_rect, pos):
                exit_button = pygame.image.load('assets/menu_sprites/exit.png')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not interface_menu:
                background = pygame.image.load('assets/menu_sprites/Background_Menu.png')
                background = pygame.transform.scale(background, x)
                interface_menu = True
            elif interface_menu:
                if exit_rect.collidepoint(event.pos):
                    launched = False
                    pygame.quit()
                if start_new_career_rect.collidepoint(event.pos):
                    interface_menu = False
                    background = pygame.image.load('assets/menu_sprites/Start.png')
                    background = pygame.transform.scale(background, x)

    pygame.display.flip()



