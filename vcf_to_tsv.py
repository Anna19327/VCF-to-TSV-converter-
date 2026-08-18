import sys
import re
from pathlib import Path

def process_vcf(vcf_path: Path, output_path: Path, keep_meta: bool = True):
    fixed_headers = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
    info_keys = []
    
    with open(vcf_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        
        line = infile.readline()
        if not line.startswith('##'):
            raise ValueError(f"Error in {vcf_path.name}: File must start with '##'")

        # 1. Collect INFO keys from metadata headers (##INFO=<ID=...>)
        while line.startswith('##'):
            if match := re.search(r'^##INFO=<ID=([^,]+)', line):
                key = match.group(1)
                if key not in info_keys:
                    info_keys.append(key)
            if keep_meta:
                outfile.write(line)
            line = infile.readline()

        if not info_keys:
            raise ValueError(f"Error in {vcf_path.name}: No ##INFO headers found in metadata")

        # 2. Validate standard VCF table header (first 8 columns)
        header = line.strip().split('\t')
        if not line.startswith('#') or header[:8] != fixed_headers:
            raise ValueError(f"Error in {vcf_path.name}: Invalid header. First 8 columns must be {fixed_headers}")

        # 3. Construct new header (replace INFO column with individual sub-columns)
        new_header = header[:7] + info_keys + header[8:]
        outfile.write('\t'.join(new_header) + '\n')

        # 4. Process and tabulate data rows
        for line_num, line in enumerate(infile, start=2):
            if not line.strip(): 
                continue
            row = line.strip().split('\t')
            
            # Parse key-value pairs from the 8th column (INFO)
            info_dict = {}
            for item in row[7].split(';'):
                if '=' in item:
                    k, v = item.split('=', 1)
                else:
                    k, v = item, 'TRUE'  # Flag fields without explicit value
                info_dict[k] = v

            # Extract INFO values in fixed order matching the header
            info_values = [info_dict.get(k, '') for k in info_keys]
            
            # Reassemble row with expanded INFO columns
            new_row = row[:7] + info_values + row[8:]
            outfile.write('\t'.join(new_row) + '\n')

if __name__ == '__main__':
    src_dir = Path(input('Path to source VCF folder: ').strip())
    trg_dir = Path(input('Path to target output folder: ').strip())
    trg_dir.mkdir(parents=True, exist_ok=True)

    for vcf_file in src_dir.glob('*.vcf'):
        out_file = trg_dir / f"{vcf_file.stem}_tab.tsv"
        print(f"Processing: {vcf_file.name} -> {out_file.name}")
        process_vcf(vcf_file, out_file, keep_meta=False)
