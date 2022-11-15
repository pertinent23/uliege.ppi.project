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

##### Définition ENTITE #####

def nouvelleEntite():
    return {
        'visible':False,
        'position': [0, 0],
        'vitesse':[0,0],
        'acceleration':[0,0],
        'imageAffichee':None,
        'poses': []
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


def ajoutePose(entite, image):
    entite['poses'].append(image)


def prendsPose(entite, pose):
    entite['imageAffichee'] = entite['poses'][pose]
    visible(entite)

def dessine(entite, ecran):
    ecran.blit(entite['imageAffichee'], entite['position'])


##### Fin ENTITE #####


    


def traite_entrees() :
   global fini
   for evenement in pygame.event.get():
      if evenement.type == pygame.QUIT:
         fini = True
      if evenement.type == pygame.KEYDOWN:
         if evenement.key == pygame.K_UP:
            saute(bale)



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
chemin = './images/bale.png' 
image = pygame.image.load(chemin).convert_alpha(fenetre)
image = pygame.transform.scale(image, (BALE_LARGEUR, BALE_HAUTEUR))
bale['imageAffichee']=image
fini = False
temps = pygame.time.Clock()

temps_precedent = 0
while not fini:


    traite_entrees()
    

    fenetre.fill(BLEU_CIEL)

    temps_maintenant = pygame.time.get_ticks()

    dessine(bale, fenetre)
    newPos(bale)
    

    pygame.display.flip()

    temps.tick(10)

pygame.display.quit()
pygame.quit()
exit()