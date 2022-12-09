import pygame
import random
import math

# Constantes

TITRE = "BALL RUNNER"

# Représente le type d'entités que nous allons utilisé

TYPE_SOL = "sol"
TYPE_BALLE = "balle"
TYPE_EAU = "eau"
TYPE_VIE = "vie"
TYPE_PIECE = "piece"
TYPE_BRICK = "brick"
TYPE_BROKEN_BRICK = "broken-brick"

# La déclaration des couleurs utilisées dans notre code

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
JAUNE = (255, 200, 0)

# Les autres constantes utiles dans notre code

FENETRE_LARGEUR = 800 #en px
FENETRE_HAUTEUR = 550 #en px

FENETRE_MARGE_EXTERNE = 200 #en px
FENETRE_MARGE_INTERNE = 175 #en px

BALLE_RAYON = 30 #en px
BALLE_POSITION = FENETRE_LARGEUR // 3 #en px
BALLE_TOUCHE_MARGE = 2 #en px

PIECE_LARGEUR = 60 #en px
PIECE_HAUTEUR = 60 #en px
PIECE_MARGE = 10 #en px
PIECE_DELAI = 300 # en px

SOL_HAUTEUR = 370 #en px
SOL_LARGEUR = 120 #en px
SOL_MARGE_HORIZONTALE = 10 #en px
SOL_MARGE_VERTICALE = 40 #en px

SOL_POSITION_MINIMALE = - SOL_HAUTEUR + SOL_MARGE_VERTICALE * 2 #en px
SOL_POSITION_MAXIMALE = 0 #en px

EAU_HAUTEUR = 368
EAU_LARGEUR = 120
EAU_POSITION_MINIMALE = - EAU_HAUTEUR + SOL_MARGE_VERTICALE * 2 #en px
EAU_POSITION_MAXIMALE = 0 #en px
EAU_INTERVAL = 37000 #en ms

OCEAN_LONGUEUR_MINIMALE = 1500 #en px
OCEAN_LONGUEUR_MAXIMALE = 5000 #en px
OCEAN_INTERVAL = 25000 #en ms

BRICK_HAUTEUR = 50 #en px
BRICK_LARGEUR = 120 #en px
BRICK_MARGE = 50 #en px

VITESSE_HORIZONTALE = 0.2 # px/s
VITESSE_VERTICALE = 0.6 # px/s

ACCELERATION_GRAVITATIONNELLE = 0.002 # px/s/s
ACCELERATION_HORIZONTALE = 0.0008 #px/s/s

TEMPS_DE_TOUCHE_MAXIMALE = 300 #en ms

IMAGES_PAR_SECONDE = 40 #en px

SAUTE_DELAI = 300 #en ms

JUNGLE_INTERVAL = 57000 #en ms
JUNGLE_LONGUEUR_MINIMALE = 1500 #en px
JUNGLE_LONGUEUR_MAXIMALE = 5000 #en px

TABLEAU_DE_BORD_LARGEUR = 100 #en px
TABLEAU_DE_BORD_HAUTEUR = 25 #en px
TABLEAU_DE_BORD_MARGE = 3 #en px
TABLEAU_DE_BORD_X = 100 #en px 
TABLEAU_DE_BORD_Y = 13 #en px
TABLEAU_DE_BORD_TAILLE_POLICE = 20

IMAGE_TABLEAU_DE_BORD_LARGEUR = 30 #en px
IMAGE_TABLEAU_DE_BORD_HAUTEUR = 30 #en px

ECRAN_DE_JEUX_POLICE_TAILLE = 80

ECRAN_SELECTION_NIVEAU_POLICE_TAILLE = 30

FADE_SCREEN_TAILLE_POLICE = 15

NOMBRE_DE_VIE_MAXIMUM = 3
VIE_INTERVALLE = 30000 #en ms

WALL_DIMENSIONS = 90
NIVEAU_WALL_DIMENSIONS = 50
WALL_MARGE = 15


SCORE_FILE_PATH = "./file/score.txt"

# Utilisé pour la gestion des écrans

ECRAN_ACCUEIL = 1
ECRAN_SELECTION_NIVEAU = 2
ECRAN_DE_JEUX = 3

# Utilisé pour la gestion des niveaux

NIVEAU_FACILE = 3.1
NIVEAU_NORMAL = 3.2
NIVEAU_DIFFICILE = 3.3

# Utilisé pour la gestion de la vitesse

SCORE_V_MAX = 100000
FACTEUR_V_FACILE = 1
FACTEUR_V_NORMAL = 1.4
FACTEUR_V_DIFFICILE = 1.7
FACTEUR_V_MAX = 1.8

# Fin Constantes

# Ici nous transformons une entité en Objet
# Rect utilisable part pygame
def rectangle(entite):
    x, y = positionEntite(entite)
    return imageEntite(entite).get_rect().move(x, y)

# Nous utilisons dans notre code un repère orthonormé
# Donc nous avons besoin de cette fonction pour ramener nos dimensions
# Vers le repère de pygame
def repere_vers_pygame(position, taille):
    return (position[0], FENETRE_HAUTEUR - position[1] - taille[1])

# Gestion des scènes
def nouvelleScene(ecran = ECRAN_ACCUEIL, niveau = NIVEAU_FACILE):
    return {
        "entites": [],
        "reserve": [],
        "tempsDepart": None, #Va contenir le temps de depart de chaque scene
        "dernierTempsJeu": pygame.time.get_ticks(),
        "dernierTempsSaut": None,
        "dernierTempsEau": None,
        "dernierTempsVie": None,
        "dernierTempsOcean": None,
        "dernierTempsTouche": None,
        "dernierTempsJungle": None,
        "cameraDeplacementVerticale": 0,
        "score": 0, #equivalent à la distance parcouru
        "scorePiece": 0,
        "nombreDeVie": NOMBRE_DE_VIE_MAXIMUM,
        "enPause": False,
        "enJeu": False,
        "fini": False,
        "enGameOver": False,
        "balle": None,
        "peutSauter": False,
        "ecran": ecran,
        "niveau": niveau
    }

def estFini(scene):
    return scene.get("fini")

def terminerScene(scene):
    scene["fini"] = True
    
def niveauActuel(scene):
    return scene.get("niveau")

def modifierNiveau(scene, niveau):
    scene["niveau"] = niveau
    miseAJourVitesseHorizontale()
    
def ecranActuel(scene):
    return scene.get("ecran")

def modifierEcran(scene, ecran):
    scene["ecran"] = ecran

def tempsDepartScene(scene):
    return scene.get("tempsDepart")

def modifierTempsDepartScene(scene, tempsDepart = None):
    scene["tempsDepart"] = tempsDepart

def dernierTempsJeuxScene(scene):
    return scene.get("dernierTempsJeux")

def modifierDernierTempsJeuxScene(scene, dernierTempsJeu = None):
    scene["dernierTempsJeux"] = dernierTempsJeu

def dernierTempsSautScene(scene):
    return scene.get("dernierTempsSaut")

def modifierDernierTempsSautScene(scene, dernierTempsSaut = None):
    scene["dernierTempsSaut"] = dernierTempsSaut

def dernierTempsEauScene(scene):
    return scene.get("dernierTempsEau")

def modifierDernierTempsEauScene(scene, dernierTempsEau = None):
    scene["dernierTempsEau"] = dernierTempsEau

