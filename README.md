# Genomic Data Processing and Visualization

This project provides a set of Python scripts for processing and visualizing genomic data from SAM files. The code filters, analyzes, and visualizes read data based on various criteria such as read quality, FLAG values, and chromosomal intervals.

## Features

- **Filter Reads**:
  - Select reads based on quality (QMAP > 30) and FLAG values (not unmapped).
  
- **Interval-Based Analysis**:
  - Divide chromosomes into intervals and count the number of reads within each interval.
  
- **Quality Analysis**:
  - Analyze and visualize the distribution of reads across MAPQ quality intervals.
  
- **Visualization**:
  - Generate bar charts and line graphs for interval-based and quality-based read counts.

- **Export Results**:
  - Save interval read counts to a file for further analysis.

## Requirements

- Python 3.x
- Matplotlib

Install required packages using:
```bash
pip install matplotlib

