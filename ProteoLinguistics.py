import os
import csv

def fasta_to_sequences(filename):
    """Reads a FASTA file and returns a list of sequences."""
    sequences = []
    with open(filename, 'r') as f:
        sequence = ''
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if sequence:
                    sequences.append(sequence)
                sequence = ''
            else:
                sequence += line
        if sequence:
            sequences.append(sequence)
    return sequences

def word_to_sequence(word):
    """Converts a word to amino acid sequence."""
    word = word.upper()
    return ''.join([char if 'A' <= char <= 'Z' else '' for char in word])

def find_matches(fasta_filename, dictionary_filename):
    """Finds matches of words in the FASTA sequences."""
    sequences = fasta_to_sequences(fasta_filename)
    matches = []
    with open(dictionary_filename, 'r') as f:
        for word in f:
            word = word.strip().lower()
            if len(word) <= 2:  # Skip two-letter words
                continue
            amino_seq = word_to_sequence(word)
            for sequence in sequences:
                if amino_seq in sequence:
                    matches.append(word)
                    break
    return matches

def process_all_fasta_files(directory_path, dictionary_filename, results_directory):
    """Process all FASTA files in the specified directory."""
    for filename in os.listdir(directory_path):
        if filename.endswith('.fasta'):
            fasta_path = os.path.join(directory_path, filename)
            matched_words = find_matches(fasta_path, dictionary_filename)
            
            # Extract the name from the fasta_filename without the .fasta suffix
            fasta_file_name = filename.replace('.fasta', '')
            
            # Save matched words to a CSV file in the specified results directory with the modified name
            output_filename = os.path.join(results_directory, f'matched_words_{fasta_file_name}.csv')
            
            with open(output_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Matched Words"])  # Header
                for word in matched_words:
                    writer.writerow([word])

            print(f"Processed {filename}:")
            print(f"Words matched: {len(matched_words)}")
            print(f"Results saved to {output_filename}\n")

directory_path = ''
dictionary_filename = ''
results_directory = ''

# Ensure the results directory exists
if not os.path.exists(results_directory):
    os.makedirs(results_directory)

process_all_fasta_files(directory_path, dictionary_filename, results_directory)

