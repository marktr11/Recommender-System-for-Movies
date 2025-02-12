import numpy as np
import pandas as pd
def data():
    #importer les données
    file_path = 'ratings.csv'
    data = pd.read_csv(file_path)

    #Création d'un tableau croisé dynamique
    movie_Y = data.pivot(index='movieID', columns='userID', values='rating')
    movie_Y= movie_Y.fillna(0)

    movie_R=movie_Y
    movie_R=(movie_R > 0).astype(int)

    Y = movie_Y.to_numpy()
    R = movie_R.to_numpy()
    return Y,R