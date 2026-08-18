# VCF to TSV Converter

A lightweight Python utility designed to validate VCF files and expand (tabulate) the dense `INFO` column (8th column) into individual, tab-separated columns for easy downstream analysis and inspection.

## Features

* **INFO Column Tabulation:** Unpacks key-value pairs from the 8th column (`INFO`) into clean, independent TSV columns.
* **Format Validation:** Verifies essential VCF metadata (`##`) and ensures the presence of the mandatory first 8 columns (`#CHROM`, `POS`, `ID`, `REF`, `ALT`, `QUAL`, `FILTER`, `INFO`).
* **Zero Dependencies:** Built entirely with Python standard libraries (`pathlib`, `re`, `sys`) — no external packages required.
* **Safe Missing-Value Handling:** Automatically handles missing flags or tags without shifting table columns.

## Requirements

* Python 3.10 or higher

## Usage

1. Clone or download this repository:
   ```bash
   git clone https://github.com/Anna19327/VCF-to-TSV-converter-.git
cd VCF-to-TSV-converter-```