def dernierTempsVieScene(scene):
    return scene.get("dernierTempsVie")

def modifierDernierTempsVieScene(scene, dernierTempsVie = None):
    scene["dernierTempVie"] = dernierTempsVie

def dernierTempsOceanScene(scene):
    return scene.get("dernierTempsOcean")

def modifierDernierTempsOcean(scene, dernierTempsOcean = None):
    scene["dernierTempsOcean"] = dernierTempsOcean

def dernierTempsToucheScene(scene):
    return scene.get("dernierTempsTouche")

def modifierDernierTempsToucheScene(scene, dernierTempsTouche = None):
    scene["dernierTempsTouche"] = dernierTempsTouche
    
def dernierTempsJungleScene(scene):
    return scene.get("dernierTempsJungle")

def modifierDernierTempsJungleScene(scene, dernierTempsJungle = None):
    scene["dernierTempsJungle"] = dernierTempsJungle

def cameraPositionScene(scene):
    return scene.get("cameraDeplacementVerticale")

def modifierCameraPositionScene(scene, cameraPosition = 0):
    scene["cameraDeplacementVerticale"] = cameraPosition

def scoreScene(scene):
    return scene.get("score")

def modifierScoreScene(scene, score = 0):
    scene["score"] = score

def scorePieceScene(scene):
    return scene.get("scorePiece")

def modifierScorePiece(scene, scorePiece = 0):
    scene["scorePiece"] = scorePiece

def nombreDeVieScene(scene):
    return scene.get("nombreDeVie")

def modifierNombreDeVie(scene, nombre = 0):
    scene["nombreDeVie"] = nombre

def estEnPause(scene):
    return scene.get("enPause")
    
def modifierPause(scene, etat = False):
    scene["enPause"] = etat
    
def mettreEnPause(scene):
    modifierPause(scene, etat = True)

def estEnJeu(scene):
    return scene.get("enJeu")

def mettreEnJeu(scene):
    scene["enJeu"] = True
    modifierPause(scene, etat = False)

def estGameOver(scene):
    return scene.get("enGameOver")
    
def modifierGameOver(scene, etat = False):
    scene["enGameOver"] = etat
    
def mettreEnGameOver(scene):
    modifierGameOver(scene, True)

def balleScene(scene):
    return scene.get("balle")

def modifierBalleScene(scene, balle = None):
    scene["balle"] = balle

def ballePeutSauterSurScene(scene):
    return scene.get("peutSauter")

def modifierEtatSautScene(scene, etat = False):
    scene["peutSauter"] = etat

def preprareScene(background):
    FENETRE.fill(NOIR)
    FENETRE.blit(background, (0,0))
    
def afficherScene(scene):
    preprareScene(IMAGE_SCENE)    

def ajouterEntite(scene, entitee):
    scene["entites"].append(entitee)

def sceneReserve(scene):
    return scene["reserve"]

def ajouterEntiteReserve(scene, entitee):
    sceneReserve(scene).append(entitee)

def tailleReserve(scene):
    return len(sceneReserve(scene))

def prendreDansReserve(scene):
    if tailleReserve(scene) > 0:
        return sceneReserve(scene).pop(0)
    return None
    
def listEntite(scene):
    return scene["entites"]

# Gestion des entités

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

def estVisible(entite):
    return entite["visible"]

def estEntite(scene, entite):
    return listEntite(scene).count(entite) != 0

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
        vh = gestionVitesse()
        vx = vitesseEntite(entite)[0]
        
        if vx >= 0:
            if vx > 0:
                actuelle += 2
            else:
                actuelle += 1
            
        if actuelle >= nbr_poses:
            actuelle = 0
            
        modifierPoseActuelle(entite, actuelle)
        modifierImage(entite, listPoses(entite)[actuelle])

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

def collision_avec(entite, entite_list = []):
    return rectangle(entite).collidelistall([rectangle(o) for o in entite_list])
        

def creerSol(position):
    entite = nouvelleEntite(TYPE_SOL, IMAGE_SOL)
    
    modifierPosition(entite, position)
    modifierTaille(entite, (SOL_LARGEUR, SOL_HAUTEUR))
    modifierAcceleration(entite, (0,0))
    modifierVitesse(entite, (-gestionVitesse(), 0))
    modifierDernierTemps(entite, pygame.time.get_ticks())
    
    return entite

def creerEau(position):
    entite = nouvelleEntite(TYPE_EAU, IMAGE_EAU)
    
    modifierPosition(entite, position)
    modifierTaille(entite, (EAU_LARGEUR, EAU_HAUTEUR))
    modifierAcceleration(entite, (0,0))
    modifierVitesse(entite, (-gestionVitesse(), 0))
    modifierDernierTemps(entite, pygame.time.get_ticks())
    
    return entite

def creerPiecePour(entite, type=TYPE_PIECE, image=None):
    
    x, y = positionEntite(entite)
    largeur, hauteur = tailleEntite(entite)
    marge = 0
    
    if typeEntite(entite) == TYPE_EAU:
        marge = random.randint(3, 5)
    else:
        marge = random.randint(1, 3)
    
    entite = nouvelleEntite(type, IMAGE_PIECE if not image else image)
    
    x += (largeur - PIECE_LARGEUR)/2
    y += hauteur + PIECE_MARGE * marge
    
    modifierPosition(entite, (x, y))
    modifierTaille(entite, (PIECE_LARGEUR, PIECE_HAUTEUR))
    modifierAcceleration(entite, (0,0))
    modifierVitesse(entite, (-gestionVitesse(), 0))
    modifierDernierTemps(entite, pygame.time.get_ticks())
    
    return entite

def creerBrickPour(entite, cassable = False, marge = 1):
    
    x, y = positionEntite(entite)
    largeur, hauteur = tailleEntite(entite)
    
    entite = nouvelleEntite(TYPE_BRICK if not cassable else TYPE_BROKEN_BRICK, IMAGE_BRICK if not cassable else IMAGE_BROKENABLE_BRICK)
    
    x += (largeur - BRICK_LARGEUR)/2
    y += hauteur + BRICK_MARGE*marge
    
    modifierPosition(entite, (x, y))
    modifierTaille(entite, (BRICK_LARGEUR, BRICK_HAUTEUR))
    modifierAcceleration(entite, (0,0))
    modifierVitesse(entite, (-gestionVitesse(), 0))
    modifierDernierTemps(entite, pygame.time.get_ticks())
    
    return entite

def generer_pas(y, max = SOL_POSITION_MAXIMALE, min = SOL_POSITION_MINIMALE, marge = SOL_MARGE_VERTICALE):
    marge_hauter_haut = (max - y) // marge 
    marge_hauter_bas = (y - min) // marge 
    
    if marge_hauter_haut > 2:
        marge_hauter_haut = 2
        
    elif marge_hauter_bas < -2:
        marge_hauter_bas = -2
    
    if marge_hauter_haut < 0:
        marge_hauter_haut = 0
        
    return random.randint(-marge_hauter_bas, marge_hauter_haut)

