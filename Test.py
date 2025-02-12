# Parcourir chaque utilisateur existant (incluant le nouvel utilisateur)
    for utilisateur_index in range(nb_utilisateurs): # Maintenant cela fonctionne avec un utilisateur supplémentaire
        for film_index,film_id in enumerate(film_ratings):
            # Khi thêm người dùng mới vào cột đầu tiên, chúng ta cần xử lý chỉ số cột đúng cách
        # Vérifiez si l'utilisateur a donné une évaluation pour ce film
            if utilisateur_index == 0:  # Xử lý người dùng mới ở cột đầu tiên
               if Y[film_index, utilisateur_index] != 0:
                  utilisateur_ratings[nb_utilisateurs].append(Y[film_index, utilisateur_index])
                  film_ratings[film_id].append(Y[film_index, utilisateur_index])
            # Si une évaluation existe, mettre à jour le dictionnaire
            # Lorsque vous ajoutez un nouvel utilisateur avec l'index 0, tous les anciens utilisateurs seront déplacés d'une colonne dans le dictionnaire. Cela signifie que les indices des utilisateurs existants seront ajustés pour libérer la colonne 0 pour le nouvel utilisateur. C'est pourquoi on doit mettre à jour le dictionnaire
            else:
                if Y[film_index, utilisateur_index] != 0:  # f est l'index, film_id est la clé du dictionnaire film_ratings
                   utilisateur_ratings[utilisateur_index].append(Y[film_index, utilisateur_index]) # Les ID commencent à 1, donc le nouvel utilisateur occupera ID1.
                   film_ratings[film_id].append(Y[film_index, utilisateur_index])