import subprocess

def run_fastp(input_fastq, output_fastq_clean, output_fastq_report, input_fastq2=None, output_fastq_clean2=None):
    """
    Ejecuta fastp para el control de calidad de secuencias FASTQ.
    
    :param input_fastq: Ruta al archivo FASTQ de entrada para forward o single-end.
    :param output_fastq_clean: Ruta al archivo FASTQ de salida limpio para forward o single-end.
    :param output_fastq_report: Ruta al archivo de reporte HTML de fastp.
    :param input_fastq2: Ruta al archivo FASTQ de entrada para reverse, opcional.
    :param output_fastq_clean2: Ruta al archivo FASTQ de salida limpio para reverse, opcional.
    """
    command = [
        'fastp',
        '-i', input_fastq,
        '-o', output_fastq_clean,
        '--html', output_fastq_report,
        '--thread', '4'  # Hilos para cpu.
    ]
    if input_fastq2 and output_fastq_clean2:
        command.extend(['-I', input_fastq2, '-O', output_fastq_clean2])
    
    subprocess.run(command, check=True)
