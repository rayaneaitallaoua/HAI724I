taille_interval = 100
x = 4
c = 0
flag_list = []
output_file_path = '/Users/ayoubrayaneaitallaoua/Documents/ProjetSyst/results.txt'

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

def divise_chromosome(longueur_chrom: int, taille_interval: int):
    interv_start_dict = {}
    interv_end_dict = {}

    interv_index = 0
    interv_start = 1

    while interv_start < longueur_chrom:
        interv_index += 1
        interv_end = int(interv_start + taille_interval + 1)

        while interv_end >= longueur_chrom:
            interv_end = int(interv_end) - 1

        interv_start_dict[interv_index] = interv_start
        interv_end_dict[interv_index] = interv_end

        interv_start = interv_end + 1

    return interv_start_dict, interv_end_dict


def read_interval(file_path: str):
    dict_read_start = {}
    dict_read_end = {}
    read_num = 0

    with open(file_path, 'r') as file:
        # pour chaque ligne dans mon fichier
        for line in file:
            # ignorer les headers
            if line.startswith('@'):
                continue

            # Diviser les colonnes en utilisant \t
            columns = line.split('\t')

            read_name = columns[0]
            read_start = int(columns[3])
            dict_read_start[str(read_num)] = read_start

            read_length = abs(int(columns[8]))
            read_end = read_start + read_length
            dict_read_end[str(read_num)] = read_end

            read_num += 1

        # Write dictionaries to the output file
        #change into def read_interval(file_path: str, output_file:str):
    #    with open(output_file, 'w') as out_file:
    #        out_file.write("Read Start Positions:\n")
    #        for read, start in dict_read_start.items():
    #            out_file.write(f"{read}: {start}\n")

    #        out_file.write("\nRead End Positions:\n")
    #        for read, end in dict_read_end.items():
    #            out_file.write(f"{read}: {end}\n")

    #    print(f"Dictionaries written to {output_file}")

    return dict_read_start, dict_read_end


def num_read_interval(file_path: str):
    num_read_interval = {}

    with open(file_path, 'r') as file:
        # pour chaque ligne dans mon fichier
        for line in file:
            # ignorer les headers
            if line.startswith('@SQ'):
                columns = line.split('\t')
                for col in columns:
                    if col.__contains__("LN:"):
                        LN = col.split(":")
                        chrom_length = int(LN[1])

    interval_start, interval_end = divise_chromosome(chrom_length, 1000)
    read_start, read_end = read_interval(file_path)

    for i in interval_start:
        int_start = interval_start[i]
        int_end = interval_end[i]
        counter = 0

        for j in read_start:
            rd_start = read_start[j]
            rd_end = read_end[j]
            if rd_start <= int_end and rd_end >= int_start:
                counter += 1
        num_read_interval[i] = counter

    return num_read_interval


reads_per_interval = num_read_interval(file_path)



def save_intervals_to_file(interval_counts:dict, output_file:str):

#    Saves the interval counts to a file.

#    Args:
#        interval_counts (dict): A dictionary where keys are interval indices and values are read counts.
#        output_file (str): The path to the file where the data will be saved.


    with open(output_file, 'w') as file:
        file.write("Interval\tRead_Count\n")  # Header
        for interval, count in sorted(interval_counts.items()):
            file.write(f"{interval}\t{count}\n")
    print(f"Interval counts have been saved to {output_file}")

save_intervals_to_file(reads_per_interval,output_file_path)

import matplotlib.pyplot as plt

#the plot is sus, to be rechecked
def plot_histogram(reads_per_interval):
    """
    Plots a histogram of the number of reads per interval.

    Args:
        reads_per_interval (dict): A dictionary where keys are interval indices and values are the count of reads.
    """
    # Extract the values (read counts) from the dictionary
    read_counts = list(reads_per_interval.values())

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(read_counts, bins=50, edgecolor='black', alpha=0.7)

    # Adding labels and title
    plt.xlabel('Number of Reads per Interval')
    plt.ylabel('Frequency')
    plt.title('Histogram of Reads per Interval')

    # Show the plot
    plt.show()

plot_histogram(reads_per_interval)