import matplotlib.pyplot as plt

# flag value
x = 4
taille_interv = 10000
output_file = '/Users/ayoubrayaneaitallaoua/Documents/ProjetSyst/dictionnary.txt'

# Où est mon fichier?
file_path = '/Users/ayoubrayaneaitallaoua/Documents/ProjetSyst/mapping.sam'


# Question 1
def mapped_read_count(filepath: str):
    x = 4
    compte_read = 0

    with open(filepath, "r") as f:
        for line in f:

            if line.startswith('@'):
                continue
            columns = line.split('\t')

            flag = columns[1]
            # print (f"name: {name}", f"flag: {flag}")

            if int(flag) & x == 0:
                compte_read = compte_read + 1

    return compte_read


# print(f"le nombre de read mappé est: {mapped_read_count(file_path)}")


# Question 2
# filtre pour MAPQ < 30 AND Flag & 4 == 0
def reads_QMAP30_or_FLAGNOT4(file_path: str):
    # clean reads est un dictionnaire dont lequel le numéro du read est une clé
    # est les valeurs sont : flag, debut du read, fin du read et MAPQ. Tout en int.

    clean_reads = {}

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

            if (int(columns[1]) & x == 0) and int(columns[4]) < 30:
                # extraire les flags de chaque read
                flag_value = int(columns[1])

                # extraire POS pour chaque read
                read_start = int(columns[3])

                # extraire la longueur pour calculer la fin du read
                read_length = abs(int(columns[8]))
                read_end = read_start + read_length - 1  # 1-based system pour les position

                # stocker la valeur de QMAP
                read_quality = int(columns[4])

                # pour chaque read i, stocker dans la
                clean_reads_values = flag_value, read_start, read_end, read_quality
                clean_reads[i] = clean_reads_values

                # incrémenter i
                i += 1

    return clean_reads


# print(reads_QMAP30_or_FLAGNOT4(file_path))


def num_read_per_flag(clean_reads: dict):
    flag_distinct_reps = {}

    for i in clean_reads:
        read_values = clean_reads[i]
        flag_value = read_values[0]

        if flag_value in flag_distinct_reps:
            flag_distinct_reps[flag_value] = flag_distinct_reps[flag_value] + 1
        else:
            flag_distinct_reps[flag_value] = 1

    return flag_distinct_reps


# print(num_read_per_flag(reads_QMAP30_or_FLAGNOT4(file_path)))


# Question 3 : ou les reads sont ils mappés
def divise_chromosome(file_path: str, taille_interval: int):
    interv_dict = {}

    interv_index = 0
    interv_start = 1

    with open(file_path, 'r') as file:
        # pour chaque ligne dans mon fichier
        for line in file:
            # ignorer les headers
            if line.startswith('@SQ'):
                columns = line.split('\t')
                for col in columns:
                    if col.__contains__("LN:"):
                        LN = col.split(":")
                        longueur_chrom = int(LN[1])

    while interv_start <= longueur_chrom:

        interv_end = int(interv_start + taille_interval - 1)

        if interv_end >= longueur_chrom:
            interv_end = longueur_chrom

        interv_info = interv_start, interv_end
        interv_dict[interv_index] = interv_info

        interv_start = interv_end + 1
        interv_index += 1

    return interv_dict


# print(divise_chromosome(file_path, 100000))

def num_read_interval(file_path: str, taille_interval):
    num_read_interval = {}

    # le dictionnaire de tout les intervals avec le numéro d'interval comme index et la liste contenant int_start
    # et int end comme valeurs

    interval = divise_chromosome(file_path, taille_interval)

    clean_reads_dict = reads_QMAP30_or_FLAGNOT4(file_path)

    for i in interval:

        interval_info = interval[i]
        int_start = interval_info[0]
        int_end = interval_info[1]

        counter = 0

        for j in clean_reads_dict:

            read_info = clean_reads_dict[j]
            rd_start = read_info[1]
            rd_end = read_info[2]

            if rd_start >= int_start and rd_end <= int_end:
                counter += 1

            elif int_start < rd_start < int_end:
                counter += 1

            elif int_start < rd_end < int_end:
                counter += 1

        num_read_interval[i] = counter

    return num_read_interval


# print(num_read_interval(file_path, taille_interv))


def plot_read_counts_with_avg(reads_per_interval):
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
    plt.title(f'Read Counts Per Interval\ntaille des intervals = {taille_interv / 1000}kb', fontsize=14)

    plt.legend(fontsize=10, loc='upper right')

    # Adjusting tick spacing and appearance
    plt.xticks(interval_indices[::max(1, len(interval_indices) // 10)], rotation=45)  # Avoid overcrowding
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()


# plot_read_counts_with_avg(num_read_interval(file_path, taille_interv))

def read_count_per_quality(file_path: str):
    read_count_quality = {}
    i = 0
    clean_reads_dict = reads_QMAP30_or_FLAGNOT4(file_path)

    for i in clean_reads_dict:
        read_info = clean_reads_dict[i]
        read_MAPQ = read_info[3]

        if read_MAPQ in read_count_quality:
            read_count_quality[read_MAPQ] += 1
        else:
            read_count_quality[read_MAPQ] = 1

    return read_count_quality


def plot_read_counts_per_quality(reads_per_interval):
    """
    Plots a bar chart with interval indices on the X-axis and the count of reads on the Y-axis.

    Args:
        reads_per_interval (dict): A dictionary where keys are interval indices and values are the count of reads.
    """
    # Extract the keys (interval indices) and values (read counts)
    interval_indices = list(reads_per_interval.keys())
    read_counts = list(reads_per_interval.values())

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(interval_indices, read_counts, color='skyblue', edgecolor='black')

    # Adding labels and title
    plt.xlabel('MAPQ values', fontsize=12)
    plt.ylabel('Read Count', fontsize=12)
    plt.title(f'Read count per distribution values', fontsize=14)

    # Adjusting tick spacing and appearance
    plt.xticks(interval_indices[::max(1, len(interval_indices) // 10)], rotation=45)  # Avoid overcrowding
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.tight_layout()
    plt.show()


# print(read_count_per_quality(file_path))

# plot_read_counts_per_quality_with_avg(read_count_per_quality(file_path))


def save_dict_to_file(dictionnary: dict, output_file: str):
    #    Saves the interval counts to a file.

    #    Args:
    #        interval_counts (dict): A dictionary where keys are interval indices and values are read counts.
    #        output_file (str): The path to the file where the data will be saved.

    with open(output_file, 'w') as file:
        file.write("Keys\tRead_Count\n")  # Header
        for interval, count in sorted(dictionnary.items()):
            file.write(f"{interval}\t{count}\n")
    print(f"Interval counts have been saved to {output_file}")


# save_dict_to_file(num_read_interval(file_path, taille_interv), output_file)
