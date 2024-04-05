# annotation.py
import subprocess

def run_prokka(spades_output_dir, prokka_output_dir):
    """
    Ejecuta Prokka para anotar contigs ensamblados.
    
    :param spades_output_dir: Directorio de salida de SPAdes que contiene los contigs.
    :param prokka_output_dir: Directorio de salida para los archivos anotados por Prokka.
    """
    contigs_path = f"{spades_output_dir}/contigs.fasta"  # Ajustar donde esten los contigs.
    command = [
        'prokka',
        '--outdir', prokka_output_dir,
        '--prefix', 'annotated_contigs',
        contigs_path
    ]
    subprocess.run(command, check=True)
