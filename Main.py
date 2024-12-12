import matplotlib.pyplot as plt
import sys

# Where is my file?
file_path = sys.argv[1]

# mapped reads only or not?
mapped_only = bool(sys.argv[2])

# if filter for MapQ then reads > filter
filter_mapQ = int(sys.argv[3])

# interval size to reads couverage per chromosome
interval_size_user = int(sys.argv[4])

# interval of MapQ for the number of reads per MapQ value
interval_size_for_MAPQ_plot_user = int(sys.argv[5])

# where to save my results?
save_result_to = str(sys.argv[6])

print("~~~~~~~~~ Your analysis results ~~~~~~~~~")

# Fonction pour lire le SAM et le stocker en dictionnaire : sam_reds
# reads_per_chromosome{
#   [chr1] : {
#            [i]   : list[flag, read_start, read_end, MAPQ]
#            [i+1] : list[flag, read_start, read_end, MAPQ]
#                ...
#            }
#
#   [chr2] : {
#            list[i]   : [flag, read_start, read_end, MAPQ]
#            list[i+1] : [flag, read_start, read_end, MAPQ]
#                ...
#            }
#
#   [...]
def read_sam(file_path: str):
    reads_per_chromosome = {}
    reads_per_chromosome["*"] = {}
    chromosome_lengths = []
    i = 0

    with open(file_path, "r") as f:
        for line in f:

            # divise le SAM en colonnes utilisant \t
            columns = line.split('\t')

            if line.startswith('@'):
                if line.startswith('@SQ'):
                    for column in columns:
                        if column.startswith('LN'):
                            chromosome_length_info = column.split(":")[1]  # récup la longueur des chroms
                            chromosome_length = int(chromosome_length_info)  # transform longueur to entier
                            chromosome_lengths.append(chromosome_length)
                            # obtention d'une liste de longueurs des chroms

                        if column.startswith('SN'):
                            chromosome_name = column.split(":")[1]
                            reads_per_chromosome[chromosome_name] = {}
                            # obtention dict dont clé [SN]
                continue

            # extraire les flags de chaque read
            flag_value = int(columns[1])

            # extraire POS pour chaque read
            read_start = int(columns[3])

            # extraire la longueur pour calculer la fin du read
            read_length = abs(int(columns[8])) if columns[8].isdigit() else len(columns[9])
            read_end = read_start + read_length - 1  # 1-based system pour les position

            # stocker la valeur de QMAP
            read_quality = int(columns[4])

            # pour chaque read i, stocker dans la
            reads_values = (flag_value, read_start, read_end, read_quality)
            chromosome = columns[2]

            if chromosome not in reads_per_chromosome.keys():  # malgré la récup des SN en haut, je vérifie quand même
                # que tout les chromosome + symboles chelous sont pris en considération
                reads_per_chromosome[chromosome] = {}

            reads_per_chromosome[chromosome][i] = reads_values
            # |-----------------||----------||-|
            #   1st dict          2nd dict  3rd dict stores the read_values

            # incrémenter i
            i += 1

    return reads_per_chromosome, chromosome_lengths


reads_per_chromosome_raw, len_per_chrom = read_sam(file_path)


def filter_MAPQ_or_FLAG(reads_per_chromosome: dict, filter_mapQ: int, mapped_only: bool):
    filtered_reads_per_chromosome = {}

    # Determine the flag
    flag = 4 if mapped_only else 0

    # Process mapped chromosomes
    for chromosome in reads_per_chromosome:
        # Initialize dictionary for this chromosome
        if chromosome not in filtered_reads_per_chromosome:
            filtered_reads_per_chromosome[chromosome] = {}

        for read in reads_per_chromosome[chromosome]:
            if (int(reads_per_chromosome[chromosome][read][0]) & flag == 0
                    and int(reads_per_chromosome[chromosome][read][3]) >= filter_mapQ):
                filtered_reads_per_chromosome[chromosome][read] = reads_per_chromosome[chromosome][read]

    # Remove chromosomes with no filtered reads
    filtered_reads_per_chromosome = {
        chrom: reads
        for chrom, reads in filtered_reads_per_chromosome.items()
        if reads
    }

    return filtered_reads_per_chromosome


