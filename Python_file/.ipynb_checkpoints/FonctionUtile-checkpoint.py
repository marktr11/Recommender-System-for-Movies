import numpy as np
import pandas as pd
import os

def data_ratings():
    """
    Cette fonction transforme les colonnes du fichier ratings.csv en un tableau croisé.
    Retourne : 
    - la matrice Y : ndarray (nb_films, nb_utilisateurs) qui inclut les notes
    - la matrice R : ndarray (nb_films, nb_utilisateurs) qui inclut 1 si le film a été noté, 0 sinon.
    """
    # Déterminer le chemin absolu vers le fichier ratings.csv
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Dossier Python_file
    file_path = os.path.join(base_dir, "../Data/ratings.csv")  # Aller vers Data
    data = pd.read_csv(file_path)

    #Création d'un tableau croisé dynamique
    movie_Y = data.pivot(index='movieID', columns='userID', values='rating')
    movie_Y= movie_Y.fillna(0)

    # R est basée sur Y et indique la présence d'une évaluation
    movie_R=movie_Y
    movie_R=(movie_R > 0).astype(int)

    Y = movie_Y.to_numpy()
    R = movie_R.to_numpy()
    return Y,R

def normalizeRatings(Y,R):
    """
    Fonction qui permet de calculer la note normalisée.
    Args:
      - Y : ndarray (nb_films, nb_utilisateurs)
      - R : ndarray (nb_films, nb_utilisateurs)
 
    Retourne :
      - Ymean : ndarray (nb_films, ) qui inclut la note moyenne de chaque film
      - Ynorm : ndarray (nb_films, nb_utilisateurs) qui inclut les notes normalisées données par chaque utilisateur pour chaque film
    """

    Ymean = np.zeros((Y.shape[0], 1))  
    Ynorm = np.zeros(Y.shape)
    for i in range(Y.shape[0]):
        Ymean[i]=np.mean(Y[i, R[i, :].astype(bool)])
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            if R[i,j]==1: #normaliser que les valeurs actuelles
               Ynorm[i,j]=Y[i,j]-Ymean[i,0]
    return Ymean,Ynorm

def dict_evaluations():
    """
    Fonction qui crée le dictionnaire stockant les évaluations pour chaque utilisateur et le dictionnaire stockant les évaluations obtenues pour chaque film selon le fichier ratings csv.

    Retourne:
      - dict: utilisateur_ratings.
      - dict: film_ratings.
    """

    # Déterminer le chemin absolu vers le fichier ratings.csv
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Dossier Python_file
    file_path = os.path.join(base_dir, "../Data/ratings.csv")  # Aller vers Data
    data = pd.read_csv(file_path)
    ratings = data.to_numpy()
    

    # Initialiser les dictionnaires pour stocker les évaluations des utilisateurs et des films
    utilisateur_ratings = {}
    film_ratings = {}
    
    # Parcourir chaque ligne du fichier ratings.csv (qui contient utilisateur_id, film_id, note, timestamp)
    for utilisateur_id, film_id, rating, timestamp in ratings:
        # Si l'utilisateur n'existe pas encore dans le dictionnaire, créer une entrée vide
        if utilisateur_id not in utilisateur_ratings:
            utilisateur_ratings[utilisateur_id] = []  # Stocker les évaluations des utilisateurs
        if film_id not in film_ratings:
            film_ratings[film_id] = []  # Stocker toutes les évaluations des films
        utilisateur_ratings[utilisateur_id].append(rating)
        film_ratings[film_id].append(rating)

    return utilisateur_ratings, film_ratings

