import os # Provides functions for interacting with the operating system.
from datetime import datetime
import pandas as pd
import subprocess

print("Script is running...")

# Set the number of OpenBLAS threads
os.environ["OPENBLAS_NUM_THREADS"] = "16"

# Define paths
output_base = "/home/mfafouti/scratch/Mommybrain_marlen/Curio/OUTPUT_Seeker"
fastq_path = "/home/mfafouti/scratch/Mommybrain_marlen/Curio/all_merged_fastqs_slideseq"
tile_folder = "/home/mfafouti/scratch/Mommybrain_marlen/Curio/all_merged_fastqs_slideseq/bacrodes"
slurm_script_folder = "/home/mfafouti/scratch/Mommybrain_marlen/Curio/all_merged_fastqs_slideseq/SLURM_scripts"

email = "mariaeleni.fafouti@mail.utoronto.ca"

# Read sample and tile lists from CSV
csv_file = "/home/mfafouti/scratch/Mommybrain_marlen/Curio/Slide_seq_Nuos_tile_ids_matching.csv" 
sample_tile_matching = pd.read_csv(csv_file)
sample_list = sample_tile_matching['Sample'].tolist()
tile_list = sample_tile_matching['Nuo_Best_Matched_tile'].tolist()

print("Current working directory:", os.getcwd())

for i, sample in enumerate(sample_list):
#     # Obtaining the specific components for the samplesheet
#     CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')
#     TILE_ID = os.path.join(tile_folder, tile_list[i] + "_BeadBarcodes.txt")
#     FASTQ_1 = os.path.join(fastq_path, sample + "_merged_R1.fastq.gz") 
#     FASTQ_2 = os.path.join(fastq_path, sample + "_merged_R2.fastq.gz") 
    
#     # SLURM job script for sbatch submission with email notifications
#     # Creating samplesheet - 1 sample
#     # table_header = ["sample", "experiment_date", "barcode_file", "fastq_1", "fastq_2", "genome"]
#     # table_content = [sample, CURRENT_DATE, TILE_ID, FASTQ_1, FASTQ_2, "mRatBN7.2"]
    samplesheet_file = f"{sample}_samplesheet_seeker.csv"
    
#     # with open(samplesheet_path, mode='w', newline='') as file:
#     #     writer = csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\')
#     #     writer.writerow(table_header)
#     #     writer.writerow(table_content)

#     # SLURM job script
#     sbatch_script = f"""#!/bin/bash
# #SBATCH --job-name=CurioSeeker_gpu_{sample}   # Name of your job
# #SBATCH --account=def-shreejoy                # Compute Canada account
# #SBATCH --time=34:00:00                        # Job time (HH:MM:SS) 
# #SBATCH --nodes=1                              # Number of nodes
# #SBATCH --ntasks=1                             # Number of tasks
# #SBATCH --cpus-per-task=16                      # Request 16 CPU cores per task
# #SBATCH --mem=64G                              # Request 64 GB of memory
# #SBATCH --output={output_base}/%x_%j.out       # Standard output
# #SBATCH --error={output_base}/%x_%j.err        # Standard error
# #SBATCH --mail-user={email}
# #SBATCH --mail-type=BEGIN,END,FAIL

# cd /home/mfafouti/scratch/Mommybrain_marlen/Curio/curioseeker-v3.0.0
# module load StdEnv/2020
# module load nextflow/23.04.3
# module load apptainer
# export root_output_dir={output_base}
# export NXF_SINGULARITY_CACHEDIR=/home/mfafouti/scratch/Mommybrain_marlen/Curio/curioseeker-v3.0.0/.singularity
# nextflow run main.nf \
#     --input /home/mfafouti/scratch/Mommybrain_marlen/Curio/{samplesheet_file} \
#     --outdir ${output_base}/results/ \
#     -work-dir ${output_base}/work/ \
#     --igenomes_base /home/mfafouti/scratch/Mommybrain_marlen/Curio/curioseeker-v3.0.0 \
#     -profile slurm \
#     -config /home/mfafouti/scratch/Mommybrain_marlen/Curio/curioseeker-v3.0.0/slurm.config
# """

    # # Write the SLURM script to a file
    sbatch_script_path = os.path.join(slurm_script_folder, f"sbatch_curioseeker_{sample}.slurm")
    # with open(sbatch_script_path, "w") as f:
    #     f.write(sbatch_script)

    # Submit the job using sbatch
    try:
        subprocess.run(["sbatch", sbatch_script_path], check=True)
        print(f"Submitted Curio Seeker job for {sample}. SLURM script: {sbatch_script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to submit Curio Seeker job for {sample}. Error: {e}")