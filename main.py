import pygame
import math

# Constantes

TYPE_SOL = "sol"
TYPE_BALLE = "balle"

NOIR = (0, 0, 0)

FENETRE_LARGEUR = 1000
FENETRE_HAUTEUR = 600

FENETRE_MARGE_EXTERNE = 200
FENETRE_MARGE_INTERNER = 50

BALLE_RAYON = 30
BALLE_COLLISION_MARGE = 45

SOL_HAUTEUR = 370
SOL_LARGEUR = 120
SOL_MARGE = 5

SOL_POSITION_MINIMALE = - SOL_HAUTEUR + SOL_MARGE * 20
SOL_POSITION_MAXIMALE = 0

VITESSE_HORIZONTALE = 0.08 # px/s
VITESSE_VERTICALE = 1.1 # px/s

ACCELERATION_GRAVITATIONNELLE = 0.002 # px/s/s
ACCELERATION_HORIZONTALE = 0.000008

# Fin Constantes

# Paramètres

dimensions_fenetre = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
images_par_seconde = 25

# Fin Paramètres

# Fonctions 
def repere_vers_pygame(position, taille):
    return (position[0], FENETRE_HAUTEUR - position[1] - taille[1])

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
    
def listEntite(scene):
    return scene["entites"]

def estVisible(entite):
    return entite["visible"]

def modifierTaille(entite, taille):
    entite["taille"] = taille
    
def modifierImage(entite, image):
    entite["image"] = image
    
def modifierVitesse(entite, vitesse):
    entite["vitesse"][0] = vitesse[0]
    entite["vitesse"][1] = vitesse[1]

def modifierPosition(entite, position):
    entite["position"][0] = position[0]
    entite["position"][1] = position[1]

def modifierAcceleration(entite, acceleration):
    entite["acceleration"][0] = acceleration[0]
    entite["acceleration"][1] = acceleration[1]
    
def modifierDernierTemps(entite, maintenant):
    entite["dernierTemps"] = maintenant

def typeEntite(entite):
    return entite.get("nom")

def positionEntite(entite):
    return entite.get("position")

def vitesseEntite(entite):
    return entite.get("vitesse")

def accelerationEntite(entite):
    return entite.get("acceleration")

def tailleEntite(entite):
    return entite.get("taille")

def dernierTempsEntite(entite):
    return entite.get("dernierTemps")

def imageEntite(entite):
    return entite.get("image")

def listPoses(entite):
    return entite["poses"]

def ajouterPose(entite, pose):
    entite["poses"].append(pose)

def nombrePoses(entite):
    return len(listPoses(entite))

def poseActuelle(entite):
    return entite["poseActuelle"]

def estAnime(entite):
    return entite["animer"]

def modifierAnimation(entite, etat):
    entite["animer"] = etat

def commencerAnimation(entite):
    modifierAnimation(entite, True)

def arreterAnimation(entite):
    modifierAnimation(entite, False)

def modifierPoseActuelle(entite, index=0):
    entite["poseActuelle"] = index

def progresserAnimation(entite):
    actuelle = poseActuelle(entite)
    nbr_poses = nombrePoses(entite)
    
    if nbr_poses > 0:
        actuelle += 1;
        if actuelle >= nbr_poses:
            actuelle = 0
        modifierPoseActuelle(entite, actuelle)
        modifierImage(entite, listPoses(entite)[actuelle])
            
    
def nouvelleEntite(nom, image):
    return {
        "nom": nom,
        "visible": False,
        "taille": (0,0),
        "position": [0, 0],
        "acceleration": [0, 0],
        "vitesse": [0, 0],
        "poses": [],
        "poseActuelle": -1,
        "animer": False, 
        "dernierTemps": 0,
        "image": image
    }

def nombreElementScene(scene):
    return len(listEntite(scene))

def derniereEntite(scene, types=[]):
    nbr = nombreElementScene(scene)
    
    if nbr > 0:
        entites = listEntite(scene)
        
        if len(types) == 0:
            return entites[nbr-1]
        
        i = nbr-1
        
        while i >= 0 and types.count(typeEntite(entites[i])) == 0:
            i -= 1 
            
        if i >= 0:
            return entites[i]
    return None

def premiereEntite(scene, types=[]):
    nbr = nombreElementScene(scene)
    if nbr> 0:
        entites = listEntite(scene)
        if len(types) == 0:
            return entites[0]
        
        i = 0
        
        while i<nbr and types.count(typeEntite(entites[i])) == 0:
            i += 1
        
        if i < nbr:
            return entites[i]
    return None        

def reveillerEntite(entite):
    entite["visible"] = True
    return entite

def endormirEntite(entite):
    entite["visible"] = False
    return entite

def entite_a_position(scene, x, types=[], myself=None):
    nbr = nombreElementScene(scene)
    result = list()
    
    if nbr > 0:
        entites = listEntite(scene)
        i = 0;

        while i < nbr and positionEntite(entites[i])[0] <= x:
            if positionEntite(entites[i])[0] <= x and positionEntite(entites[i])[0] + tailleEntite(entites[i])[0] >= x:
                if entites[i] is not myself:
                    if len(types) == 0:
                        result.append(entites[i])
                    else:
                        if types.count(typeEntite(entites[i])) != 0:
                            result.append(entites[i])
            i += 1
            
    return result
        

