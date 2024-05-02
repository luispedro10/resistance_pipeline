import subprocess
import os
import pandas as pd

def run_rgi(annotated_contigs_path, output_dir):
    """
    Ejecuta RGI para detectar genes de resistencia en las secuencias anotadas.
    :param annotated_contigs_path: Ruta al archivo de contigs anotados por Prokka (.fna o .fasta).
    :param output_dir: Directorio donde se guardarán los resultados de RGI.
    """
    # Asegura que el directorio de salida exista
    os.makedirs(output_dir, exist_ok=True)
    
    # Ruta al archivo de salida de RGI
    rgi_output_path_json = os.path.join(output_dir, "rgi_output.json")
    rgi_output_path_excel = os.path.join(output_dir, "rgi_output.xlsx")
    
    # Comando para ejecutar RGI
    command = [
        "conda", "run", "-n", "rgi_env", "rgi",
        "main", "--input_sequence", annotated_contigs_path, 
        "--output_file", rgi_output_path_json, 
        "--input_type", "contig",
        "--local",  # Este flag indica a RGI que use la base de datos CARD local
        "--debug"   # Habilita el modo debug para más detalles durante la ejecución
    ]
    
    # Ejecuta el comando y espera a que termine
    subprocess.run(command, check=True)
    
    # Convierte JSON a Excel
    convert_json_to_excel(rgi_output_path_json, rgi_output_path_excel)
    
    print(f"RGI ha finalizado. Los resultados se han guardado en {rgi_output_path_json} y {rgi_output_path_excel}")

def convert_json_to_excel(input_file, output_file):
    """
    Convierte un archivo JSON a Excel.
    :param input_file: Ruta al archivo JSON de entrada.
    :param output_file: Ruta al archivo Excel de salida.
    """
    df = pd.read_json(input_file)
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    annotated_contigs_path = "./prokka_output/annotated_contigs.fna"
    output_dir = "./rgi_output"
    run_rgi(annotated_contigs_path, output_dir)
