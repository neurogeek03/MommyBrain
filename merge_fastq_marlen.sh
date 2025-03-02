#!/bin/bash

# Define input and output directories
INPUT_DIR="/home/mfafouti/scratch/Mommybrain_marlen/Curio/Data_niagara_new"  # Replace with your input directory
OUTPUT_DIR="/home/mfafouti/scratch/Mommybrain_marlen/Curio/new_fastqs_merged"
mkdir -p $OUTPUT_DIR

# # Function to gzip .ora files if they exist
# gzip_ora_file() {
#     local sample=$1
#     local read=$2
#     local pattern="${INPUT_DIR}/${sample}_lib_S*_L00*_${read}_001.fastq.ora"
    
#     # Check if .ora files exist
#     if ls $pattern 1> /dev/null 2>&1; then
#         echo "Found .ora files for ${sample} ${read}, compressing them..."
#         # Gzip the .ora files
#         local gz_output="${OUTPUT_DIR}/${sample}_merged_${read}.fastq.ora.gz"
#         gzip -c $pattern > $gz_output
        
#         # Verify compression
#         total_size=$(stat -c %s $gz_output)
#         echo "Created compressed file ${gz_output} (${total_size} bytes)"
#     else
#         echo "No .ora files found for ${sample} ${read}, skipping compression."
#     fi
# }

# Function to merge .fastq.gz files
merge_fastqs() {
    local sample=$1
    local read=$2
    local pattern="${INPUT_DIR}/${sample}_lib_S*_L00*_${read}_001.fastq.gz"
    local output="${OUTPUT_DIR}/${sample}_merged_${read}.fastq.gz"
    
    echo "Merging ${pattern} into ${output}"
    
    # Check if input files exist
    if ls $pattern 1> /dev/null 2>&1; then
        cat $pattern > $output
        
        # Verify merge
        total_size=$(stat -c %s $output)
        echo "Created ${output} (${total_size} bytes)"
    else
        echo "Error: No files found matching pattern ${pattern}"
        exit 1
    fi
}

# Process each sample
for sample in B2 B3 B11 B14 B23 B33 B37 B42 B47 B48; do
    echo "Processing sample ${sample}..."
    
    # # Check and compress .ora files first
    # gzip_ora_file $sample "R1"
    # gzip_ora_file $sample "R2"
    
    # Merge .fastq.gz files
    merge_fastqs $sample "R1"
    merge_fastqs $sample "R2"
done

echo "Merge and compression complete. Please verify the output files in ${OUTPUT_DIR}/"