def creerSol(position):
    entite = nouvelleEntite("sol", IMAGE_SOL)
    
    modifierPosition(entite, position)
    modifierTaille(entite, (SOL_LARGEUR, SOL_HAUTEUR))
    modifierAcceleration(entite, (0,0))
    modifierVitesse(entite, (-VITESSE_HORIZONTALE, 0))
    modifierDernierTemps(entite, pygame.time.get_ticks())
    
    return entite

def generer_entite(position_precedente, taille_precedente):
    global IMAGE_SOL
    
    return creerSol((position_precedente[0] + taille_precedente[0] - SOL_MARGE, SOL_POSITION_MINIMALE))

def remplirScene(scene):
    nombre_elements = nombreElementScene(scene)
    
    if nombre_elements > 0:
        premier = premiereEntite(scene)
        while premier and positionEntite(premier)[0] < -FENETRE_MARGE_EXTERNE:
            listEntite(scene).remove(premier)
            nombre_elements -= 1
            premier = premiereEntite(scene)
        
    derniere_position = (0,0)
    derniere_taille = (0,0)
    dernier = None
    require = [TYPE_SOL]
    
    if nombre_elements > 0:
        dernier = derniereEntite(scene, require)
        if dernier:
            derniere_position = positionEntite(dernier)
            derniere_taille = tailleEntite(dernier)
    
    while derniere_position[0] + derniere_taille[0] < FENETRE_LARGEUR + FENETRE_MARGE_EXTERNE:
        entite = reveillerEntite(generer_entite(derniere_position, derniere_taille))
        ajouterEntite(scene, entite)
        
        dernier = derniereEntite(scene, require)
        derniere_position = positionEntite(dernier)
        derniere_taille = tailleEntite(dernier)
 
def mru_vitesse(vitesse, acceleration, dt):
    vx0, vy0 = vitesse
    ax, ay = acceleration
    
    return (vx0 + ax * dt, vy0 + ay * dt)
    
def mru_position(position, vitesse, acceleration, dt):
    x0, y0 = position
    vx0, vy0 = vitesse
    ax, ay = acceleration
    
    return (x0 + vx0 * dt + 0.5 * ax * dt ** 2, y0 + vy0 * dt  + 0.5 * ay * dt ** 2)

def miseAJourEntite(scene, maintenant):
    nbr = nombreElementScene(scene)
    dt = 0
    
    if nbr > 0:
        for entite in listEntite(scene):
            dt = maintenant - dernierTempsEntite(entite)
            if dt > 0:
                position = positionEntite(entite)
                vitesse = vitesseEntite(entite)
                acceleration = accelerationEntite(entite)
                
                vitesse = mru_vitesse(vitesse, acceleration, dt)
                position = mru_position(position, vitesse, acceleration, dt)
                
                modifierVitesse(entite, vitesse)
                modifierPosition(entite, position)
                
                if estAnime(entite):
                    progresserAnimation(entite)
                    
                modifierDernierTemps(entite, maintenant)    
            

def afficheEntite(scene):
    global fenetre
    entites = listEntite(scene)
    
    for entite in entites:
        if estVisible(entite):
            fenetre.blit(imageEntite(entite), repere_vers_pygame(positionEntite(entite), tailleEntite(entite)))

def creerImage(path, taille):
    global fenetre
    
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(fenetre), taille) 

def peutSauter(entite, marge_de_collision):
    global scene
    
    x = positionEntite(entite)[0]
    entites = entite_a_position(scene, x, [TYPE_SOL], entite)
    
    if len(entites) != 1:
        return False
    
    return estPoseSur(entite, entites[0], marge_de_collision)
    

def faireSauterBalle():
    global balle
    
    if peutSauter(balle, BALLE_COLLISION_MARGE):
        vx = vitesseEntite(balle)[0]
        ax = accelerationEntite(balle)[0]

        modifierVitesse(balle, (vx, VITESSE_VERTICALE))
        modifierAcceleration(balle, (ax,-ACCELERATION_GRAVITATIONNELLE))

def estPoseSur(entite1, entite2, marge):
    y1 = positionEntite(entite1)[1]
    y2 = positionEntite(entite2)[1] + tailleEntite(entite2)[1]
    
    if ( y1 < y2 and y1 + marge >= y2 ) or y1 == y2:
        return True
    return False

def collisionBalle():
    global balle
    
    xb = positionEntite(balle)[0]
    vy = vitesseEntite(balle)[1]
    entites = entite_a_position(scene, xb, [TYPE_SOL], balle)
    est_au_sol = False
    
    for entite in entites:
        
        if estPoseSur(balle, entite, BALLE_COLLISION_MARGE):
            if typeEntite(entite) == TYPE_SOL:
                est_au_sol = True
                if vy != 0:
                    modifierPosition(balle, (xb, positionEntite(entite)[1]+tailleEntite(entite)[1]))
                    modifierVitesse(balle, (0,0))
                    modifierAcceleration(balle, (0,0))
    
    if not est_au_sol:
        modifierAcceleration(balle, (0, -ACCELERATION_GRAVITATIONNELLE))

