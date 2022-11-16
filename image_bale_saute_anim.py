import pygame

BLEU_CIEL = (135, 206, 250)

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

BALE_LARGEUR = 60
BALE_HAUTEUR = 51


SOL_HAUTEUR = 500

X = 0
Y = 1


pygame.init()

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('BALE')

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

##### Définition ENTITE #####

def nouvelleEntite():
    return {
        'visible':False,
        'position': [0, 0],
        'vitesse':[0,0],
        'acceleration':[0,0],
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


def ajoutePose(entite, nom, image):
    entite['poses'][nom] = image


def prendsPose(entite, pose):
    entite['imageAffichee'] = entite['poses'][pose]
    visible(entite)

def dessine(entite, ecran):
    ecran.blit(entite['imageAffichee'], entite['position'])

 


def traite_entrees() :
   global fini
   for evenement in pygame.event.get():
      if evenement.type == pygame.QUIT:
         fini = True
      if evenement.type == pygame.KEYDOWN:
         if evenement.key == pygame.K_UP:
            saute(bale)

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

##### Fin ENTITE #####

def affiche(entites, ecran):
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


def miseAJour(scene):
    maintenant = pygame.time.get_ticks()
    for objet in scene:
        deplace(objet, maintenant)

def newPos(objet):
   global temps_precedent, fini
   delai = temps_maintenant - temps_precedent
   
   set_vitesse(objet, objet['vitesse'][X] + objet['acceleration'][X] * delai,objet['vitesse'][Y] + objet['acceleration'][Y] * delai)
   

   place(objet,int(objet['position'][X] + objet['vitesse'][X] * delai),  int(objet['position'][Y] + objet['vitesse'][Y] * delai))
   
 
   temps_precedent = temps_maintenant
   
   
#    if objet['pos'][Y] + objet['rad'] > LIMITE_MORT :
#       fini = True
   if objet['position'][Y] + BALE_HAUTEUR > SOL_HAUTEUR :
      objet['position'][Y]= SOL_HAUTEUR - BALE_HAUTEUR
      objet['vitesse'][Y]=0
      

   if objet['position'][X] > FENETRE_LARGEUR :
      objet['position'][X] = 0
   elif objet['position'][X] < 0 :
      objet['position'][X] = FENETRE_LARGEUR




def saute(objet):
   if objet['position'][Y] == SOL_HAUTEUR - BALE_HAUTEUR:
      set_vitesse(objet,0,-0.5)



bale = nouvelleEntite()
set_acceleration(bale,0,0.001)
place(bale,400,300)

for nom_image, nom_fichier in (('BALE_1','ball.png'),
                               ('BALE_2','ball_30.png'),
                               ('BALE_3','ball_60.png'),
                               ('BALE_4','ball_90.png')):
    chemin = 'images/' + nom_fichier
    image = pygame.image.load(chemin).convert_alpha(fenetre)
    image = pygame.transform.scale(image, (BALE_LARGEUR, BALE_HAUTEUR))
    ajoutePose(bale, nom_image, image)


animation = nouvelleAnimation()
ajouteMouvement(animation, mouvement('BALE_1', 80))
ajouteMouvement(animation, mouvement('BALE_2', 80))
ajouteMouvement(animation, mouvement('BALE_3', 80))
ajouteMouvement(animation, mouvement('BALE_4', 80))

                              

ajouteAnimation(bale, 'roule', animation)

scene = [bale]
commenceAnimation(bale, 'roule', 0)


fini = False
temps = pygame.time.Clock()

temps_precedent = 0
while not fini:


    traite_entrees()
    
    miseAJour(scene)

    fenetre.fill(BLEU_CIEL)

    temps_maintenant = pygame.time.get_ticks()

    affiche(scene, fenetre)
    newPos(bale)
    

    pygame.display.flip()

    temps.tick(100)

pygame.display.quit()
pygame.quit()
exit()