def generer_hauteur(position_y_precedente, hauteur_precedente, type_precedente, type_actuelle):
    hauteur = 0
    
    if type_actuelle == TYPE_EAU:
        hauteur = position_y_precedente + hauteur_precedente - EAU_HAUTEUR
    else:
        if type_actuelle == TYPE_SOL:
            if type_precedente == TYPE_EAU:
                marge = (generer_pas(position_y_precedente)%2) * SOL_MARGE_VERTICALE
                hauteur = position_y_precedente + hauteur_precedente - SOL_HAUTEUR + abs(marge)
            else:
                marge = generer_pas(position_y_precedente) * SOL_MARGE_VERTICALE
                hauteur = position_y_precedente + marge
    
    return hauteur

def ajouter_piece(resultat):
    maintenant = pygame.time.get_ticks()
    
    if dernierTempsVieScene(scene) and nombreDeVieScene(scene) < NOMBRE_DE_VIE_MAXIMUM and maintenant - dernierTempsVieScene(scene) > VIE_INTERVALLE and random.randint(0, 1000) < 7:
        resultat.append(creerPiecePour(resultat[len(resultat)-1], type=TYPE_VIE, image=IMAGE_VIE))
        modifierDernierTempsVieScene(scene, maintenant)
    elif scoreScene(scene) > PIECE_DELAI and random.randint(0, 10) > 5 and ecranActuel(scene) == ECRAN_DE_JEUX:
        resultat.append(creerPiecePour(resultat[len(resultat)-1]))
    
    if not dernierTempsVieScene(scene):
        modifierDernierTempsVieScene(scene, maintenant)
        
    return resultat

def generer_entite(dernier_entite, position_precedente, taille_precedente, maintenant):
    x = position_precedente[0] + taille_precedente[0] - SOL_MARGE_HORIZONTALE
    hauteur = 0
    resultat = list()
    
    if scoreScene(scene) > BALLE_POSITION and ecranActuel(scene) == ECRAN_DE_JEUX and dernier_entite:
        if dernierTempsJungleScene(scene) and typeEntite(dernier_entite) == TYPE_SOL and maintenant - dernierTempsJungleScene(scene) > JUNGLE_INTERVAL and random.randint(0, 10) > 7: 
            modifierDernierTempsJungleScene(scene, maintenant)
            longeur = random.randint(JUNGLE_LONGUEUR_MINIMALE, JUNGLE_LONGUEUR_MAXIMALE)
            total = 0
            block_existe = 0
            y = position_precedente[1]
            
            if y < SOL_POSITION_MAXIMALE:
                while y + SOL_MARGE_VERTICALE < SOL_POSITION_MAXIMALE:
                    y += SOL_MARGE_VERTICALE
                    entite = creerSol((x + total - SOL_MARGE_HORIZONTALE, y))
                    total += tailleEntite(entite)[0]
                    resultat.append(entite)
                    resultat = ajouter_piece(resultat)
            
            while total < longeur:
                entite = None
                
                if block_existe:
                    if random.randint(0, 10) > 7:
                        entite = creerSol((x + total - SOL_MARGE_HORIZONTALE, y))
                        block_existe = 1
                    else:
                        entite = creerSol((x + total - SOL_MARGE_HORIZONTALE, SOL_POSITION_MINIMALE))
                        block_existe = 0
                    resultat.append(entite)
                    
                else:
                    block_existe = 1
                    entite = creerSol((x + total - SOL_MARGE_HORIZONTALE, y))
                    resultat.append(entite)
                    resultat = ajouter_piece(resultat)
                
                total += tailleEntite(entite)[0]
            
            return resultat
        
        elif dernierTempsOceanScene(scene) and typeEntite(dernier_entite) != TYPE_EAU and maintenant - dernierTempsOceanScene(scene) > OCEAN_INTERVAL and random.randint(0, 10) > 9:
            modifierDernierTempsOcean(scene, maintenant)
            modifierDernierTempsEauScene(scene, maintenant)
            longeur = random.randint(OCEAN_LONGUEUR_MINIMALE, OCEAN_LONGUEUR_MAXIMALE)
            total = 0
            brick_existe = 0
            
            while total < longeur:
                hauteur = generer_hauteur(position_precedente[1], taille_precedente[1], typeEntite(dernier_entite), TYPE_EAU) 
                entite = creerEau((x + total, hauteur - SOL_MARGE_HORIZONTALE))
                total += tailleEntite(entite)[0]
                
                resultat.append(entite)
                
                if not brick_existe or random.randint(0, 100) > 5:
                    if brick_existe and random.randint(0, 100) > 93:
                        brick_existe = 0
                        resultat.append(creerBrickPour(entite, True))
                    else:
                        brick_existe = 1
                        resultat.append(creerBrickPour(entite))
                    resultat = ajouter_piece(resultat)
                else:
                    brick_existe = 0
            
            return resultat
        
        elif dernierTempsEauScene(scene) and typeEntite(dernier_entite) != TYPE_EAU and maintenant - dernierTempsEauScene(scene) > EAU_INTERVAL:
            modifierDernierTempsEauScene(scene, maintenant)
            modifierDernierTempsOcean(scene, maintenant)
            hauteur = generer_hauteur(position_precedente[1], taille_precedente[1], typeEntite(dernier_entite), TYPE_EAU) 
            resultat.append(creerEau((x, hauteur)))
            
        else:
            hauteur = generer_hauteur(position_precedente[1], taille_precedente[1], typeEntite(dernier_entite), TYPE_SOL)
            resultat.append(creerSol((x, hauteur)))
        
        if not dernierTempsEauScene(scene):
            modifierDernierTempsEauScene(scene, maintenant)
        
        if not dernierTempsOceanScene(scene):
            modifierDernierTempsOcean(scene, maintenant)
        
        if not dernierTempsJungleScene(scene):
            modifierDernierTempsJungleScene(scene, maintenant)
    else:
        resultat.append(creerSol((x, SOL_POSITION_MINIMALE)))
    
    return ajouter_piece(resultat)

def nettoyerScene(scene):
    for entite in listEntite(scene):
        x, y = positionEntite(entite)
        hauteur = tailleEntite(entite)[1]
        if x < -FENETRE_MARGE_EXTERNE or y > FENETRE_HAUTEUR + FENETRE_MARGE_EXTERNE * 2 or y + hauteur < -FENETRE_MARGE_EXTERNE:
            listEntite(scene).remove(entite)

def remplirScene(scene, maintenant):
    nettoyerScene(scene)
    nombre_elements = nombreElementScene(scene)
        
    derniere_position = (0,0)
    derniere_taille = (0,0)
    dernier = None
    require = [TYPE_SOL, TYPE_EAU]
    
    if nombre_elements > 0:
        dernier = derniereEntite(scene, require)
        if dernier:
            derniere_position = positionEntite(dernier)
            derniere_taille = tailleEntite(dernier)
    
    while derniere_position[0] + derniere_taille[0] < FENETRE_LARGEUR + FENETRE_MARGE_EXTERNE:
        if tailleReserve(scene) > 0:
            entite = prendreDansReserve(scene)
            ajouterEntite(scene, entite)
                
            if require.count(typeEntite(entite)) != 0:
                dernier = entite
                derniere_position = positionEntite(dernier)
                derniere_taille = tailleEntite(dernier)
        else:
            for entite in generer_entite(dernier, derniere_position, derniere_taille, maintenant):
                entite = reveillerEntite(entite)
            
                if derniere_position[0] + derniere_taille[0] > FENETRE_LARGEUR + FENETRE_MARGE_EXTERNE:
                    ajouterEntiteReserve(scene, entite)
                else:
                    ajouterEntite(scene, entite) 

                if require.count(typeEntite(entite)) != 0:
                    dernier = entite
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
    
    return (x0 + vx0 * dt + 0.5 * ax * dt**2, y0 + vy0 * dt  + 0.5 * ay * dt**2)