def createBalleImage(path):   
    return creerImage(path, (BALLE_RAYON*2, BALLE_RAYON*2))

def creerBalle():
    global IMAGE_BALLE
    
    balle = nouvelleEntite("balle", IMAGE_BALLE)
    
    modifierTaille(balle, (BALLE_RAYON*2, BALLE_RAYON*2))
    modifierPosition(balle, (100, SOL_POSITION_MINIMALE + SOL_HAUTEUR))
    modifierVitesse(balle, (0,0))
    modifierAcceleration(balle, (0,0))
    modifierDernierTemps(balle, pygame.time.get_ticks())
    
    ajouterPose(balle, IMAGE_BALLE)
    ajouterPose(balle, IMAGE_BALLE_30_DEG)
    ajouterPose(balle, IMAGE_BALLE_45_DEG)
    ajouterPose(balle, IMAGE_BALLE_60_DEG)
    ajouterPose(balle, IMAGE_BALLE_90_DEG)
    ajouterPose(balle, IMAGE_BALLE_120_DEG)
    ajouterPose(balle, IMAGE_BALLE_135_DEG)
    ajouterPose(balle, IMAGE_BALLE_150_DEG)
    ajouterPose(balle, IMAGE_BALLE_180_DEG)
    ajouterPose(balle, IMAGE_BALLE_210_DEG)
    ajouterPose(balle, IMAGE_BALLE_225_DEG)
    ajouterPose(balle, IMAGE_BALLE_240_DEG)
    ajouterPose(balle, IMAGE_BALLE_270_DEG)
    ajouterPose(balle, IMAGE_BALLE_300_DEG)
    ajouterPose(balle, IMAGE_BALLE_315_DEG)
    ajouterPose(balle, IMAGE_BALLE_330_DEG)
    
    return reveillerEntite(balle);
    
def afficherEcranDeJeu(maintenant):
    global scene, balle
    
    if enJeu:
        commencerAnimation(balle)
        miseAJourEntite(scene, maintenant)
        collisionBalle()
    
    remplirScene(scene)
    afficherScene(scene, IMAGE_SCENE)
    afficheEntite(scene)
    
def traite_entrees():
    global fini, enJeu
    
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if not enJeu:
                enJeu = True  
            else:
                if evenement.key == pygame.K_SPACE:
                    faireSauterBalle()

# Initialisation
pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption( "Bounce Tales" )

IMAGE_SOL = creerImage("images/ground.png", (SOL_LARGEUR, SOL_HAUTEUR))
IMAGE_SCENE = creerImage("images/trees-7191822_1280.png", (FENETRE_LARGEUR, FENETRE_HAUTEUR))
IMAGE_BALLE = createBalleImage("images/ball/ball.0.png")
IMAGE_BALLE_30_DEG = createBalleImage("images/ball/ball.30.png")
IMAGE_BALLE_45_DEG = createBalleImage("images/ball/ball.45.png")
IMAGE_BALLE_60_DEG = createBalleImage("images/ball/ball.60.png")
IMAGE_BALLE_90_DEG = createBalleImage("images/ball/ball.90.png")
IMAGE_BALLE_120_DEG = createBalleImage("images/ball/ball.120.png")
IMAGE_BALLE_135_DEG = createBalleImage("images/ball/ball.135.png")
IMAGE_BALLE_150_DEG = createBalleImage("images/ball/ball.150.png")
IMAGE_BALLE_180_DEG = createBalleImage("images/ball/ball.180.png")
IMAGE_BALLE_210_DEG = createBalleImage("images/ball/ball.210.png")
IMAGE_BALLE_225_DEG = createBalleImage("images/ball/ball.225.png")
IMAGE_BALLE_240_DEG = createBalleImage("images/ball/ball.240.png")
IMAGE_BALLE_270_DEG = createBalleImage("images/ball/ball.270.png")
IMAGE_BALLE_300_DEG = createBalleImage("images/ball/ball.300.png")
IMAGE_BALLE_315_DEG = createBalleImage("images/ball/ball.315.png")
IMAGE_BALLE_330_DEG = createBalleImage("images/ball/ball.330.png")

fini = False
enJeu = False
scene = nouvelleScene()
balle = creerBalle()
horloge = pygame.time.Clock()
temps_depart = pygame.time.get_ticks()

ajouterEntite(scene, balle)

while not fini:
    traite_entrees()
    
    fenetre.fill(NOIR)
    
    maintenant = pygame.time.get_ticks()
    
    afficherEcranDeJeu(maintenant)
    
    pygame.display.flip()
    horloge.tick(images_par_seconde)

pygame.display.quit()
pygame.quit()
exit()