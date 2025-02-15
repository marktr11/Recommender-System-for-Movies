import numpy as np
import pandas as pd

def matrix_covariance(matrix):
    """
    Calcule la matrice de covariance normalisée d'une matrice donnée.

    Paramètres :
    - matrix (numpy.ndarray) : Une matrice 2D (nb de films, nb d'utlisateur) contenant les données.

    Retourne :
    - numpy.ndarray : La matrice de covariance normalisée (nb d'utlisateur, nb d'utlisateur).
    """

    # Normalisation des colonnes de la matrice :
    # - np.mean(matrix, axis=0) : Calcule la moyenne de chaque colonne (chaque utilisateur).
    # - np.std(matrix, axis=0, ddof=1) : Calcule l'écart-type de chaque colonne.
    # - ddof=1 pour obtenir un estimateur sans biais de l'écart-type,
    # ce qui signifie qu'on divise par (N-1) au lieu de N .
    matrix_normalized = (matrix - np.mean(matrix, axis=0)) / np.std(matrix, axis=0, ddof=1) 

    # Calcul de la matrice de covariance :
    # - rowvar=False : chaque colonne est considérée comme une variable
    # (chaque ligne est une observation).
    matrix_cov = np.cov(matrix_normalized, rowvar=False) 

    return matrix_cov

def eigen(matrix):
    """
    Calcule les valeurs propres (eigenvalues) et les vecteurs propres (eigenvectors) 
    d'une matrice donnée et les trie en ordre décroissant.

    Paramètres :
    - matrix (numpy.ndarray) : Une matrice carrée dont on veut extraire 
      les valeurs et vecteurs propres.
    Retourne :
    - eigenvalues (numpy.ndarray) : Un tableau 1D contenant les valeurs propres triées par ordre décroissant.
    - eigenvectors (numpy.ndarray) : Une matrice contenant les vecteurs propres correspondants (colonnes).
    """

    # Calcul des valeurs propres et des vecteurs propres :
    eigenvalues, eigenvectors = np.linalg.eig(matrix)

    # np.argsort(eigenvalues) renvoie les indices qui trieraient eigenvalues en ordre croissant.
    # [::-1] permet d'inverser l'ordre pour obtenir un tri décroissant.
    sorted_indices = np.argsort(eigenvalues)[::-1]

    eigenvalues = eigenvalues[sorted_indices]  # Trie les valeurs propres.
    eigenvectors = eigenvectors[:, sorted_indices]  # Trie les vecteurs propres en conséquence.

    return eigenvalues, eigenvectors


import numpy as np

def cumulative_explained_variance(eigenvalues, normalized=False):
    """
    Calcule la variance expliquée cumulée à partir des valeurs propres ou des ratios de variance expliquée.

    Paramètres :
    - eigenvalues (array-like) : Liste des valeurs propres ou des ratios de variance expliquée.
    - normalized (bool) : Si True, indique que les valeurs dans 'eigenvalues' sont déjà normalisées (somme = 1).
                          Par défaut False, ce qui signifie que les valeurs propres brutes sont fournies.

    Retourne :
    - cumulative_variance (numpy.ndarray) : Tableau contenant la variance expliquée cumulée.
    - explained_variance_ratio (numpy.ndarray) : Ratios de variance expliquée individuels.
    """

    eigenvalues = np.array(eigenvalues)  # Conversion en tableau NumPy

    # Si les valeurs propres ne sont pas normalisées, on les normalise pour obtenir le ratio de variance expliquée
    if not normalized:
        total_variance = np.sum(eigenvalues)  # Somme des valeurs propres
        explained_variance_ratio = eigenvalues / total_variance  # Ratio de variance expliquée
    else:
        explained_variance_ratio = eigenvalues  # Si déjà normalisées, on les utilise 

    # Vérifier si la somme des ratios est bien égale à 1 (normalisation correcte)
    if abs(sum(explained_variance_ratio) - 1) < 1e-6:  
       print("Les valeurs propres ont été normalisées")

    # la variance expliquée cumulée
    cumulative_variance = np.cumsum(explained_variance_ratio)  

    return cumulative_variance, explained_variance_ratio


    