def gestionVitesse():
    vitesse_initiale = 0
    if niveauActuel(scene) == NIVEAU_FACILE:
        vitesse_initiale = VITESSE_HORIZONTALE * FACTEUR_V_FACILE
        facteur_niveau = VITESSE_HORIZONTALE * (FACTEUR_V_NORMAL - FACTEUR_V_FACILE)
    elif niveauActuel(scene) == NIVEAU_NORMAL:
        vitesse_initiale = VITESSE_HORIZONTALE * FACTEUR_V_NORMAL
        facteur_niveau = VITESSE_HORIZONTALE * (FACTEUR_V_DIFFICILE - FACTEUR_V_NORMAL)
    else:
        vitesse_initiale = VITESSE_HORIZONTALE * FACTEUR_V_DIFFICILE
        facteur_niveau = VITESSE_HORIZONTALE * (FACTEUR_V_MAX - FACTEUR_V_DIFFICILE)
    
    if scoreScene(scene) < SCORE_V_MAX:
        return vitesse_initiale + (scoreScene(scene) / SCORE_V_MAX * facteur_niveau)
    else:
        return vitesse_initiale + (facteur_niveau / SCORE_V_MAX)

def miseAJourEntite(scene, maintenant, change_pose):
    nbr = nombreElementScene(scene)
    dt = 0
    
    if nbr > 0:
        for entite in listEntite(scene):
            dt = maintenant - dernierTempsEntite(entite)
            position = positionEntite(entite)
            vitesse = vitesseEntite(entite)
            acceleration = accelerationEntite(entite)
            
            vitesse = mru_vitesse(vitesse, acceleration, dt)
            position = mru_position(position, vitesse, acceleration, dt)
            
            modifierVitesse(entite, vitesse)
            modifierPosition(entite, position)
            
            if estAnime(entite) and change_pose:
                progresserAnimation(entite)
            modifierDernierTemps(entite, maintenant) 
                
    collisionBalle() 
    
def miseAJourDernierTemps(scene, maintenant):
    nbr = nombreElementScene(scene)
    
    if nbr > 0:
        for entite in listEntite(scene):
            modifierDernierTemps(entite, maintenant)
            
def miseAJourVitesseHorizontale():
    nbr = nombreElementScene(scene)
    
    if nbr > 0:
        for entite in listEntite(scene):
            if typeEntite(entite) != TYPE_BALLE:
                vy = vitesseEntite(entite)[1]
                modifierVitesse(entite, (-gestionVitesse(), vy))
            

def afficheEntite(scene):
    entites = listEntite(scene)
    
    for entite in entites:
        if estVisible(entite):
            x, y = positionEntite(entite)
            w, h = tailleEntite(entite)
            if x + w <= FENETRE_LARGEUR + FENETRE_MARGE_EXTERNE:
                y -= cameraPositionScene(scene)
                FENETRE.blit(imageEntite(entite), repere_vers_pygame((x, y), (w, h)))

def creerImage(path, taille):
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(FENETRE), taille) 

def generer_vitesse_saut():
    temps = pygame.time.get_ticks() - dernierTempsToucheScene(scene)
    
    if temps > TEMPS_DE_TOUCHE_MAXIMALE:
        temps = TEMPS_DE_TOUCHE_MAXIMALE
    elif temps < TEMPS_DE_TOUCHE_MAXIMALE/2:
        temps = TEMPS_DE_TOUCHE_MAXIMALE/2
    
    modifierDernierTempsToucheScene(scene, None)
    
    return VITESSE_VERTICALE * (temps/(TEMPS_DE_TOUCHE_MAXIMALE/2))

# Musique

def initialiserMusique():
    global sound_piece, sound_saut, sound_collision
    pygame.mixer.init()
    
    start_musique(MUSIQUE_ACCUEIL)
    sound_piece = pygame.mixer.Channel(1)
    sound_saut = pygame.mixer.Channel(2)
    sound_collision = pygame.mixer.Channel(3)

def start_musique(path):
    pygame.mixer.music.load(path)
    if path == MUSIQUE_GAMEOVER:
        pygame.mixer.music.play(1)
    else:
        pygame.mixer.music.play(-1)
    if path == MUSIQUE_JEU:
        pygame.mixer.music.set_volume(0.2)

def stop_musique(temps):
    pygame.mixer.music.fadeout(temps)

def creer_son(path, volume):
    son = pygame.mixer.Sound(path)
    son.set_volume(volume)
    return son

def playSound(son):
    if son == SON_PIECE:
        if not sound_piece.get_busy():
            sound_piece.play(son)
    elif son == SON_SAUT:
        if not sound_saut.get_busy():
            sound_saut.play(son)
    else:
        if not sound_collision.get_busy():
            sound_collision.play(son)

# Gestion des collisions

def faireSauterBalle(maintenant):
    if ballePeutSauterSurScene(scene):
        vx = vitesseEntite(balleScene(scene))[0]
        ax = accelerationEntite(balleScene(scene))[0]
        
        if vx < 0:
            vx = gestionVitesse()

        modifierVitesse(balleScene(scene), (vx, generer_vitesse_saut()))
        modifierAcceleration(balleScene(scene), (ax,-ACCELERATION_GRAVITATIONNELLE))
        modifierDernierTempsSautScene(scene, None)
        playSound(SON_SAUT)
    else:
        modifierDernierTempsSautScene(scene, maintenant)

def estPoseSur(entite1, entite2, marge):
    y1 = positionEntite(entite1)[1]
    y2 = positionEntite(entite2)[1] + tailleEntite(entite2)[1]
    
    if ( y1 - marge < y2 and y1 + marge >= y2 ) or y1 == y2:
        return True
    return False

def peutTomber(entite1, entite2):
    # Retourne 0 si l'entite 1 ne peut pas tomber
    # Retourne -1 si l'entite peut tomber par l'avant
    # Retourne 1 si l'entite peut tomber par l'arrière
    
    x1 = positionEntite(entite1)[0]
    w1 = tailleEntite(entite1)[0]
    
    x2 = positionEntite(entite2)[0]
    w2 = tailleEntite(entite2)[0]
    
    if x1 < x2:
        if x1 + w1 - x2 < w1 / 2:
            return -1
    elif x2 + w2 < x1 + w1:
        if x1 + w1 - x2 - w2 > w1 / 2:
            return 1
    return 0

def vaTomber(direction_chute, id_collision, nombre_de_collision):
    return (direction_chute < 0 and id_collision == 0) or (direction_chute > 0 and id_collision+1 == nombre_de_collision)

