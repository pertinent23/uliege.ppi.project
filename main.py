import pygame

# Constantes

NOIR = (0, 0, 0)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

FENETRE_MARGE_EXTERNE = 200
FENETRE_MARGE_INTERNE = 50

SOL_Y = 500

SOL_HAUTEUR = 370
SOL_LARGEUR = 120

BALE_LARGEUR = 60
BALE_HAUTEUR = 60

# Paramètres

dimensions_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
images_par_seconde = 25

# Fonctions

#### Definition Entitee ####

def nouvelleEntite(nom):
    return {
        "nom": nom,
        "visible": False,
        "taille": [0,0],
        "position": [0, 0],
        "vitesse": [0, 0],
        "acceleration": [0, 0],
        'momentDeplacement': 0,
        'imageAffichee':None,
        'poses': {},
        'animationActuelle':None,
        'animations':{} 
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


def ajoutePose(entite, nom, image):
    entite['poses'][nom] = image

def prendsPose(entite, pose):
    entite['imageAffichee'] = entite['poses'][pose]
    visible(entite)

def dessine(entite, ecran):
    ecran.blit(entite['imageAffichee'], entite['position'])


def deplace(entite, maintenant):
    dt = (maintenant - entite['momentDeplacement']) / 1000
    # mise à jour vitesse
    entite['vitesse'][0] += entite['acceleration'][0] * dt
    entite['vitesse'][1] += entite['acceleration'][1] * dt
    # mise à jour position
    entite['position'][0] += entite['vitesse'][0] * dt
    entite['position'][1] += entite['vitesse'][1] * dt
    # mise à jour moment de déplacement
    entite['momentDeplacement'] = maintenant

def commenceAnimation(entite, nomAnimation, fois = 1):
    entite['animationActuelle'] = entite['animations'][nomAnimation]
    if fois == 0:
        enBoucle(entite['animationActuelle'])
    else:
        repete(entite['animationActuelle'], fois - 1)
    visible(entite)


def arreteAnimation(entite):
    arrete(entite['animationActuelle'])
    entite['animationActuelle'] = None


def ajouteAnimation(entite, nom, animation):
    entite['animations'][nom] = animation


def estEnAnimation(entite):
    return entite['animationActuelle'] != None


#### Fin Entitee ####

#### Definition Scene ####
     
def nouvelleScene():
    return {
        "entites": []
    }
    

def ajouterEntite(scene, entite):
    scene["entites"].append(entite)
    
def acteurs(scene):
    return scene["entites"]

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
    entite = nouvelleEntite("sol")
    ajoutePose(entite, 'Sol', IMAGE_SOL)
    prendsPose(entite, 'Sol')
    place(entite, position, SOL_Y)
    set_taille(entite, SOL_LARGEUR, SOL_HAUTEUR)
    
    
    return entite


def get_sol(scene):
    entites = acteurs(scene)
    sols = []

    for entite in entites:
        if entite["nom"] == "sol":
            sols.append(entite)

    return sols


def updateSol(scene):
    sols = get_sol(scene)
    
    if len(sols) > 0:
        while position(sols[0])[0] < -FENETRE_MARGE_EXTERNE:
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

##### Définition MOUVEMENT #####

def mouvement(nom, duree):
    return (nom, duree) # durée en msec


def nomMouvement(mvt):
    return mvt[0]


def dureeMouvement(mvt):
    return mvt[1]

##### Fin MOUVEMENT #####

##### Définition ANIMATION #####

def nouvelleAnimation():
    return {
        'boucle':False,
        'repetition': 0,
        'momentMouvementSuivant':None,
        'indexMouvement':None,
        'choregraphie':[] # liste de mouvements
    }


def repete(animation, fois):
    animation['repetition'] = fois
    animation['boucle'] = False


def enBoucle(animation):
    animation['boucle'] = True


def ajouteMouvement(animation, mvt):
    animation['choregraphie'].append(mvt)


def mouvementActuel(animation):
    if animation['indexMouvement'] == None:
        return None
    else:
        return nomMouvement(animation['choregraphie'][animation['indexMouvement']])


def commenceMouvement(animation, index):
    animation['indexMouvement'] = index
    animation['momentMouvementSuivant'] = pygame.time.get_ticks() + dureeMouvement(animation['choregraphie'][index])


def commence(animation):
    commenceMouvement(animation, 0)


def arrete(animation):
    animation['indexMouvement'] = None


def anime(animation):
    if animation['indexMouvement'] == None:
        commence(animation)
    elif animation['momentMouvementSuivant'] <= pygame.time.get_ticks():
      if animation['indexMouvement'] == len(animation['choregraphie']) - 1:
        if animation['boucle']:
            commence(animation)
        else:
            if animation['repetition'] > 0:
                animation['repetition'] -= 1
                commence(animation)
            else:
                arrete(animation)
      else:
        commenceMouvement(animation, animation['indexMouvement'] + 1)

##### Fin ANIMATION #####

def traite_entrees():
    global fini
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_UP:
                saute(balle)


def miseAJour(scene):
    maintenant = pygame.time.get_ticks()
    updateSol(scene)
    for objet in acteurs(scene):
        deplace(objet, maintenant)


def creation_balle():
    balle = nouvelleEntite("balle")
    set_acceleration(balle,0,1000)
    place(balle,100,300)

    for nom_image, nom_fichier in (('BALE_1','ball.png'),
                               ('BALE_2','ball_30.png'),
                               ('BALE_3','ball_60.png'),
                               ('BALE_4','ball_90.png')):
        chemin = 'images/' + nom_fichier
        image = load_image(fenetre, chemin, (BALE_LARGEUR, BALE_HAUTEUR))
        ajoutePose(balle, nom_image, image)
    
    animation = nouvelleAnimation()
    ajouteMouvement(animation, mouvement('BALE_1', 80))
    ajouteMouvement(animation, mouvement('BALE_2', 80))
    ajouteMouvement(animation, mouvement('BALE_3', 80))
    ajouteMouvement(animation, mouvement('BALE_4', 80))

    ajouteAnimation(balle, 'roule', animation)

    return balle

def saute(objet):
    set_vitesse(objet, 0, -500)


def afficherBack(fenetre, background):
    fenetre.blit(background, (0,0))
    
def affiche(scene, ecran):
    entites = acteurs(scene)
    afficherBack(ecran, IMAGE_BACK)
    for objet in entites:
        if estVisible(objet):
            if estEnAnimation(objet):
                animationActuelle = objet['animationActuelle']
                poseActuelle = mouvementActuel(animationActuelle)
                anime(animationActuelle)
                nouvellePose = mouvementActuel(animationActuelle)
                if nouvellePose == None:
                    objet['animationActuelle'] = None
                    prendsPose(objet, poseActuelle)
                else:
                    prendsPose(objet, nouvellePose)

            dessine(objet, ecran)
    

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
IMAGE_BACK = load_image(fenetre, "images/trees-7191822_1280.png", (FENETRE_LARGEUR, FENETRE_HAUTEUR))

fini = False
enJeu = False
horloge = pygame.time.Clock()

scene = nouvelleScene()

balle = creation_balle()
ajouterEntite(scene, balle)

commenceAnimation(balle, 'roule', 0)

while not fini:
    traite_entrees()
    
    miseAJour(scene)

    fenetre.fill(NOIR)

    affiche(scene, fenetre)
    

    pygame.display.flip()
    horloge.tick(images_par_seconde)

pygame.display.quit()
pygame.quit()
exit()