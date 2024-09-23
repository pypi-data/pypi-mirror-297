import subprocess
import os

def genome_string_to_kmer_count(file_path, threads):
    # Check file type
    if not file_path.endswith(('.fastq', '.fastq.gz')):
        raise Exception("File type is not either .fastq or .fastq.gz")
    
    base_name = os.path.basename(file_path)

    # Modify the file extension to .jf for the output
    output_file = base_name.replace('.fastq', '.jf').replace('.gz', '')

    # If the input is a .fastq.gz file, use zcat (or gzcat on macOS)
    if file_path.endswith('.fastq.gz'):
        zcat_command = "zcat" if os.name != "posix" else "gzcat"  # Handles different platforms
        command = f"{zcat_command} {file_path} | jellyfish count -m 10 -s 100M -C -t {threads} -o {output_file} /dev/fd/0"
    else:
        # For .fastq files, directly use jellyfish
        command = f"jellyfish count -m 10 -s 100M -C -t {threads} -o {output_file} {file_path}"

    try:
        # Run the command using shell=True to process piping
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running Jellyfish: {e}")

    # Return the path to the k-mer count file
    return output_file