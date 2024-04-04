# preprocessing.py

import subprocess

def run_fastp(input_path, output_path):
    # Aquí va el código para ejecutar fastp y manejar sus archivos de entrada/salida
    subprocess.run(["fastp", "--in1", f"{input_path}/input_R1.fastq", "--out1", f"{output_path}/out_R1.fastq", "...otros argumentos..."])
