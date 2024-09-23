>  # Prostruc: Protein Structure Prediction Tool

Prostruc is a command-line tool designed for comprehensive protein structure prediction, leveraging sequence alignment, template-based modeling, deep learning, and validation techniques. With a simple input of either an amino acid sequence or a FASTA file, ProStruc generates high-quality protein structures using cutting-edge algorithms. ProStruc automates the process of blast searches, template selection, structural modeling, and validation, including RMSD, TM-score, and QMEAN.

## Key Features
Accepts input as a FASTA file or a raw amino acid sequence.
Performs sequence alignment and template-based modeling via ProMod3 and BLAST.
Incorporates deep learning-based predictions (ESMFold).
Validates results using structural comparison metrics (RMSD, TM-score) and QMEAN.
Supports Docker integration for handling modeling and validation engines.
Outputs the top-performing models for further analysis and evaluation.
Usage: You can run ProStruc from the terminal with a variety of options to customize the input and output, depending on your use case.

## Basic Commands
### Using a fasta file
```bash
   prostruc --fasta_file  <path_to_fasta>  --job_name <job_name>  --email <email>
   ```
### Using a sequence
```bash    
   prostruc --sequence <amino_acid_sequence>  --job_name <job_name>  --email <email>
   ````

## Required Arguments
- --fasta_file: Path to the target protein sequence in FASTA format.
- --sequence: Input target amino acid sequence directly as a string.
- --job_name: A custom name for the prediction job.
- --email: A valid email address to receive model results.

## Package Requirements

To ensure that Prostruc functions correctly, the following requirements must be met:

- **Python 3.6+**:  
  Prostruc requires Python version 3.6 or above. Ensure that you have the appropriate Python version installed. You can check your Python version with the following command:
  ```bash
  python --version

- **Docker**:
  Docker is necessary for managing the computational workloads, including modeling and validation processes. Make sure Docker is installed and actively running in the background.
  Verify Docker installation and status using:
  ```bash
  docker --version 

- **Internet**:
  An active internet connection is required for Prostruc to perform BLAST searches, retrieve templates, and complete various prediction     tasks.
## Example
```bash
    prostruc --sequence "AAAAA" --job_name "new_protien" --email "user@example.com"
```