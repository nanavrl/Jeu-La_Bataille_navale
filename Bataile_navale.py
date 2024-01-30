'''
JEU DE LA BATAILLE NAVALE

1 JOUEUR MAX ET PLACEMENT DES BATEAUX ALEATOIRE

'''

# Importation des bibliothèques nécessaires

import pygame  # Bibliothèque pour la création de jeux en Python
import random  # Module pour la génération de nombres aléatoires

# Initialisation de Pygame

pygame.init()

# Définition des dimensions de l'écran

LARGEUR, HAUTEUR = 500, 500
ECRAN = pygame.display.set_mode((LARGEUR, HAUTEUR))  # Création de la fenêtre de jeu
pygame.display.set_caption('Bataille Navale')  # Titre de la fenêtre

# Définition des couleurs utilisées dans le jeu

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 153, 153)

# Définition de la taille des cases et du nombre de cases dans la grille

TAILLE_CASE = 80
NB_CASES = 5

# Définition de la classe pour les bateaux

class Bateau:
    def __init__(self, taille):
        self.taille = taille  # Taille du bateau
        self.position = []  # Liste des positions du bateau sur la grille
        self.base_position = []

# Définition de la classe pour la grille

class Grille:
    def __init__(self, x, y, couleur):
        self.x = x  # Position en X de la grille
        self.y = y  # Position en Y de la grille
        self.couleur = couleur  # Couleur des cases de la grille
        self.grille = [[0] * NB_CASES for i in range(NB_CASES)]  # Initialisation de la grille vide

    def afficher(self):
        # Boucle pour dessiner les cases de la grille
        for i in range(NB_CASES):
            for j in range(NB_CASES):
                # Dessiner une case avec un contour
                pygame.draw.rect(ECRAN, self.couleur, (self.x + j * TAILLE_CASE, self.y + i * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 1)

                # Vérification de l'état de la case et dessin des formes en conséquence
                if self.grille[i][j] == 3:  # Affiche une croix pour coulé
                    pygame.draw.line(ECRAN, (255, 102, 102), (self.x + j * TAILLE_CASE, self.y + i * TAILLE_CASE), (self.x + j * TAILLE_CASE + TAILLE_CASE, self.y + i * TAILLE_CASE + TAILLE_CASE), 3)
                    pygame.draw.line(ECRAN, (255, 102, 102), (self.x + j * TAILLE_CASE + TAILLE_CASE, self.y + i * TAILLE_CASE), (self.x + j * TAILLE_CASE, self.y + i * TAILLE_CASE + TAILLE_CASE), 3)
                if self.grille[i][j] == 2:  # Affiche un rond pour touché
                    pygame.draw.circle(ECRAN, (255, 153, 153), (self.x + j * TAILLE_CASE + TAILLE_CASE // 2, self.y + i * TAILLE_CASE + TAILLE_CASE // 2), TAILLE_CASE // 4)
                elif self.grille[i][j] == 4:  # Affiche une croix pour manqué
                    pygame.draw.line(ECRAN, (255, 255, 255), (self.x + j * TAILLE_CASE, self.y + i * TAILLE_CASE), (self.x + j * TAILLE_CASE + TAILLE_CASE, self.y + i * TAILLE_CASE + TAILLE_CASE), 3)
                    pygame.draw.line(ECRAN, (255, 255, 255), (self.x + j * TAILLE_CASE + TAILLE_CASE, self.y + i * TAILLE_CASE), (self.x + j * TAILLE_CASE, self.y + i * TAILLE_CASE + TAILLE_CASE), 3)

    def tirer(self, x, y):
        # Fonction pour tirer sur une case donnée
        if self.grille[y][x] == 1:  # Vérification si un bateau est présent dans la case
            self.grille[y][x] = 2  # 2 représente un tir réussi
            return True  # Renvoie True si le tir a touché un bateau
        else:
            self.grille[y][x] = 4  # 4 représente un tir manqué
            return False  # Renvoie False si le tir a manqué

    def verifier_couler(self, x, y, bateaux):
        # Vérification si un bateau a été coulé
        for bateau in bateaux:
            if (x, y) in bateau.position:  # Vérification si la position est présente dans les positions du bateau
                bateau.position.remove((x, y))  # Retire la position du bateau
                if not bateau.position:  # Vérification si toutes les positions du bateau ont été touchées
                    print("Coulé!")  # Affichage du message si le bateau est coulé
                    for pos in bateau.base_position:
                        self.grille[pos[1]][pos[0]] = 3 #toute les enciennes pose en coulée
                    if all(not bateau.position for bateau in bateaux):  # Vérification si tous les bateaux ont été coulés
                        print("Bravo, vous avez gagné !")  # Affichage du message de victoire
                        pygame.quit()  # Fermeture de Pygame
                        return True  # Renvoie True si le joueur a gagné

# Fonction pour le placement aléatoire des bateaux
def placer_bateaux(grille, bateaux): 
    # Boucle pour placer les bateaux
    for bateau in bateaux:
        bateau_horizontal = random.choice([True, False])  # Sélection aléatoire de l'orientation du bateau
        if bateau_horizontal:  # Vérification si le bateau est orienté horizontalement
            x = random.randint(0, NB_CASES - bateau.taille)  # Position aléatoire en X pour le bateau
            y = random.randint(0, NB_CASES - 1)  # Position aléatoire en Y pour le bateau
            for i in range(bateau.taille):
                grille.grille[y][x + i] = 1  # Positionne le bateau sur la grille
                bateau.position.append((x + i, y))  # Ajoute la position du bateau
        else:  # Le bateau est orienté verticalement
            x = random.randint(0, NB_CASES - 1)  # Position aléatoire en X pour le bateau
            y = random.randint(0, NB_CASES - bateau.taille)  # Position aléatoire en Y pour le bateau
            for i in range(bateau.taille):
                grille.grille[y + i][x] = 1  # Positionne le bateau sur la grille
                bateau.position.append((x, y + i))  # Ajoute la position du bateau
        bateau.base_position = bateau.position.copy()

# Fonction principale du jeu
def jeu_bataille_navale():
    # Initialisation des variables
    continuer = True  # Variable pour contrôler la boucle principale
    clock = pygame.time.Clock()  # Horloge pour contrôler le taux de rafraîchissement de l'écran

    # Création de la grille du joueur
    grille = Grille(50, 50,BLANC)

    # Initialisation des bateaux du joueur
    bateaux = [Bateau(1), Bateau(2), Bateau(3)]

    # Placement initial aléatoire des bateaux
    placer_bateaux(grille, bateaux)

    # Boucle principale
    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Vérification si l'utilisateur a fermé la fenêtre
                continuer = False  # Arrête la boucle principale
            ECRAN.fill(BLEU)  # Remplissage de l'écran avec la couleur noire
            # Interaction avec la grille
            if event.type == pygame.MOUSEBUTTONDOWN:  # Vérification si l'utilisateur a cliqué
                if event.button == 1:  # Vérification si le clic était le bouton gauche de la souris
                    x, y = event.pos  # Récupération des coordonnées du clic
                    if 50 <= x < 50 + NB_CASES * TAILLE_CASE and 50 <= y < 50 + NB_CASES * TAILLE_CASE:  # Vérification si le clic est à l'intérieur de la grille
                        x = (x - 50) // TAILLE_CASE  # Conversion de la position en X
                        y = (y - 50) // TAILLE_CASE  # Conversion de la position en Y
                        print(x+1, y+1)
                        if grille.tirer(x, y):  # Vérification si le tir a touché un bateau
                            print("Touché!")  # Affichage d'un message si le tir a touché
                            grille.verifier_couler(x, y, bateaux)  # Vérification si un bateau a été coulé
                        else:
                            print("Manqué!")  # Affichage d'un message si le tir a manqué

        # Affichage de la grille
        grille.afficher()  # Affichage de la grille

        pygame.display.flip()  # Mise à jour de l'écran
        clock.tick(60)  # Limite le taux de rafraîchissement à 60 images par seconde

    pygame.quit()  # Fermeture de Pygame

# Lancement du jeu
jeu_bataille_navale()  # Appel de la fonction pour commencer le jeu

