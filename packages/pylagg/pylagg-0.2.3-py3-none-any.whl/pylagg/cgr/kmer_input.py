from io import BytesIO, TextIOWrapper

import PIL.Image as im
from pylagg.cgr.image_gen import generate_image

from typing import Dict, Tuple

def contains_valid_characters(input_string: str) -> bool:
    """
    Checks if the given input string contains valid base pair characters
    """    
    for char in input_string:
        if char not in {'A', 'T', 'C', 'G'}:
            return False
    
    return True

def parse_count_file_line(line: str, k: int) -> Tuple[str, int]:
    """
    Reads a line from an input counts file with a given kmer length 'k', returns the tuple: (kmer, count)
    """

    line_split = line.split()
    kmer = line_split[0]

    if k <= 0:
        raise Exception("The k-mer length must be greater than zero")
    
    if len(kmer) != k:
        raise Exception(f"The k-mer does match the reported length k={k}")

    if not contains_valid_characters(kmer):
        raise Exception(f"Invalid k-mer character in {kmer} (valid characters are A, T, C, G)")

    try:
        count = int(line_split[1])
    except ValueError:
        raise Exception("Count must only contain integer values")

    if count < 1:
        raise Exception("All k-mer counts must be ≥1")
    
    return (kmer, count)


def count_file_to_dictionary(file: TextIOWrapper) -> Dict[str, int]:
    """
    Takes a counts file as input and outputs a dictionary representation used later for image generation
    """

    k_dict = {}

    with file:
        k = len(file.readline().split()[0])
        file.seek(0)

        for line in file:
            if 'N' in line: continue
            (kmer, count) = parse_count_file_line(line, k)
            k_dict.update({kmer : count})

    return k_dict

def count_file_to_image(input_data: TextIOWrapper, verbose=True) -> im.Image:
    """
    Takes a counts file as input and returns the generated image as an image object
    """

    k_dict = count_file_to_dictionary(input_data)
    return generate_image(k_dict, verbose)

def count_file_to_image_file(input_data: TextIOWrapper, output_file: str | BytesIO, output_type="png", verbose=True):
    """
    Takes counts file data and creates an image at the provided file path or buffer with the given output file type
    """
    
    img = count_file_to_image(input_data, verbose)
    img.save(output_file, output_type)