def collisionBalle():
    balle = balleScene(scene)
    entites = [item for item in listEntite(scene) if item != balle and estVisible(item)]
    collisions = collision_avec(balle, entites)
    id_collision = 0
    nombre_de_collision = len(collisions)
    
    est_au_sol = False
    est_sur_eau = False
    
    if len(collisions) != 0:
        for collision in collisions:
            xb = positionEntite(balle)[0]
            vy = vitesseEntite(balle)[1]
            entite = entites[collision]

            #Pour vérifier que la balle est posée 
            #Sur l'entité en question
            if estPoseSur(balle, entite, BALLE_TOUCHE_MARGE):
                etype = typeEntite(entite)
                
                if etype == TYPE_SOL or etype == TYPE_BRICK or etype == TYPE_BROKEN_BRICK:
                    est_au_sol = True
                    modifierEtatSautScene(scene, True)
                    direction_chute = peutTomber(balle, entite)
                    
                    if vy < 0:
                        #Pour contrer la gravité de la balle
                        #lorsque la balle touche le sol
                        modifierPosition(balle, (xb, positionEntite(entite)[1]+tailleEntite(entite)[1]-BALLE_TOUCHE_MARGE))
                        modifierVitesse(balle, (vitesseEntite(balle)[0], 0))
                        modifierAcceleration(balle, (0,0))
                        if etype == TYPE_SOL:
                            playSound(SON_COLLISION_SOL)
                        else:
                            playSound(SON_COLLISION_BRIQUE)
                    else:
                        if positionEntite(balle)[0] < BALLE_POSITION:
                            #Pour que la balle retrouve
                            #sa position d'orgine
                            modifierVitesse(balle, (0, vitesseEntite(balle)[1]))
                            modifierAcceleration(balle, (ACCELERATION_HORIZONTALE/5, accelerationEntite(balle)[1]))
                        else:
                            modifierVitesse(balle, (0, vitesseEntite(balle)[1]))
                    
                    #Pour pemetre que la balle tombe
                    #Lorsque la reception est mauvaise
                    if vaTomber(direction_chute, id_collision, nombre_de_collision):
                        #pour eviter de sauter violement après avoir
                        #été coincé derrière un obstacle
                        if direction_chute < 0:
                            modifierPosition(balle, (positionEntite(entite)[0] - BALLE_RAYON * 2 + BALLE_TOUCHE_MARGE, positionEntite(balle)[1]))
                        
                        if vitesseEntite(balle)[0] <= 0:
                            modifierVitesse(balle, (gestionVitesse()*direction_chute, vitesseEntite(balle)[1]))
                        
                        if not est_sur_eau:
                            modifierAcceleration(balle, (ACCELERATION_HORIZONTALE, -ACCELERATION_GRAVITATIONNELLE))
                            
                    elif positionEntite(balle)[0] < BALLE_POSITION:
                        modifierVitesse(balle, (gestionVitesse(), vitesseEntite(balle)[1]))
                    elif etype == TYPE_BROKEN_BRICK:
                        modifierImage(entite, IMAGE_BROKEN_BRICK)
                        modifierPosition(balle, (positionEntite(balle)[0] + BALLE_TOUCHE_MARGE, positionEntite(entite)[1] - BALLE_RAYON))
                        modifierAcceleration(balle, (ACCELERATION_HORIZONTALE, -ACCELERATION_GRAVITATIONNELLE))
                        playSound(SON_BRIQUE_CASSE)
                    
                        
                elif etype == TYPE_EAU:
                    direction_chute = peutTomber(balle, entite)
                    est_sur_eau = True
                    
                    if not direction_chute:
                        
                        modifierPosition(balle, (xb, positionEntite(entite)[1]+tailleEntite(entite)[1]-BALLE_TOUCHE_MARGE))
                        modifierVitesse(balle, (gestionVitesse()*direction_chute,0))
                        modifierAcceleration(balle, (0,0))
                        playSound(SON_COLLISION_EAU)
                        
                        if positionEntite(entite)[0] - BALLE_TOUCHE_MARGE <= xb:
                            modifierVitesse(balle, (-gestionVitesse(),0))
                    elif vaTomber(direction_chute, id_collision, nombre_de_collision):
                        #pour eviter de sauter violement après avoir
                        #été coincé derrière un obstacle
                        if direction_chute < 0:
                            modifierPosition(balle, (positionEntite(entite)[0] - BALLE_RAYON*2 + BALLE_TOUCHE_MARGE, positionEntite(balle)[1]))
                            playSound(SON_COLLISION_EAU)
                        modifierVitesse(balle, (gestionVitesse()*direction_chute, vitesseEntite(balle)[1]))
                            
                    elif positionEntite(balle)[0] < BALLE_POSITION:
                        modifierVitesse(balle, (gestionVitesse(), vitesseEntite(balle)[1]))
                        playSound(SON_COLLISION_EAU)
                        
                elif etype == TYPE_PIECE:
                    if vitesseEntite(entite)[1] == 0:
                        modifierScorePiece(scene, scorePieceScene(scene)+1)
                    modifierVitesse(entite, (-gestionVitesse(), VITESSE_VERTICALE))
                elif etype == TYPE_VIE:
                    endormirEntite(entite)
                    if nombreDeVieScene(scene) < NOMBRE_DE_VIE_MAXIMUM:
                        modifierNombreDeVie(scene, nombreDeVieScene(scene)+1)
            else:
                etype = typeEntite(entite)
                
                if etype == TYPE_SOL and not est_sur_eau:
                    direction_vitesse = 0
                    if positionEntite(balle)[0] < positionEntite(entite)[0]:
                        direction_vitesse = -1
                        modifierPosition(balle, (positionEntite(entite)[0] - BALLE_RAYON*2 + BALLE_TOUCHE_MARGE, positionEntite(balle)[1]))

                    modifierVitesse(balle, (gestionVitesse()*direction_vitesse, vitesseEntite(balle)[1]))
                
                elif etype == TYPE_PIECE:
                    if vitesseEntite(entite)[1] == 0:
                        modifierScorePiece(scene, scorePieceScene(scene)+1)
                        playSound(SON_PIECE)
                    modifierVitesse(entite, (-gestionVitesse(), VITESSE_VERTICALE))
                
                elif etype == TYPE_VIE:
                    endormirEntite(entite)
                    if nombreDeVieScene(scene) < NOMBRE_DE_VIE_MAXIMUM:
                        modifierNombreDeVie(scene, nombreDeVieScene(scene)+1)
                
            if not est_au_sol and not est_sur_eau:
                modifierAcceleration(balle, (0, -ACCELERATION_GRAVITATIONNELLE))
                modifierEtatSautScene(scene, False)
                
            id_collision += 1
    else:
        modifierVitesse(balle, (0, vitesseEntite(balle)[1]))
        modifierAcceleration(balle, (0, -ACCELERATION_GRAVITATIONNELLE))
        modifierEtatSautScene(scene, False)
        
        if positionEntite(balle)[1] - FENETRE_HAUTEUR + FENETRE_MARGE_INTERNE >= 0:
            modifierCameraPositionScene(scene, positionEntite(balle)[1] - FENETRE_HAUTEUR + FENETRE_MARGE_INTERNE)
            

def lire_score(chemin):
    liste_score = []
    with open(chemin, 'r') as fichier:
        ligne = fichier.readline()
        for elem in ligne.split(" "):
            if elem !='':
                liste_score.append(float(elem))
        return(liste_score)
        
def ajout_score(scr, scr_pieces, chemin):
    #compare le nouveau score passé en paramètre avec le score enregistré dans le fichier dont le chemin est donné en paramètre, 
    #et remplace le code enregistré dans le fichier par le nouveau code dans le cas où le nouveau code est meilleur
    with open(chemin, 'w+') as fichier:
        scores = lire_score(chemin)
        if len(scores)==0:
            fichier.write(str(scr)+" "+str(scr_pieces))
        elif scores[0]<scr:
            fichier.truncate()
            fichier.write(str(scr)+" "+str(scr_pieces))

