import pygame

# Constantes

NOIR = (0, 0, 0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

SOL_HAUTEUR = 370
SOL_LARGEUR = 120

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

def nouvelleScene():
    return {
        "entites": []
    }

def preprareScene(scene, background):
    global fenetre
    
    fenetre.blit(background, (0,0))
    
def afficherScene(scene, background):
    preprareScene(scene, background)
    

def ajouterEntite(scene, entitee):
    scene["entites"].append(entitee)
    
def nouvelleEntite(nom, image):
    return {
        "nom": nom,
        "visible": False,
        "position": [0, 0],
        "vitesse": [0, 0],
        "acceleration": [0, 0],
        "image": image,
        "angleRotation": 0
    }

def reveillerEntite(scene, entite):
    entite["visible"] = True
    return entite

def supprimerEntite(scene, entite):
    entite["visible"] = False
    return entite

def miseAJourEntite(scene):
    pass

def afficheEntite(scene):
    global fenetre
    entites = scene["entites"]
    
    x = 0
    
    for entite in entites:
        fenetre.blit(entite["image"], (x, 400))
        x += SOL_LARGEUR

# Initialisation
pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption( "Bounce Tales" )

IMAGE_SOL = pygame.image.load("images/ground.png").convert_alpha(fenetre)
IMAGE_SOL = pygame.transform.scale(IMAGE_SOL, (SOL_LARGEUR, SOL_HAUTEUR))

IMAGE_SCENE = pygame.image.load("images/trees-7191822_1280.png").convert_alpha(fenetre)
IMAGE_SCENE = pygame.transform.scale(IMAGE_SCENE, (FENETRE_LARGEUR, FENETRE_HAUTEUR))

fini = False
enJeu = False
scene = nouvelleScene()
horloge = pygame.time.Clock()
temps_depart = pygame.time.get_ticks()

ajouterEntite(scene, nouvelleEntite("sol", IMAGE_SOL))
ajouterEntite(scene, nouvelleEntite("sol", IMAGE_SOL))
ajouterEntite(scene, nouvelleEntite("sol", IMAGE_SOL))
ajouterEntite(scene, nouvelleEntite("sol", IMAGE_SOL))
ajouterEntite(scene, nouvelleEntite("sol", IMAGE_SOL))
ajouterEntite(scene, nouvelleEntite("sol", IMAGE_SOL))
ajouterEntite(scene, nouvelleEntite("sol", IMAGE_SOL))

while not fini:
    traite_entrees()
    
    fenetre.fill(NOIR)
    
    afficherScene(scene, IMAGE_SCENE)
    miseAJourEntite(scene)
    afficheEntite(scene)
    
    pygame.display.flip()
    horloge.tick(images_par_seconde)

pygame.display.quit()
pygame.quit()
exit()