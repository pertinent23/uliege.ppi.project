import pygame

BLEU_CIEL = (135, 206, 255)
 
FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

SOL_HAUTEUR = 500

X = 0
Y = 1


def traite_entrees() :
   global fini
   for evenement in pygame.event.get():
      if evenement.type == pygame.QUIT:
         fini = True
      if evenement.type == pygame.KEYDOWN:
         if evenement.key == pygame.K_UP:
            saute(Obj)

def affiche_objet(fenetre, objet):
   pygame.draw.circle(fenetre, (255,0,0), objet['pos'], objet['rad'])

def newPos(objet):
   global temps_precedent
   delai = temps_maintenant - temps_precedent
   
   objet['vit'][X] = objet['vit'][X] + objet['acc'][X] * delai
   objet['vit'][Y] = objet['vit'][Y] + objet['acc'][Y] * delai

   objet['pos'][X] = int(objet['pos'][X] + objet['vit'][X] * delai)
   objet['pos'][Y] = int(objet['pos'][Y] + objet['vit'][Y] * delai)
 
   temps_precedent = temps_maintenant

   if objet['pos'][Y] + objet['rad'] > SOL_HAUTEUR :
      objet['pos'][Y] = SOL_HAUTEUR - objet['rad']
      objet['vit'][Y] = 0

   if objet['pos'][X] > FENETRE_LARGEUR :
      objet['pos'][X] = 0
   elif objet['pos'][X] < 0 :
      objet['pos'][X] = FENETRE_LARGEUR

Obj = {'pos':[400,300], 'vit':[0,0], 'acc':[0,0.001], 'rad':25}

def saute(objet):
   if objet['pos'][Y] == SOL_HAUTEUR - objet['rad']:
      Obj['vit'][Y] = -0.5


pygame.init()

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)
pygame.display.set_caption('Jeu')

fini = False
temps = pygame.time.Clock()
temps_precedent = 0

while not fini:
   traite_entrees()
 
   fenetre.fill(BLEU_CIEL)
   pygame.draw.line(fenetre, (0,0,0), (0, SOL_HAUTEUR), (FENETRE_LARGEUR, SOL_HAUTEUR))

   temps_maintenant = pygame.time.get_ticks()

   affiche_objet(fenetre, Obj)
   newPos(Obj)

   pygame.display.flip()

   temps.tick(50)

pygame.display.quit()
pygame.quit()
exit()
