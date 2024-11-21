x = 4
c = 0
flag_list = []

# Où est mon fichier?
file_path = '/Users/ayoubrayaneaitallaoua/Documents/ProjetSyst/mapping.sam'

# ouvrir le fichier en lecture 'r' sous le nom file
with open(file_path, 'r') as file:
    #pour chaque ligne dans mon fichier
    for line in file:
        c += 1

        # ignorer les headers
        if line.startswith('@'):
            continue

        # Diviser les colonnes en utilisant \t
        columns = line.split('\t')
        # extraire le nom + colonne
        name_value = columns[0]
        flag_value = columns[1]
        #test si les flags contiennet PAS 1 sur le digit 4 donc read n'est pas 'read unmapped' en utilisant l'operation binaire &
        if int(flag_value) & x == 0:
            #rajoute chacune des valeurs dans la liste des flags
            flag_list.append(flag_value)
#print(flag_list)

#crée un dictionnaire vide
flag_distinct_reps = {}

#pour chaque valeur de flag dans ma liste de tout les flags
for flag in flag_list:

    #si le flag existe déja, prends la valeur précédante + 1
    if flag in flag_distinct_reps:
        flag_distinct_reps[flag] = flag_distinct_reps[flag] + 1
    #Sinon tu crée la clé avec le flag et tu l'initialise à 1
    else:
        flag_distinct_reps[flag] = 1


#print(flag_distinct_reps)

def divise_chromosome(longueur_chrom: int, taille_interv: int):
    interv_start_dict = {}
    interv_end_dict = {}

    interv_index = 0
    interv_start = 1

    while interv_start < longueur_chrom:
        interv_index += 1
        interv_name = f"Interval_{interv_index}"
        interv_end = interv_start + taille_interv + 1

        while interv_end >= longueur_chrom:
            interv_end = interv_end - 1

        interv_start_dict[interv_name] = interv_start
        interv_end_dict[interv_name] = interv_end

        interv_start = interv_end + 1

    return interv_start_dict, interv_end_dict


start, end = divise_chromosome(1000, 100)

print(start)

def read_interval(file_path: str):
    dict_read_start = {}
    dict_read_end = {}

    with open(file_path, 'r') as file:
        # pour chaque ligne dans mon fichier
        for line in file:
            # ignorer les headers
            if line.startswith('@'):
                continue

            # Diviser les colonnes en utilisant \t
            columns = line.split('\t')

            read_name = columns[0]
            read_start = columns[3]
            dict_read_start[read_name] = read_start

            read_end = read_start + columns[8]
            dict_read_end[read_name] = read_end

    return dict_read_start, dict_read_end