def dessinerTableauDeBord(maintenant):
    #Affichage du score du au parcour
    FENETRE.blit(IMAGE_BALLE_TABLEAU_DE_BORD, repere_vers_pygame((30, FENETRE_HAUTEUR * 0.9), (IMAGE_TABLEAU_DE_BORD_LARGEUR, IMAGE_TABLEAU_DE_BORD_HAUTEUR)))
    texte = " {0:.1f}".format(scoreScene(scene))
    image = police_tableau_de_bord.render(texte, True, JAUNE)
    FENETRE.blit(image, repere_vers_pygame((30 + IMAGE_TABLEAU_DE_BORD_LARGEUR + 10, FENETRE_HAUTEUR*0.9 + TABLEAU_DE_BORD_TAILLE_POLICE/5), (TABLEAU_DE_BORD_TAILLE_POLICE, TABLEAU_DE_BORD_TAILLE_POLICE)))
    
    #Affichage du score du aux pieces
    FENETRE.blit(IMAGE_PIECE_TABLEAU_DE_BORD, repere_vers_pygame((30, FENETRE_HAUTEUR * 0.9 - 40), (IMAGE_TABLEAU_DE_BORD_LARGEUR, IMAGE_TABLEAU_DE_BORD_HAUTEUR)))
    texte = " {0}".format(scorePieceScene(scene))
    image = police_tableau_de_bord.render(texte, True, JAUNE)
    FENETRE.blit(image, repere_vers_pygame((30 + IMAGE_TABLEAU_DE_BORD_LARGEUR + 10, FENETRE_HAUTEUR*0.9 + TABLEAU_DE_BORD_TAILLE_POLICE/5 - 40), (TABLEAU_DE_BORD_TAILLE_POLICE, TABLEAU_DE_BORD_TAILLE_POLICE)))
    
    #Affichage du score du aux pieces
    i = 0
    while i < nombreDeVieScene(scene):
        FENETRE.blit(IMAGE_VIE_TABLEAU_DE_BORD, repere_vers_pygame((30 + (IMAGE_TABLEAU_DE_BORD_LARGEUR + 10)*i, FENETRE_HAUTEUR * 0.9 - 80), (IMAGE_TABLEAU_DE_BORD_LARGEUR, IMAGE_TABLEAU_DE_BORD_HAUTEUR)))
        i += 1
    
    if dernierTempsToucheScene(scene):
        x, y = repere_vers_pygame((TABLEAU_DE_BORD_X, TABLEAU_DE_BORD_Y), (TABLEAU_DE_BORD_LARGEUR, TABLEAU_DE_BORD_HAUTEUR))
        rect = pygame.Rect(x, y, TABLEAU_DE_BORD_LARGEUR, TABLEAU_DE_BORD_HAUTEUR)
        
        temps = maintenant - dernierTempsToucheScene(scene)
        largeur = 0
        if temps > TEMPS_DE_TOUCHE_MAXIMALE:
            temps = TEMPS_DE_TOUCHE_MAXIMALE
        
        largeur = temps * 100/TEMPS_DE_TOUCHE_MAXIMALE #Pourcentage de l'argeur
        largeur *= TABLEAU_DE_BORD_LARGEUR/100 
            
        pygame.draw.rect(FENETRE, BLANC, rect, TABLEAU_DE_BORD_MARGE, 1)
        pygame.draw.rect(FENETRE, BLANC, pygame.Rect(x, y, largeur, TABLEAU_DE_BORD_HAUTEUR))

def dessinerEcranAccueilMessage():
    #Affichage du titre du Jaune
    image = police_ecran_de_jeu.render(TITRE, True, JAUNE)
    taille = image.get_rect()
    x = (FENETRE_LARGEUR - taille.width)/2
    y = FENETRE_HAUTEUR/2
    i = x - WALL_MARGE * 2
    while i < x + taille.width:
        FENETRE.blit(IMAGE_WALL, (i, y - WALL_DIMENSIONS))
        i += WALL_DIMENSIONS
    FENETRE.blit(image, repere_vers_pygame((x, y), (taille.width, taille.height)))

    
    image = police_tableau_de_bord.render("appuyez sur [espace]", True, JAUNE)
    taille = image.get_rect()
    x = (FENETRE_LARGEUR - taille.width)/2
    y -= WALL_MARGE + taille.height
    FENETRE.blit(image, repere_vers_pygame((x, y), (taille.width, taille.height)))


def dessinerEcranNiveauMessage():
    increment = FENETRE_HAUTEUR/6
    y = increment * 4
    niveaux = [("FACILE", NIVEAU_FACILE), ("NORMAL", NIVEAU_NORMAL), ("DIFFICILE", NIVEAU_DIFFICILE)]
    
    for niveau in niveaux:
        image = police_ecran_de_niveau.render(niveau[0], True, JAUNE if niveauActuel(scene) == niveau[1] else BLANC)
        taille = image.get_rect()
        
        i = (FENETRE_LARGEUR/7)*2.5
        
        if niveauActuel(scene) == niveau[1]:
            marge = WALL_MARGE/2
            largeur = math.ceil((FENETRE_LARGEUR/7)*1.5/NIVEAU_WALL_DIMENSIONS) * NIVEAU_WALL_DIMENSIONS + marge*2
            hauteur = NIVEAU_WALL_DIMENSIONS + marge*2
            x0, y0 = repere_vers_pygame((i-marge, y-marge), (largeur, hauteur))
            rect = pygame.Rect(x0, y0, largeur, hauteur)
            pygame.draw.rect(FENETRE, JAUNE, rect, 0, 4)
        
        while i < (FENETRE_LARGEUR/6) * 3.5:
            FENETRE.blit(IMAGE_NIVEAU_WALL, repere_vers_pygame((i, y), (NIVEAU_WALL_DIMENSIONS, NIVEAU_WALL_DIMENSIONS)))
            i += NIVEAU_WALL_DIMENSIONS
            
        x = (i - (FENETRE_LARGEUR/7)*2.5 - taille.width)/2 + (FENETRE_LARGEUR/7)*2.5
        FENETRE.blit(image, repere_vers_pygame((x, y + (NIVEAU_WALL_DIMENSIONS - taille.height)/2), (taille.width, taille.height)))
        y -= increment
    
    image = police_tableau_de_bord.render("appuyez sur [monter] et [descendre] ou [espace] pour continuer", True, JAUNE)
    taille = image.get_rect()
    x = (FENETRE_LARGEUR - taille.width)/2
    y = WALL_MARGE
    FENETRE.blit(image, repere_vers_pygame((x, y), (taille.width, taille.height)))
    
