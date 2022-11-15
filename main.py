import pygame

# Constantes

NOIR = (0, 0, 0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

FENETRE_MARGE_EXTERNE = 200
FENETRE_MARGE_INTERNER = 50

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
            
def repere_vers_pygame(position):
    return (position[0], FENETRE_HAUTEUR - position[1])

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
        "taille": (0,0),
        "position": [0, 0],
        "vitesse": [0, 0],
        "acceleration": [0, 0],
        "dernierTemps": 0,
        "image": image,
        "angleRotation": 0
    }

def nombreElementScene(scene):
    return len(scene["entites"])

def derniereEntite(scene):
    nbr = nombreElementScene(scene)
    
    if nbr > 0:
        return scene["entites"][nbr-1]
    return None

def premiereEntite(scene):
    if nombreElementScene(scene) > 0:
        return scene["entites"][0]
    return None        

def reveillerEntite(entite):
    entite["visible"] = True
    return entite

def endormirEntite(entite):
    entite["visible"] = False
    return entite

def generer_entite(position_precedente, taille_precedente):
    global IMAGE_SOL
    
    entite = nouvelleEntite("sol", IMAGE_SOL)
    entite["position"][0] = position_precedente[0] + taille_precedente[0]
    entite["position"][1] = 100
    entite["taille"] = (SOL_LARGEUR, SOL_HAUTEUR)
    entite["dernierTemps"] = pygame.time.get_ticks()
    
    return entite

def remplirScene(scene):
    nombre_elements = nombreElementScene(scene)
    
    if nombre_elements > 0:
        while premiereEntite(scene).get("position")[0] < -FENETRE_MARGE_EXTERNE:
            scene["entites"].remove(0)
            nombre_elements -= 1
        
    derniere_position = (0,0)
    derniere_taille = (0,0)
    
    if nombre_elements > 0:
        dernier = derniereEntite(scene)
        derniere_position = dernier.get("position") 
        derniere_taille = dernier.get("taille")
    
    while derniere_position[0] + derniere_taille[0] < FENETRE_LARGEUR + FENETRE_MARGE_EXTERNE:
        entite = reveillerEntite(generer_entite(derniere_position, derniere_taille))
        ajouterEntite(scene, entite)
        
        derniere_position = entite.get("position")
        derniere_taille = entite.get("taille")

def miseAJourEntite(scene):
    nbr = nombreElementScene(scene)
    
    if nbr > 0:
        pass

def afficheEntite(scene):
    global fenetre
    entites = scene["entites"]
    
    for entite in entites:
        fenetre.blit(entite["image"], repere_vers_pygame(entite["position"]))
    
def afficherEcranDeJeu():
    global scene
    
    #miseAJourEntite(scene)
    remplirScene(scene)
    afficherScene(scene, IMAGE_SCENE)
    afficheEntite(scene)
    

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

while not fini:
    traite_entrees()
    
    fenetre.fill(NOIR)
    
    afficherEcranDeJeu()
    
    pygame.display.flip()
    horloge.tick(images_par_seconde)

pygame.display.quit()
pygame.quit()
exit()