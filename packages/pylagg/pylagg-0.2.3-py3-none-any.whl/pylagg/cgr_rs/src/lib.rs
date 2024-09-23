// rustimport:pyo3

use std::fs::File;
use std::io::{BufRead, BufReader};

use pyo3::prelude::*;
use image::{self, Pixel, RgbImage};

fn parse_kmer_line(line: String, k: Option<usize>) -> (String, u32) {
    let mut split_line = line.split_whitespace();

    let Some(kmer) = split_line.next() else {
        panic!("Unable to find kmer in line!");
    };

    if let Some(k_size) = k {
        if k_size != kmer.len() {
            panic!("The k-mer does not match the report length k={k_size}");
        } 
    }

    if !kmer.contains(|c| "ATCG".contains(c)) {
        panic!("The k-mer contains an invalid character that isn't A, T, C, or G!")
    }

    let Some(count_line) = split_line.next() else {
        panic!("Unable to find count for kmer!");
    };

    let Ok(count) = count_line.parse::<u32>() else {
        panic!("Unable to parse count string as a number!");
    };

    if count < 1 {
        panic!("All k-mer counts must be greater than or equal to 1!");
    }

    return (kmer.to_owned(), count);
}

fn get_kmer_counts(file_path: &str) -> (Vec<(String, u32)>, u32) {
    let input_file = File::open(file_path).unwrap();
    let reader = BufReader::new(input_file);

    let mut map = vec![];
    let mut max = 0;

    let mut k = None;
    
    for line_result in reader.lines() {
        if let Ok(line) = line_result {
            let (kmer, count) = parse_kmer_line(line, k);

            if k.is_none() {
                k = Some(kmer.len());
            }
            
            max = max.max(count);
            map.push((kmer.to_owned(), count));
        }
    }

    (map, max)
}

fn calculate_pos(kmer: &str, size: u32, bot_left: char, _top_left: char, top_right: char, bot_right: char) -> (u32, u32) {
    let mut x = 0;
    let mut y = 0;

    let mut offset = size >> 1;

    for base in kmer.chars().rev() {
        if base == bot_left || base == bot_right {
            x += offset;
        }

        if base == top_right || base == bot_right {
            y += offset;
        }

        offset >>= 1;
    }

    return (x, y)
}

fn generate_cgr_buffer(counts_file: &str, size: Option<u32>) -> RgbImage {
    let (kmer_counts, max) = get_kmer_counts(counts_file);    

    // Determines image size based on kmer length (2^k) if none is provided
    let img_size = match size {
        Some(some_size) => some_size,
        None => {
            let k = kmer_counts[0].0.len() as u32;
            2_i32.pow(k) as u32
        }
    };
    
    let mut imgbuf = RgbImage::new(img_size, img_size);

    for (kmer, count) in kmer_counts {
        let count = (count as f32).log10();
        let count = count / (max as f32).log10();

        let count = (count * 255.) as u8;

        // weak H-bonds W = {A, T} and strong H-bonds S = {G, C} on the diagonals        
        let (x, y) = calculate_pos(&kmer, img_size, 'A', 'G', 'T', 'C');
        imgbuf.get_pixel_mut(x, y).channels_mut()[0] = count;

        // purine R = {A, G} and pyrimidine Y = {C, T} on the diagonals
        let (x, y) = calculate_pos(&kmer, img_size, 'A', 'T', 'G', 'C');
        imgbuf.get_pixel_mut(x, y).channels_mut()[1] = count;

        // amino group M = {A, C} and keto group K = {G, T} on the diagonals
        let (x, y) = calculate_pos(&kmer, img_size, 'A', 'T', 'C', 'G');
        imgbuf.get_pixel_mut(x, y).channels_mut()[2] = count;
    }

    imgbuf
}

#[pyfunction]
fn generate_cgr_bytes(counts_file: &str, size: Option<u32>) -> Vec<u8> {
    let buf = generate_cgr_buffer(counts_file, size);
    buf.into_raw()
}

#[pyfunction]
fn generate_cgr_png(counts_file: &str, output_file: &str, size: Option<u32>) {
    let buf = generate_cgr_buffer(counts_file, size);
    let _ = buf.save(output_file);
}

// Integrates the generate_cgr functions into the Python module
#[pymodule]
fn cgr(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
   m.add_function(wrap_pyfunction!(generate_cgr_bytes, m)?)?;
   m.add_function(wrap_pyfunction!(generate_cgr_png, m)?)?;
   Ok(())
}
