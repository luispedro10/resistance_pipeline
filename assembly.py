# assembly.py
import subprocess

def run_spades(input_fastq, output_dir):
    command = [
        'spades.py',
        '-s', input_fastq,
        '-o', output_dir,
        '--careful',
        '--phred-offset', '33'
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode
