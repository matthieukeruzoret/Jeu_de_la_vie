import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Initialisation de la grille avec des cellules vivantes placées aléatoirement
def init_jeu(N):
    grille = np.zeros((N, N))
    nb_cellule_vivante = random.randint(700,800)  # Nombre aléatoire de cellules vivantes
    positions = random.sample([(x, y) for x in range(N) for y in range(N)], nb_cellule_vivante) # Générer des positions uniques pour éviter les doublons
    for x, y in positions:
        grille[x, y] = 1  # Place une cellule vivante
    return grille

# Fonction pour compter les voisins vivants d'une cellule
def compter_voisins(grille, i, j):
    nb_voisins = 0
    N = len(grille)  # Taille de la grille
    for x in range(i - 1, i + 2):  # Parcourt de i-1 à i+1
        for y in range(j - 1, j + 2):  # Parcourt de j-1 à j+1
            if 0 <= x < N and 0 <= y < N and (x != i or y != j):
                if grille[x, y] == 1:
                    nb_voisins += 1
    return nb_voisins

# Fonction qui met à jour l'état de la grille pour une seule itération
def iterer_jeu(grille):
    N = len(grille)
    nouvelle_grille = grille.copy()  # Copie de la grille actuelle
    for i in range(N):
        for j in range(N):
            nb_voisins = compter_voisins(grille, i, j)
            if grille[i, j] == 1:  # Cellule vivante
                if nb_voisins < 2 or nb_voisins > 3:
                    nouvelle_grille[i, j] = 0  # Meurt par sous/surpopulation
            else:  # Cellule morte
                if nb_voisins == 3:
                    nouvelle_grille[i, j] = 1  # Naît par reproduction
    grille[:] = nouvelle_grille  # Mise à jour effective de la grille en place

# Fonction pour compter la population actuelle
def compter_population(grille):
    return np.sum(grille)  # Compte les cellules vivantes (valeurs à 1)

# Affichage de la grille avec animation
N = 80  # Taille de la grille 80x80
G = init_jeu(N)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))  # Deux sous-graphes

# ---- Affichage de la grille ----
ax1.set_xticks([])
ax1.set_yticks([])
img = ax1.imshow(G, cmap='gray_r')  # Affichage initial
ax1.set_title("Jeu de la Vie - Évolution")

# ---- Affichage du graphe de population ----
population = [compter_population(G)]  # Liste pour stocker la population
ax2.set_xlim(0, 1000)  # Limite en X (110 générations)
ax2.set_ylim(0, N * N)  # Limite en Y (max possible = 80x80)
ax2.set_title("Évolution de la Population")
ax2.set_xlabel("Générations")
ax2.set_ylabel("Nombre de cellules vivantes")
(line,) = ax2.plot([], [], 'b-', label="Population vivante")  # Ligne du graphe
ax2.legend()

# Ajout du compteur de générations
generation = [0]  # Utilisation d'une liste pour que la valeur soit mutable
text = ax1.text(0, 83, f"Génération: {generation[0]}", color="black", fontsize=12, fontweight='bold')

# Fonction d'animation pour mettre à jour l'affichage et le graphe
def animate(frame):
    if generation[0] >= 1000:
        ani.event_source.stop()  # Stoppe l'animation après 110 générations
        plt.pause(0.1)  # Petite pause pour éviter un arrêt brusque
        return

    iterer_jeu(G)  # Met à jour la grille
    img.set_array(G)  # Met à jour l'image

    # Mise à jour du compteur de génération
    generation[0] += 1
    text.set_text(f"Génération: {generation[0]}")

    # Mise à jour du graphe de population
    population.append(compter_population(G))  # Ajoute la population actuelle
    line.set_data(range(len(population)), population)  # Mise à jour des données

    ax2.set_xlim(0, max(1000, len(population)))  # Ajuste X si besoin
    ax2.set_ylim(0, max(population) + 50)  # Ajuste Y pour voir toute la courbe

# Création de l'animation
ani = FuncAnimation(fig, animate, frames=1000, interval=100)
plt.show()