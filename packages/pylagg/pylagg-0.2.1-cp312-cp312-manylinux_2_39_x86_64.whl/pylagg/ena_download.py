from ftplib import FTP
import os

def quit_connection(message, ftp):
    print(message)
    # quit() can throw an exception if ftp server responds with error
    try:
        ftp.quit()
    except Exception as e:
        # This is more like a log message, just something to know that the ftp QUIT command failed.
        # This is not a critical error, so we can just close the connection with ftp.close().
        print("ftp QUIT command failed, trying to close the connection with ftp.close()", e)
        ftp.close()

def ena_download(sra_accession, output_dir):
    # small argument validations for the sra_accession parameter
    if (not sra_accession.isalnum()):
        print("Invalid SRA accession number. Please provide a valid SRA accession number.")
        return

    ftp = FTP('ftp.sra.ebi.ac.uk')
    ftp.login()

    prefix = sra_accession[:6]
    last_digit_of_accession = sra_accession[len(sra_accession)-1]

    # handles different format of directory for shorter accession numbers
    if (len(sra_accession) < 10):
        directory = f'/vol1/fastq/{prefix}/{sra_accession}'
    else:
        directory = f'/vol1/fastq/{prefix}/00{last_digit_of_accession}/{sra_accession}'

    try:
        ftp.cwd(directory)
    except Exception:
        quit_connection("Failed to access the directory for the provided accession number.\n"
                 "Please ensure that the accession number is correct and the corresponding\n"
                 "FASTQ files are available on ENA.", ftp)
        return

    file_names = ftp.nlst()
    if (file_names == []):
        quit_connection("No files found for the given SRA accession number.", ftp)
        return
    
    if (output_dir != None):
        if not os.path.exists(output_dir):
            quit_connection("Directory does not exist.", ftp)
            return

    for file_name in file_names:
        if (output_dir != None):
            local_file_path = os.path.join(output_dir, file_name)
        else:
            local_file_path = file_name
        print(f"Downloading {file_name}...")
        with open(local_file_path, 'wb') as f:
            ftp.retrbinary(f"RETR {file_name}", f.write)

    quit_connection("Downloaded file(s) successfully!", ftp)

    # TODO: (possibly) try with SRA toolkit if failure with ENA

# Example usage (uncomment to test):
# ena_download("SRR8782097", None) 
# ena_download("SRR8782097", "Users/mel/Downloads")
# ena_download("SRR8782097", "..") 