def update_dict_evaluations(Y, utilisateur_ratings, film_ratings):
    """
    Met à jour les dictionnaires des évaluations des utilisateurs et des films 
    dans le cas où un nouvel utilisateur est ajouté.

    Args:
      - Y (ndarray(nb_films, nb_utilisateurs)): Matrice représentant les évaluations des films 
        par les utilisateurs. Chaque ligne correspond à un film et chaque colonne correspond 
        à un utilisateur.
      - utilisateur_ratings (dict): Dictionnaire où chaque clé est l'ID d'un utilisateur 
        et la valeur est une liste de ses évaluations.
      - film_ratings (dict): Dictionnaire où chaque clé est l'ID d'un film 
        et la valeur est une liste des évaluations reçues pour ce film.

    Retourne:
      - dict: Le dictionnaire mis à jour des évaluations des utilisateurs.
      - dict: Le dictionnaire mis à jour des évaluations des films.

    """
    # ------------------- Partie pour traiter les nouveaux utilisateurs
    
    # Mettre à jour les évaluations en fonction de la matrice Y avec le nouvel utilisateur ajouté
    nb_utilisateurs = Y.shape[1]
    nb_films = Y.shape[0]

    #Initialisez l'espace pour le nouvel utilisateur.
    if nb_utilisateurs not in utilisateur_ratings:
       utilisateur_ratings[nb_utilisateurs] = [] # Préparer une place pour le nouvel utilisateur
        
    # Parcourir chaque utilisateur existant (incluant le nouvel utilisateur)
    for utilisateur_index in range(nb_utilisateurs): # Maintenant cela fonctionne avec un utilisateur supplémentaire
        for film_index,film_id in enumerate(film_ratings):
            # Lorsqu'un nouvel utilisateur est ajouté dans la matrice Y, il sera placé à l'index 0.
            # Nous utilisons la colonne 0 de Y pour l'ajouter au dictionnaire,
            # avec une clé correspondant au nombre total actuel d'utilisateurs (ID du nouvel utilisateur - dans ce cas key = 611).
            if utilisateur_index == 0: 
               if Y[film_index, utilisateur_index] != 0:
                  utilisateur_ratings[nb_utilisateurs].append(Y[film_index, utilisateur_index])
                  film_ratings[film_id].append(Y[film_index, utilisateur_index])
   
    return utilisateur_ratings,film_ratings

def bias_param(Y, utilisateur_ratings, film_ratings):
    """
    Fonction qui calcule le biais pour les utilisateurs et celui pour les films
    """
    # calculer mu en fonction des nouvelles données
    mu = np.mean(Y[Y != 0])  # calculer la moyenne globale
    
    # Calculer b_u et b_f basés sur les nouvelles données
    b_u = {utilisateur_id: np.mean(utilisateur_ratings[utilisateur_id]) - mu for utilisateur_id in utilisateur_ratings.keys()}
    b_f = {film_id: np.mean(film_ratings[film_id]) - mu for film_id in film_ratings.keys()}
    return mu,b_u,b_f

def Biais_matrix(b_f,b_u,mu,Y):
    """
    Fonction qui calcule la matrice biaisée.
    Args:
      - b_u (dict): Biais utilisateur.
      - b_f (dict): Biais film.
      - mu (float): Moyenne globale des évaluations.
      - Y (ndarray): Matrice des évaluations de forme (nb_films, nb_utilisateurs).

    Retourne:
      - B (ndarray): Matrice biaisée de forme (nb_films, nb_utilisateurs).
    """
    
    B = np.zeros(Y.shape)
    nf, nu = Y.shape 
    #calculer les bias
    for j in range(nu):
        utilisateur_id = j+1
        for i, film_id in enumerate(b_f):
            B[i, j] = b_f[film_id] + b_u[utilisateur_id]
    return B

def movies_list():
    """
    Fonction qui lit le fichier 'movies_list.csv' sous forme de dataframe et crée une liste des noms de films.
    Retourne:
      - df (pd.DataFrame): Le dataframe contenant les données du fichier.
      - filmlist (list): La liste des noms de films.
    """
    # Obtenir le chemin absolu du dossier contenant le script (Python_file/)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Construire le chemin vers le fichier Data/movies_list.csv
    file_path = os.path.join(base_dir, "../Data/movies_list.csv")

    df = pd.read_csv(file_path, header=0, index_col=0,  delimiter=',', quotechar='"')
    filmList = df["title"].to_list()
    return filmList,df