# Question 1
def mapped_read_count(reads_per_chromosome: dict):

    print("~~~~~~~~~~~ The count of mapped reads ~~~~~~~~~~~")

    resultat_mapped = {}
    i = 0
    compte_total = 0
    to_save = ""

    def save_file(content: str, output_file: str):
        #    Saves the interval counts to a file.

        #    Args:
        #        interval_counts (dict): A dictionary where keys are interval indices and values are read counts.
        #        output_file (str): The path to the file where the data will be saved.

        with open(output_file, 'w') as file:
            file.write(content)

    for chromosome in reads_per_chromosome:
        compte_mapped = 0
        for read in reads_per_chromosome[chromosome]:
            compte_total += 1

            if int(reads_per_chromosome[chromosome][read][0]) & 4 == 0:
                compte_mapped += 1

        resultat_mapped[chromosome] = compte_mapped

        if chromosome.isalnum():
            print(f"The number of mapped reads in chromosome {chromosome} is : {compte_mapped}")
            to_save += f"The number of mapped reads in chromosome {chromosome} is : {compte_mapped}\n"
        else:
            print(f"The number of unmapped reads is : {len(reads_per_chromosome[chromosome]) - compte_mapped}")
            to_save += f"The number of unmapped reads is : {len(reads_per_chromosome[chromosome]) - compte_mapped}\n"

    if compte_total == 0:
        print("No reads found in the input data.")
        return

    pourcentage = round(((sum(resultat_mapped.values()) / compte_total) * 100), 2)
    print(f"The number of mapped reads is : {sum(resultat_mapped.values())} ({pourcentage}%)")
    to_save += f"The number of mapped reads is : {sum(resultat_mapped.values())} ({pourcentage}%)\n"

    output_file_for_mapped_read = f"{save_result_to}/mapped_read_count.txt"
    save_file(to_save, output_file_for_mapped_read)
    print(f"Your results were saved to {output_file_for_mapped_read}\n")


mapped_read_count(reads_per_chromosome_raw)

# Question 2

reads_per_chromosome_filtered = filter_MAPQ_or_FLAG(reads_per_chromosome_raw, filter_mapQ, mapped_only)


def num_read_per_flag(reads_per_chromosome: dict):
    print("~~~~~~~~~~~ The count of reads per flag value ~~~~~~~~~~~")

    flag_distinct_reps = {}
    parsed_reads_dict = {}
    flags = ""
    to_print = ""
    i = 0

    def save_file(content: str, output_file: str):
        #    Saves the interval counts to a file.

        #    Args:
        #        interval_counts (dict): A dictionary where keys are interval indices and values are read counts.
        #        output_file (str): The path to the file where the data will be saved.

        with open(output_file, 'w') as file:
            file.write(content)

    for chromosome in reads_per_chromosome:
        for read in reads_per_chromosome[chromosome]:
            if reads_per_chromosome[chromosome][read][0] in flag_distinct_reps.keys():
                flag_distinct_reps[reads_per_chromosome[chromosome][read][0]] += 1
            else:
                flag_distinct_reps[reads_per_chromosome[chromosome][read][0]] = 1

    for flag in flag_distinct_reps:
        flags += f"{flag:<10} \t {flag_distinct_reps[flag]:<10} \n"  # < aligns the text to the left within a fixed-width space.
        # 10 specifies that each column should be at least 10 characters wide.

    to_print = f"{'flag':<10}{'read count':<10}\n{'-' * 20}\n{flags}"

    output_file_for_num_read_flag = f"{save_result_to}/read_count_per_flag.txt"
    save_file(to_print, output_file_for_num_read_flag)

    print(f"Your results were saved to {output_file_for_num_read_flag}\n")

    print(to_print)
    return flag_distinct_reps


num_read_per_flag(reads_per_chromosome_raw)


# Question 3 : ou les reads sont ils mappés
# divise chromosome output data structure
# interv_per_chromosome {
#       [chr1] {
#       [interv_index] : [interv_start, interv_end]
#       [interv_index+1] : [interv_start, interv_end]
#       }

#       [chr2] {
#       [interv_index] : [interv_start, interv_end]
#       [interv_index+1] : [interv_start, interv_end]
#       }
# }
def divise_chromosome(reads_per_chromosome: dict, chromosome_lengths: list, taille_interval: int):
    interv_per_chromosome_total = {}

    # Filter out `*` chromosome for unmapped reads
    chromosome_names = [chrom for chrom in reads_per_chromosome if chrom != '*']

    for chromosome_index, chromosome in enumerate(chromosome_names):
        interv_per_chromosome_total[chromosome] = {}

        longueur_chrom = chromosome_lengths[chromosome_index]
        interv_start = 1  # Start of the interval
        interv_index = 0  # Index for intervals in this chromosome

        while interv_start <= longueur_chrom:
            interv_end = interv_start + taille_interval - 1

            # Ensure the last interval doesn't exceed chromosome length
            if interv_end > longueur_chrom:
                interv_end = longueur_chrom

            # Store interval information
            interv_per_chromosome_total[chromosome][interv_index] = (interv_start, interv_end)

            # Move to the next interval
            interv_start = interv_end + 1
            interv_index += 1

    return interv_per_chromosome_total


