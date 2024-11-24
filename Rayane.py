x = 4

output_file = '/Users/ayoubrayaneaitallaoua/Documents/ProjetSyst/results.txt'

# Où est mon fichier?
file_path = '/Users/ayoubrayaneaitallaoua/Documents/ProjetSyst/mapping.sam'


# 1 1 1 1 1 1 1 1
# 1 2 4 8 16 32 64 128

def reads_QMAP30_or_FLAGNOT4(file_path: str):
    # clean_reads is a dictionnary with read numbers as keys and values
    # are lists containing the flag, start and end value for each read

    clean_reads = {}
    clean_reads_values = []

    # ouvrir le fichier en lecture 'r' sous le nom file
    with open(file_path, 'r') as file:
        # pour chaque ligne dans mon fichier
        i = 0

        for line in file:
            # ignorer les headers
            if line.startswith('@'):
                continue

            # Diviser les colonnes en utilisant \t
            columns = line.split('\t')

            if (int(columns[1]) & x == 0) and int(columns[4]) > 30:
                # extraire les flags de chaque read
                flag_value = int(columns[1])

                # extraire POS pour chaque read
                read_start = int(columns[3])

                # extraire la longueur pour calculer la fin du read
                read_length = abs(int(columns[8]))
                read_end = read_start + read_length

                #stocker la valeur de QMAP
                read_quality = int(columns[4])

                # pour chaque read i, stocker dans la
                clean_reads_values = flag_value, read_start, read_end, read_quality
                clean_reads[i] = clean_reads_values

                # incrémenter i
                i += 1

    return clean_reads


#print(reads_QMAP30_or_FLAGNOT4(file_path))

# BELOW def num_reads_per_flag(file_path:str) taking a file as input:
"""
def num_reads_per_flag(file_path:str):
    flag_list = []
    c = 0

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
    return flag_distinct_reps
"""


def divise_chromosome(longueur_chrom: int, taille_interval: int):
    interv_start_dict = {}
    interv_end_dict = {}

    interv_index = 0
    interv_start = 1

    while interv_start <= longueur_chrom:

        interv_end = int(interv_start + taille_interval - 1)

        if interv_end >= longueur_chrom:
            interv_end = longueur_chrom

        interv_start_dict[interv_index] = interv_start
        interv_end_dict[interv_index] = interv_end

        interv_start = interv_end + 1
        interv_index += 1

    return interv_start_dict, interv_end_dict


# def read_interval(file_path: str): taking a file as input
"""
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
        #with open(output_file, 'w') as out_file:
        #    out_file.write("Read Start Positions:\n")
        #    for read, start in dict_read_start.items():
        #        out_file.write(f"{read}: {start}\n")

        #    out_file.write("\nRead End Positions:\n")
        #    for read, end in dict_read_end.items():
        #        out_file.write(f"{read}: {end}\n")

        #print(f"Dictionaries written to {output_file}")

    return dict_read_start, dict_read_end
"""


#uses the clean reads
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

    clean_reads_dict = reads_QMAP30_or_FLAGNOT4(file_path)

    for i in interval_start:
        int_start = interval_start[i]
        int_end = interval_end[i]
        counter = 0

        for j in clean_reads_dict:
            read_info = clean_reads_dict[j]

            rd_start = read_info[1]
            rd_end = read_info[2]

            if rd_start >= int_start and rd_end <= int_end:
                counter += 1

            elif rd_start > int_start and rd_start < int_end:
                counter += 1

            elif rd_end > int_start and rd_end < int_end:
                counter += 1

        num_read_interval[i] = counter

    return num_read_interval


reads_per_interval = num_read_interval(file_path)

"""
Si d < a  et b < f alors
    [ab] est dans [df]
Sinon si d < a < f alors
    a est dans [df] donc ]ab] est dans [df]
Sinon si d < b < f alors
    b est dans [df] donc [ab[ est dans [df]
"""


#save_intervals_to_file(num_read_interval(file_path), output_file)

def save_intervals_to_file(interval_counts: dict, output_file: str):
    #    Saves the interval counts to a file.

    #    Args:
    #        interval_counts (dict): A dictionary where keys are interval indices and values are read counts.
    #        output_file (str): The path to the file where the data will be saved.

    with open(output_file, 'w') as file:
        file.write("Interval\tRead_Count\n")  # Header
        for interval, count in sorted(interval_counts.items()):
            file.write(f"{interval}\t{count}\n")
    print(f"Interval counts have been saved to {output_file}")


import matplotlib.pyplot as plt


# the plot is sus, to be rechecked
def plot_percentage_reads_line(reads_per_interval):
    """
    Plots a line graph with interval indices on the X-axis and the percentage of reads in each interval on the Y-axis.

    Args:
        reads_per_interval (dict): A dictionary where keys are interval indices and values are the count of reads.
    """
    # Calculate the total number of reads
    total_reads = sum(reads_per_interval.values())

    # Calculate percentage of reads per interval
    interval_indices = list(reads_per_interval.keys())
    percentages = [(count / total_reads) * 100 for count in reads_per_interval.values()]

    # Plot the line graph
    plt.figure(figsize=(30, 6))
    plt.plot(interval_indices, percentages, marker='o', color='blue', linestyle='-', linewidth=2, markersize=2)

    # Adding labels and title
    plt.xlabel('Interval Index', fontsize=12)
    plt.ylabel('Percentage of Reads (%)', fontsize=12)
    plt.title('Percentage of Reads Per Interval (Line Graph)', fontsize=14)
    # Set the Y-axis range
    plt.ylim(0.0, 0.2)

    # Adding grid for better readability
    plt.grid(axis='both', linestyle='--', alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()


#plot_percentage_reads_line(reads_per_interval)


import matplotlib.pyplot as plt

def plot_read_counts(reads_per_interval):
    """
    Plots a bar chart with interval indices on the X-axis and the count of reads on the Y-axis.

    Args:
        reads_per_interval (dict): A dictionary where keys are interval indices and values are the count of reads.
    """
    # Extract the keys (interval indices) and values (read counts)
    interval_indices = list(reads_per_interval.keys())
    read_counts = list(reads_per_interval.values())

    # Calculate the average number of reads per interval
    average_reads = sum(read_counts) / len(read_counts)

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(interval_indices, read_counts, color='skyblue', edgecolor='black')

    # Line for average reads
    plt.axhline(y=average_reads, color='red', linestyle='--', linewidth=2,
                label=f'Average Reads Per Interval ({average_reads:.2f})')

    # Adding labels and title
    plt.xlabel('Interval Index', fontsize=12)
    plt.ylabel('Read Count', fontsize=12)
    plt.title('Read Counts Per Interval', fontsize=14)

    plt.legend(fontsize=10, loc='upper right')

    # Adjusting tick spacing and appearance
    plt.xticks(interval_indices[::max(1, len(interval_indices) // 10)], rotation=45)  # Avoid overcrowding
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()


plot_read_counts(reads_per_interval)
