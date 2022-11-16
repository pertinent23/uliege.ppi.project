import pygame

# Constantes

NOIR = (0, 0, 0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

FENETRE_MARGE_EXTERNE = 200
FENETRE_MARGE_INTERNE = 50

SOL_HAUTEUR = 370
SOL_LARGEUR = 120

# Paramètres

dimensions_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
images_par_seconde = 25

# Fonctions

#### Definition Entitee ####

def nouvelleEntite(nom, image):
    return {
        "nom": nom,
        "visible": False,
        "taille": [0,0],
        "position": [0, 0],
        "vitesse": [0, 0],
        "acceleration": [0, 0],
        "dernierTemps": 0,
        "image": image,
        "angleRotation": 0
    }


def visible(entite):
    entite['visible'] = True

def invisible(entite):
    entite['visible'] = False

def estVisible(entite):
    return entite['visible']


def place(entite, x, y):
    entite['position'][0] = x
    entite['position'][1] = y

def set_vitesse(entite, x, y):
    entite['vitesse'][0] = x
    entite['vitesse'][1] = y

def set_acceleration(entite, x, y):
    entite['acceleration'][0] = x
    entite['acceleration'][1] = y

def position(entite):
    return entite['position']


def set_taille(entite, largeur, hauteur):
    entite["taille"][0] = largeur
    entite["taille"][1] = hauteur

def taille(entite):
    return entite["taille"]

def miseAJourEntite(scene):
    nbr = nombreElementScene(scene)
    
    if nbr > 0:
        pass


def afficheEntite(scene):
    global fenetre
    entites = scene["entites"]
    
    for entite in entites:
        fenetre.blit(entite["image"], repere_vers_pygame(entite["position"]))


#### Fin Entitee ####

#### Definition Scene ####
     
def nouvelleScene():
    return {
        "entites": []
    }
    

def ajouterEntite(scene, entite):
    scene["entites"].append(entite)
    

def nombreElementScene(scene):
    return len(scene["entites"])

def derniereEntite(scene):
    nbr = nombreElementScene(scene)
    
    if nbr > 0:
        return scene["entites"][-1]
    return None

def premiereEntite(scene):
    nbr = nombreElementScene(scene)

    if nbr(scene) > 0:
        return scene["entites"][0]
    return None

#### Fin Scene ####

#### Sol ####

def generer_sol(position):
    entite = nouvelleEntite("sol", IMAGE_SOL)
    place(entite, position, 100)
    set_taille(entite, SOL_LARGEUR, SOL_HAUTEUR)
    entite["dernierTemps"] = pygame.time.get_ticks()
    
    return entite


def get_sol(scene):
    entites = scene["entites"]
    sols = []

    for entite in entites:
        if entite["nom"] == "sol":
            sols.append(entite)

    return sols


def updateSol(scene):
    sols = get_sol(scene)
    
    if len(sols) > 0:
        while position(sols[0]) < -FENETRE_MARGE_EXTERNE:
            scene["entites"].remove(sols[0])
            sols.remove(0)

    derniere_position = (0,0)
    derniere_taille = (0,0)
 
    if len(sols) > 0:
        dernier = sols[-1]
        derniere_position = position(dernier) 
        derniere_taille = taille(dernier)

    while derniere_position[0] + derniere_taille[0] < FENETRE_LARGEUR + FENETRE_MARGE_EXTERNE:
        entite = generer_sol(derniere_position[0] + derniere_taille[0])
        visible(entite)
        ajouterEntite(scene, entite)

        derniere_position = position(entite)
        derniere_taille = taille(entite)

#### Fin Sol ####

def traite_entrees():
    global fini
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True


def afficherBack(fenetre, background):
    fenetre.blit(background, (0,0))
    

def afficherEcranDeJeu():
    global scene
    
    #miseAJourEntite(scene)
    updateSol(scene)
    afficherBack(fenetre, IMAGE_SCENE)
    afficheEntite(scene)
    

def repere_vers_pygame(position):
    return (position[0], FENETRE_HAUTEUR - position[1])


def load_image(fenetre, chemin, dimensions):
    IMAGE = pygame.image.load(chemin).convert_alpha(fenetre)
    return pygame.transform.scale(IMAGE, dimensions)

#### Fin Fonctions ####

# Initialisation
pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption( "Bounce Tales" )

IMAGE_SOL = load_image(fenetre, "images/ground.png", (SOL_LARGEUR, SOL_HAUTEUR))
IMAGE_SCENE = load_image(fenetre, "images/trees-7191822_1280.png", (FENETRE_LARGEUR, FENETRE_HAUTEUR))

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