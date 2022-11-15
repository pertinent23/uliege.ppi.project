import pygame

# Constantes

NOIR = (0, 0, 0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

# Fin Constantes

# Paramètres

dimensions_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
images_par_seconde = 25

# Fin Paramètres

# Fonctions

def traite_entrees():
    global fini
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True

# Initialisation
pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption( "Bounce Tales" )

fini = False
enJeu = False
horloge = pygame.time.Clock()
temps_depart = pygame.time.get_ticks()

while not fini:
    traite_entrees()
    
    fenetre.fill(NOIR)
    
    pygame.display.flip()
    
    horloge.tick(images_par_seconde)

pygame.display.quit()
pygame.quit()
exit()