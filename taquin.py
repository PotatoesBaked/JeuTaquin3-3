import queue
import copy
import time
import random


class etat:
    """
    Attribut :
    - matrice 3x3 => jeux
    - chemin => mouvement effectué depuis l'état initiale
    - fonction devaluation => calcul f(E)
    - taille cote matrice => val n de la matrice N*N
    - heuristique
    - trou
    """

    def __init__(self, matrice, chaine_de_deplacement, k, taille_cote_matrice, trou):
      self.matrice = matrice
      self.chemin = chaine_de_deplacement
      self.heuristique = k
      self.taille_cote_matrice = taille_cote_matrice
      self.fonction_devaluation = self.get_taille_chemin() + self.get_heuristique(k)
      self.trou = trou

    def get_taille_chemin(self):
       return len(self.chemin)

    def get_heuristique(self, k):
      val = 0
      poid_de_la_tuile = poid_par_tuile(k)
      coeff_normalisation = get_coeff_normalisation(k)

      #calcul grâce à la formule donnée
      for i in range((self.taille_cote_matrice * self.taille_cote_matrice)-1):
         distance_elem = distance_elementaire(self.matrice, i, self.taille_cote_matrice)
         if distance_elem is not None:
            val += poid_de_la_tuile[i] * distance_elem
         else:
            break

      return val//coeff_normalisation

    def calcul_fonction_devaluation(self):
       self.fonction_devaluation = self.get_taille_chemin() + self.get_heuristique(self.heuristique)

    #comparateur pour la priorityQueue en fonction de la fonction d'evaluation
    def __lt__(self, autre):
       return self.fonction_devaluation < autre.fonction_devaluation




def get_coeff_normalisation(k):
   if k == 1 or k == 3 or k == 5:
      return 4
   else :
      return 1

def poid_par_tuile(k):
      if k == 1:
         return [36,12,12,4,1,1,4,1,0]
      elif k == 2:
         return [8,7,6,5,4,3,2,1,0]
      elif k == 3:
         return [8,7,6,5,4,3,2,1,0]
      elif k == 4:
         return [8,7,6,5,3,2,4,1,0]
      elif k == 5:
         return [8,7,6,5,3,2,4,1,0]
      elif k == 6:
         return [1,1,1,1,1,1,1,1,0]

"""
distance_elementaire calcul la distance elementaire et si get_position_i et get_position_final_i ne retourne pas de résultat, on renvoie rien
"""
def distance_elementaire(matrice,i,n):
   erreur_1 = get_position_i(matrice, i, n)
   erreur_2 = get_position_final_i(n,i)

   if erreur_1 is not None:
      xa,ya = erreur_1
      xb,yb = erreur_2
      return abs(xb - xa) + abs(yb - ya)

   return None



"""
parcours la matrice pour trouver la position de i et renvoie ses coordonnées
"""
def get_position_i(matrice, i, n):
   for x in range(n):
      for y in range(n):
         if matrice[x][y] == i:
            return x,y
   return None


"""
i//y et i%n est une formule pour convertir un indice linéaire en paire d'indice dans une matrice à 2 dimensions de côte n
"""

def get_position_final_i(n, i):
   x,y = i // n, i % n
   return x,y

"""
La fonction Deplacement vérifie que le mouvement demandé est réalisable selon les règles du jeu et interverti les valeurs
de la case actuelle du trou et celle sur laquelle il sera après déplacement
"""

def Deplacement (etat,mouv):
    valide = False
    res = copy.deepcopy(etat)
    trou = etat.trou
    pos = get_position_i(etat.matrice,trou,3)
    if (mouv == 'N'):
        if(pos[0]!=0):
            res.matrice[pos[0]][pos[1]] = res.matrice[pos[0]-1][pos[1]]
            res.matrice[pos[0]-1][pos[1]] = trou
            valide = True

    elif(mouv == 'S'):
        if(pos[0]!=2):
             res.matrice[pos[0]][pos[1]] = res.matrice[pos[0]+1][pos[1]]
             res.matrice[pos[0]+1][pos[1]] = trou
             valide = True

    elif(mouv == 'E'):
        if(pos[1]!=2):
            res.matrice[pos[0]][pos[1]] = res.matrice[pos[0]][(pos[1]+1)]
            res.matrice[pos[0]][pos[1]+1] = trou
            valide = True

    elif(mouv =='O'):
        if(pos[1]!=0):
             res.matrice[pos[0]][pos[1]] = res.matrice[pos[0]][pos[1]-1]
             res.matrice[pos[0]][pos[1]-1] = trou
             valide = True
    if valide:
        #reactualisation du chemin effectué et de la nouvelle valeur de la fonction d 'évaluation
        res.chemin = res.chemin + mouv
        res.calcul_fonction_devaluation()
        return res

    return None

