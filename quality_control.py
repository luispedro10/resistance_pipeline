import subprocess

def run_fastp(input_fastq, output_fastq_clean, output_fastq_report):
    """
    Ejecuta fastp para el control de calidad de secuencias FASTQ.
    
    :param input_fastq: Ruta al archivo FASTQ de entrada.
    :param output_fastq_clean: Ruta al archivo FASTQ de salida limpio.
    :param output_fastq_report: Ruta al archivo de reporte HTML de fastp.
    """
    command = [
        'fastp',
        '-i', input_fastq,
        '-o', output_fastq_clean,
        '--html', output_fastq_report,
        '--thread', '4'  # Hilos para cpu.
    ]
    subprocess.run(command, check=True)