def dessinerFadeEcran(message = ""):
    surface = pygame.Surface((FENETRE_LARGEUR, FENETRE_HAUTEUR), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 200))
    surface = surface.convert_alpha()
    
    image = police_ecran_de_niveau.render(message, True, BLANC)
    taille = image.get_rect()
    x = (FENETRE_LARGEUR - taille.width)/2
    y = (FENETRE_HAUTEUR - taille.height)/2
    
    surface.blit(image, repere_vers_pygame((x, y), (taille.width, taille.height)))
    
    score_message = ""
    
    if estEnPause(scene):
        score_message = "Best Score: {0:.1f} | Coins: {1}".format(scoreScene(scene), scorePieceScene(scene))
    elif estGameOver(scene):
        best_score = lire_score(SCORE_FILE_PATH)
        score_message = "Best Score: {0:.1f} | Coins: {1}".format(best_score[0], best_score[1])
    
    if len(score_message) > 0:
        image = police_fade_screen.render(score_message, True, BLANC)
        y -= taille.height
        taille = image.get_rect() 
        x = (FENETRE_LARGEUR - taille.width)/2
        surface.blit(image, repere_vers_pygame((x, y), (taille.width, taille.height)))
    
    FENETRE.blit(surface, repere_vers_pygame((0, 0), (FENETRE_LARGEUR, FENETRE_HAUTEUR)))
    
    image = police_fade_screen.render("[espace] pour commencer le jeu et sauter", True, BLANC)
    taille = image.get_rect()
    FENETRE.blit(image, repere_vers_pygame((15, 60), (taille.width, taille.height)))
    
    image = police_fade_screen.render("[esc] pour entrer et sortir du mode pause", True, BLANC)
    taille = image.get_rect()
    FENETRE.blit(image, repere_vers_pygame((15, 35), (taille.width, taille.height)))
    
    image = police_fade_screen.render("[effacer] pour retourner au menu principal à partir d'ici", True, BLANC)
    taille = image.get_rect()
    FENETRE.blit(image, repere_vers_pygame((15, 10), (taille.width, taille.height)))
    
def creerBalleImage(path):   
    return creerImage(path, (BALLE_RAYON*2, BALLE_RAYON*2))