def num_read_interval(reads_per_chromosome: dict, len_per_chrom: list, interval_size_user: int):

    print("~~~~~~~~~~~ The number of reads per interval for each chromosome ~~~~~~~~~~~")

    num_read_per_interval_per_chromosome = {}

    intervals_per_chromosome = divise_chromosome(reads_per_chromosome, len_per_chrom, interval_size_user)

    for chromosome in intervals_per_chromosome:
        num_read_per_interval_per_chromosome[chromosome] = {}

        for interval in intervals_per_chromosome[chromosome]:
            interval_info = intervals_per_chromosome[chromosome][interval]
            int_start = interval_info[0]
            int_end = interval_info[1]

            counter = 0

            for read in reads_per_chromosome[chromosome]:
                read_info = reads_per_chromosome[chromosome][read]
                rd_start = read_info[1]
                rd_end = read_info[2]

                if rd_start >= int_start and rd_end <= int_end:
                    counter += 1

                elif int_start < rd_start < int_end:
                    counter += 1

                elif int_start < rd_end < int_end:
                    counter += 1

            num_read_per_interval_per_chromosome[chromosome][interval] = counter

    def plot_read_counts_with_avg(reads_per_interval, chromosome: str):
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
        plt.title(f'Read Counts Per Interval of {chromosome} \n taille des intervals = {interval_size_user / 1000}kb',
                  fontsize=14)

        plt.legend(fontsize=10, loc='upper right')

        # Adjusting tick spacing and appearance
        plt.xticks(interval_indices[::max(1, len(interval_indices) // 10)], rotation=45)  # Avoid overcrowding
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Show the plot
        plt.tight_layout()

        savefig = f"{save_result_to}/graph_read_per_interval_{chromosome}"
        plt.savefig(savefig)

        print(f"Your plot was saved to {savefig}")

    for chromosome in num_read_per_interval_per_chromosome:
        plot_read_counts_with_avg(num_read_per_interval_per_chromosome[chromosome], chromosome)


num_read_interval(reads_per_chromosome_filtered, len_per_chrom, interval_size_user)


def read_count_per_quality(reads_per_chromosome: dict):
    """
    Analyzes and optionally plots/saves the read counts per MAPQ value for each chromosome.

    Args:
        reads_per_chromosome (dict): A dictionary of reads grouped by chromosomes.
    """

    print("~~~~~~~~~~~ The number of reads per MapQ value ~~~~~~~~~~~")

    def plot_read_counts_per_quality(chromosome: str, mapq_counts: dict):
        """Plots and optionally saves the read count distribution for a single chromosome."""
        mapq_values = list(mapq_counts.keys())
        read_counts = list(mapq_counts.values())

        # Plot the bar chart
        plt.figure(figsize=(12, 6))
        plt.bar(mapq_values, read_counts, color='skyblue', edgecolor='black')

        # Adding labels and title
        plt.xlabel('MAPQ Values', fontsize=12)
        plt.ylabel('Read Count', fontsize=12)
        plt.title(f'Read Count Distribution for Chromosome {chromosome}', fontsize=14)

        # Adjusting tick appearance
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()

        savefig = f"{save_result_to}/graph_read_per_MAPQ_{chromosome}.png"
        plt.savefig(savefig)

        print(f"Plot saved for chromosome: {chromosome} at {savefig}")

    def save_file(content: str, output_file: str):
        """Saves formatted content to a file."""
        with open(output_file, 'w') as file:
            file.write(content)
        print(f"Results saved to {output_file}")

    # Process each chromosome individually
    for chromosome in reads_per_chromosome:
        if chromosome == '*':  # Skip unmapped reads
            continue

        # Count MAPQ values for the current chromosome
        mapq_distinct_reps = {}
        for read in reads_per_chromosome[chromosome]:
            mapq_value = reads_per_chromosome[chromosome][read][3]
            mapq_distinct_reps[mapq_value] = mapq_distinct_reps.get(mapq_value, 0) + 1

        # Prepare the results table
        mapqs = f"{'MAPQ value':<15}{'Read count':<15}\n{'-' * 30}\n"
        mapqs += "\n".join(f"{mapq:<15}{count:<15}" for mapq, count in sorted(mapq_distinct_reps.items()))
        output_table = f"\n** Results for Chromosome {chromosome} **\n{mapqs}\n"

        # Save the results table
        output_file = f"{save_result_to}/table_read_per_MAPQ_{chromosome}.txt"
        save_file(output_table, output_file)

        # Plot the results
        plot_read_counts_per_quality(chromosome, mapq_distinct_reps)


read_count_per_quality(reads_per_chromosome_raw)


def save_file(content: str, output_file: str):
    #    Saves the interval counts to a file.

    #    Args:
    #        interval_counts (dict): A dictionary where keys are interval indices and values are read counts.
    #        output_file (str): The path to the file where the data will be saved.

    with open(output_file, 'w') as file:
        file.write(content)
