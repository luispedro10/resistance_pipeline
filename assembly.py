# assembly.py
import subprocess

def run_spades(input_fastq, output_dir, input_fastq2=None):
    command = [
        'spades.py',
        '-o', output_dir,
        '--careful',
        '--phred-offset', '33'
    ]
    if input_fastq2:
        # Modo de ensamblaje con lecturas pareadas
        command.extend(['-1', input_fastq, '-2', input_fastq2])
    else:
        # Modo de ensamblaje con una sola lectura
        command.extend(['-s', input_fastq])

    result = subprocess.run(command, check=False, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

