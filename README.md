# Genomic Data Processing and Visualization

This project provides a set of Python and BASH scripts for processing and visualizing genomic data from SAM files, commonly used in next-generation sequencing (NGS). The code filters, analyzes, and visualizes read data based on various genomic criteria such as read quality, FLAG values, and chromosomal intervals.

## Features

- **Filter Reads**:
  Select reads based on:
  - Mapping quality (QMAP < 30 or another chosen value)
  - FLAG values (unmapped reads with FLAG = 4).
  
- **Interval-Based Analysis**:
  - Divide chromosomes into defined intervals and counts the number of reads within each interval.
  
- **Quality Analysis**:
  -  Counts reads per flag value
  -  Generates the distribution of reads across MAPQ quality values to provide insights into the overall quality alignement
  
- **Visualization**:
  - Generates bar charts for interval-based and quality-based read counts (MAPQ).

- **Export Results**:
  - Saves results into a file for further analysis.

## Requirements

- Python 3.x
- Matplotlib

Install required packages using:
```bash
pip install matplotlib
```
## File Structure
- 'launch.sh': A shell script that interacts with the user, verifies input files, and executes the Python pipeline.
- 'Main.py': The main Python script, containing various functions for data filtering, analysis, and visualization.

## Execution
To launch the program :

```bash
chmod +x ./launch.sh
```
```bash
./launch.sh
```
Example File Path required in bash script: /path/to/your/project/data/input_file.sam