"""
Les fonctions Soluble et Permutation  permettent de déterminer à l'avance si le taquin en paramètre a une solution ou pas
Pour ça elles s'appuient sur l'affirmation qui dit que un taquin a une solution si et seulement si
la parité de la distance entre la position actuelle et la position finale du trou est égale à la parité
du nombre de permutations qu'il faut faire pour atteindre l'état final
"""
def Soluble (matrice):
    m = copy.deepcopy(matrice)
    n = len(matrice)
    valide = False
    a = get_position_i(m,'X',n)
    parite_trou = ((n-1-a[0])+(n-1-a[1]))%2
    liste=[]
    for i in range(n):
        for j in range(n):
            if(m[i][j]=='X'):
                m[i][j]=n*n-1
            liste.append(m[i][j])
    parite_permutation = Permutation(liste)%2
    if(parite_trou == parite_permutation):
        valide = True
    return valide

def Permutation(liste):
    temp=0
    compteur=0
    i=0
    while i<len(liste):
        if(liste[i]!=i):
            compteur = compteur+1
            temp = liste[i]
            liste[i]=liste[temp]
            liste[temp]=temp
        else : i=i+1
    return compteur


def A_star(start, end):
   #priorityqueue est une file qui trie en fonction d'un critère
   frontiere = queue.PriorityQueue()
   etat_visite = []
   parent = {}
   frontiere.put(start)
   #dictionnaire pour éviter de faire des chemins inverse on donne l'opposé du mouvement
   chemin_inverse = {'N':'S', 'S':'N','E':'O','O':'E'}
   retour_en_arriere = None

   while not frontiere.empty():
      etat = frontiere.get()

      if etat.matrice == end:
         tab = getTableauFinal(parent, etat, [etat])
         #on inverse le tableau
         tab = tab[::-1]
         fin = printTab(tab)
         print("Nombre d'état visité : ", len(etat_visite))
         print("Nombre d'état restant dans la frontière : ", frontiere.qsize())
         return fin

      #si on a déjà effectué un mouvement prend le dernier mouvement et verifie qu'on fasse pas de marche arrière si oui on skip la génération de l'enfant
      if len(etat.chemin) > 0 :
         retour_en_arriere = chemin_inverse[etat.chemin[-1]]
      for mouvement in ['S','N','O','E']:
         if retour_en_arriere == mouvement and retour_en_arriere is not None:
            continue
            
         enfant = Deplacement(etat, mouvement)

         if enfant is not None :
            parent[enfant] = etat
            frontiere.put(enfant)


      etat_visite.append(etat)

   #aucune solution
   return False

"""
getTableauFinal on fait une récursion où on prend le dictionnaire avec les enfants et ses parents. On démarre d'un enfant, on a son père et repete la même fonction sur le père
"""
def getTableauFinal(dictionnaire, etat, tab):
   if etat in dictionnaire:
      parent = dictionnaire[etat]
      tab.append(parent)
      getTableauFinal(dictionnaire, parent, tab)

   return tab

#print tout les éléments d'un tableau
def printTab(tab):
   for i in tab:
      print(i.matrice)
   print("Nombre d'étape :" ,len(tab))
   return True

#genere l'etat final en fonction de n
def generationEtatFinal(n, trou):
   matrice = []
   i = 0

   for x in range(n):
      sous_tab = []
      for y in range(n):
         if x == n-1 and y == n-1:
            sous_tab.append(trou)
         else:
            sous_tab.append(i)
            i += 1
      matrice.append(sous_tab)
   return matrice

#crée un plateau de jeu taquin
def generationPlateau(n,trou):
   matrice = []

   #crée une liste de 0 à (n*n)-1 + le trou et on le mélange
   liste_val_possible = list(range(n*n-1))
   liste_val_possible.append(trou)
   random.shuffle(liste_val_possible)

   for x in range(n):
      sous_tab = []
      for y in range(n):
         sous_tab.append(liste_val_possible.pop())
      matrice.append(sous_tab)
        
   return matrice

 

def main():
   start_time = time.time()

   trou = 'X'
   taille_cote = 3
   matrice = generationPlateau(taille_cote, trou)
   chemin = ''
   heuristique = random.randint(1,6)
   
   
   etat_initial = etat(matrice,chemin, heuristique,taille_cote,trou)
   etat_final = generationEtatFinal(taille_cote, trou)
  

   
   if(Soluble(etat_initial.matrice)):
        A_star(etat_initial,etat_final)
   else:
      print("Il y a aucune solution pour la matrice :")
      print(etat_initial.matrice)

   end_time = time.time()
   elapsed_time = end_time - start_time
   print("Temps d'éxecution : ", elapsed_time, "secondes")
   print("Heuristique utilisé :", heuristique)
   

main()