def creerBalle():
    balle = nouvelleEntite(TYPE_BALLE, IMAGES_BALLE[0])
    
    modifierTaille(balle, (BALLE_RAYON*2, BALLE_RAYON*2))
    modifierPosition(balle, (BALLE_POSITION // 2, SOL_POSITION_MINIMALE + SOL_HAUTEUR + SOL_MARGE_VERTICALE * 5 - VITESSE_VERTICALE))
    modifierVitesse(balle, (0,0))
    modifierAcceleration(balle, (0,0))
    modifierDernierTemps(balle, pygame.time.get_ticks())
    
    for image in IMAGES_BALLE:
        ajouterPose(balle, image)
    
    return reveillerEntite(balle)

def afficherTerrainClassique(maintenant):
    change_pose = True
    for t in range(tempsDepartScene(scene), maintenant+1):
        miseAJourEntite(scene, t, change_pose)
        change_pose = False
    modifierDernierTempsJeuxScene(scene, maintenant)
    
    if random.randint(0, 100) > 99:
        modifierDernierTempsToucheScene(scene, pygame.time.get_ticks())
    
    if dernierTempsToucheScene(scene) and random.randint(0, 10) > 9:
        faireSauterBalle(maintenant)
    
    remplirScene(scene, maintenant)
    afficherScene(scene)
    afficheEntite(scene)

# Gestion de l'écran de jeu
# Initialisation, affichage, entrées

def initialiserEcranJeu(conserver_score=False, conserver_dernier_temps=False):   
    global scene
    
    nouvelle_scene = nouvelleScene(ECRAN_DE_JEUX, niveauActuel(scene))
    balle = creerBalle()
    modifierTempsDepartScene(scene, pygame.time.get_ticks())
    
    if conserver_score:
        modifierScoreScene(nouvelle_scene, scoreScene(scene))
        modifierScorePiece(nouvelle_scene, scorePieceScene(scene))
        modifierNombreDeVie(nouvelle_scene, nombreDeVieScene(scene))
    
    if conserver_dernier_temps:
        modifierDernierTempsSautScene(scene, dernierTempsSautScene(scene))
        modifierDernierTempsEauScene(scene, dernierTempsEauScene(scene))
        modifierDernierTempsOcean(scene, dernierTempsOceanScene(scene))
        modifierDernierTempsToucheScene(scene, dernierTempsToucheScene(scene))
        modifierDernierTempsJungleScene(scene, dernierTempsJungleScene(scene))

    scene = nouvelle_scene
    
    ajouterEntite(scene, balle)
    modifierBalleScene(scene, balle)

def afficherEcranDeJeu(maintenant):
    if estEnJeu(scene) and not estEnPause(scene):
        commencerAnimation(balleScene(scene))
        change_pose = True
        
        if ballePeutSauterSurScene(scene) and dernierTempsSautScene(scene) and maintenant - dernierTempsSautScene(scene) < SAUTE_DELAI:
            faireSauterBalle(maintenant)
        
        for t in range(tempsDepartScene(scene), maintenant+1):
            miseAJourEntite(scene, t, change_pose)
            change_pose = False
        
        if not estGameOver(scene):
            modifierScoreScene(scene, scoreScene(scene) + (maintenant-dernierTempsJeuxScene(scene))*gestionVitesse())
        modifierDernierTempsJeuxScene(scene, maintenant)
    else:
        miseAJourDernierTemps(scene, maintenant)
    
    if not estEnPause(scene):
        remplirScene(scene, maintenant)
        
    afficherScene(scene)
    afficheEntite(scene)
    dessinerTableauDeBord(maintenant)
    
    if not estEnJeu(scene):
        if nombreDeVieScene(scene) < NOMBRE_DE_VIE_MAXIMUM:
            dessinerFadeEcran("OUPS!")
        else:
            dessinerFadeEcran("PREPARES TOI!")
    elif estEnPause(scene):
        dessinerFadeEcran("PAUSE")
    elif not estEntite(scene, balleScene(scene)):
        if nombreDeVieScene(scene):
            playSound(SON_ERREUR)
            modifierNombreDeVie(scene, nombreDeVieScene(scene)-1)
            initialiserEcranJeu(conserver_score=True, conserver_dernier_temps=True)
        else:
            if not estGameOver(scene):
                ajout_score(scoreScene(scene), scorePieceScene(scene), SCORE_FILE_PATH)
                start_musique(MUSIQUE_GAMEOVER)
            mettreEnGameOver(scene)
            dessinerFadeEcran("GAME OVER")

def traiterEntreeEcranDeJeu(evenement, maintenant):
    if evenement.type == pygame.KEYDOWN:
        if (estEnPause(scene) or estGameOver(scene) or not estEnJeu(scene)) and evenement.key == pygame.K_BACKSPACE:
            modifierGameOver(scene, False)
            start_musique(MUSIQUE_ACCUEIL)
            initialiserEcranAccueil()
                
        if not estEnJeu(scene):
            if evenement.key == pygame.K_SPACE:
                mettreEnJeu(scene)
                modifierDernierTempsJeuxScene(scene, pygame.time.get_ticks())
                start_musique(MUSIQUE_JEU)
        elif not estGameOver(scene):   
            if evenement.key == pygame.K_SPACE:
                modifierDernierTempsToucheScene(scene, pygame.time.get_ticks())
            elif evenement.key == pygame.K_ESCAPE:
                modifierPause(scene, not estEnPause(scene))
    elif evenement.type == pygame.KEYUP:
        if estEnJeu(scene):
            if evenement.key == pygame.K_SPACE:
                if dernierTempsToucheScene(scene):
                    faireSauterBalle(maintenant)

# Gestion de l'écran d'accueil
# Initialisation, affichage, entrées

def initialiserEcranAccueil():   
    global scene
    
    scene = nouvelleScene(ECRAN_ACCUEIL, niveauActuel(scene) if scene else NIVEAU_FACILE)
    balle = creerBalle()
    random.seed() 
    
    modifierTempsDepartScene(scene, pygame.time.get_ticks())
    modifierPosition(balle, (positionEntite(balle)[0], SOL_POSITION_MINIMALE + SOL_HAUTEUR))
    ajouterEntite(scene, balle)
    commencerAnimation(balle)
    modifierBalleScene(scene, balle)

def afficherEcranAccueil(maintenant):
    afficherTerrainClassique(maintenant)
    dessinerEcranAccueilMessage()

def traiterEntreeEcranAccueil(evenement):
    if evenement.type == pygame.KEYDOWN:
        if evenement.key == pygame.K_SPACE:
            initialiserEcranNiveau()

# Gestion de choix de niveau
# Initialisation, affichage, entrées

def initialiserEcranNiveau():
    initialiserEcranAccueil()
    modifierEcran(scene, ECRAN_SELECTION_NIVEAU)

def afficherEcranNiveau(maintenant):
    afficherTerrainClassique(maintenant)
    dessinerEcranNiveauMessage()

def traiterEntreeEcranNiveau(evenement):
    if evenement.type == pygame.KEYDOWN:
        
        if evenement.key == pygame.K_SPACE:
            stop_musique(200)
            initialiserEcranJeu()
            
        elif evenement.key == pygame.K_ESCAPE:
            initialiserEcranAccueil()
            
        elif evenement.key == pygame.K_UP:
            if niveauActuel(scene) == NIVEAU_DIFFICILE:
                modifierNiveau(scene, NIVEAU_NORMAL)
            elif niveauActuel(scene) == NIVEAU_NORMAL:
                modifierNiveau(scene, NIVEAU_FACILE)
            else:
                modifierNiveau(scene, NIVEAU_DIFFICILE)
                
        elif evenement.key == pygame.K_DOWN:
            if niveauActuel(scene) == NIVEAU_FACILE:
                modifierNiveau(scene, NIVEAU_NORMAL)
            elif niveauActuel(scene) == NIVEAU_NORMAL:
                modifierNiveau(scene, NIVEAU_DIFFICILE)
            else:
                modifierNiveau(scene, NIVEAU_FACILE)

def traite_entrees(maintenant = 0):
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            terminerScene(scene)
        
        if ecranActuel(scene) == ECRAN_DE_JEUX:
            traiterEntreeEcranDeJeu(evenement, maintenant)
        elif ecranActuel(scene) == ECRAN_ACCUEIL:
            traiterEntreeEcranAccueil(evenement)
        elif ecranActuel(scene) == ECRAN_SELECTION_NIVEAU:
            traiterEntreeEcranNiveau(evenement)

# Initialisation
pygame.init()

FENETRE = pygame.display.set_mode((FENETRE_LARGEUR, FENETRE_HAUTEUR))

pygame.display.set_caption("Bounce Tales")

IMAGE_SOL = creerImage("images/ground.png", (SOL_LARGEUR, SOL_HAUTEUR))
IMAGE_EAU = creerImage("images/water.png", (EAU_LARGEUR, EAU_HAUTEUR))

IMAGE_WALL = creerImage("images/wall.png", (WALL_DIMENSIONS, WALL_DIMENSIONS))
IMAGE_NIVEAU_WALL = creerImage("images/wall.png", (NIVEAU_WALL_DIMENSIONS, NIVEAU_WALL_DIMENSIONS))

IMAGE_BRICK = creerImage("images/brick.png", (BRICK_LARGEUR, BRICK_HAUTEUR))
IMAGE_BROKENABLE_BRICK = creerImage("images/brokenable.wall.png", (BRICK_LARGEUR, BRICK_HAUTEUR))
IMAGE_BROKEN_BRICK = creerImage("images/broken.wall.png", (BRICK_LARGEUR, BRICK_HAUTEUR))

IMAGE_SCENE = creerImage("images/trees-7191822_1280.png", (FENETRE_LARGEUR, FENETRE_HAUTEUR))
IMAGE_PIECE = creerImage("images/piece.png", (PIECE_LARGEUR, PIECE_HAUTEUR))
IMAGE_VIE = creerImage("images/receive.png", (PIECE_LARGEUR, PIECE_HAUTEUR))

IMAGE_PIECE_TABLEAU_DE_BORD = creerImage("images/piece.png", (IMAGE_TABLEAU_DE_BORD_LARGEUR, IMAGE_TABLEAU_DE_BORD_HAUTEUR))
IMAGE_VIE_TABLEAU_DE_BORD = creerImage("images/heart.png", (IMAGE_TABLEAU_DE_BORD_LARGEUR, IMAGE_TABLEAU_DE_BORD_HAUTEUR))
IMAGE_BALLE_TABLEAU_DE_BORD = creerImage("images/ball/ball.0.png", (IMAGE_TABLEAU_DE_BORD_LARGEUR, IMAGE_TABLEAU_DE_BORD_HAUTEUR))

IMAGES_BALLE = []
for img_id in range(0, 360, 15):
    IMAGES_BALLE.append(creerBalleImage("images/ball/ball.{0}.png".format(img_id)))

MUSIQUE_JEU = "music/track_1.wav" # chemin vers musique jeu
MUSIQUE_ACCUEIL = "music/track_2.wav"  # chemin vers musique accueil
MUSIQUE_GAMEOVER = "music/track_3.wav" # chemin vers musique gameover

SON_PIECE = creer_son("music/piece.wav", 0.3) # musique
SON_SAUT = creer_son("music/jump.wav", 0.5) # musique
SON_COLLISION_SOL = creer_son("music/sol.wav", 0.8) # musique
SON_COLLISION_BRIQUE = creer_son("music/brick_col.wav", 0.8) # musique
SON_COLLISION_EAU = creer_son("music/splash.wav", 0.8) # musique
SON_BRIQUE_CASSE = creer_son("music/brick_break.wav", 0.8) # musique
SON_ERREUR = creer_son("music/erreur.wav", 1) # musique

scene = None #Va contenir la scene de chaque écran
horloge = pygame.time.Clock()
police_tableau_de_bord = pygame.font.SysFont("ubuntu", TABLEAU_DE_BORD_TAILLE_POLICE, True)
police_fade_screen = pygame.font.SysFont("ubuntu", FADE_SCREEN_TAILLE_POLICE)
police_ecran_de_jeu = pygame.font.SysFont("ubuntu", ECRAN_DE_JEUX_POLICE_TAILLE, True)
police_ecran_de_niveau = pygame.font.SysFont("ubuntu", ECRAN_SELECTION_NIVEAU_POLICE_TAILLE, True)

initialiserEcranAccueil()
initialiserMusique()

while not estFini(scene):
    maintenant = pygame.time.get_ticks()
    traite_entrees(maintenant)
    
    if ecranActuel(scene) == ECRAN_DE_JEUX:
        afficherEcranDeJeu(maintenant)
        
    elif ecranActuel(scene) == ECRAN_ACCUEIL:
        afficherEcranAccueil(maintenant)
        
    elif ecranActuel(scene) == ECRAN_SELECTION_NIVEAU:
        afficherEcranNiveau(maintenant)
        
    modifierTempsDepartScene(scene, maintenant)
    
    pygame.display.flip()
    horloge.tick(IMAGES_PAR_SECONDE)
    

pygame.display.quit()
pygame.quit()
exit()
