# pipeline.py

import preprocessing
import assembly
import annotation
import resistance_detection

def main():
    # Configura aquí las rutas de entrada y salida, y otras configuraciones iniciales
    raw_data_path = "path/to/raw/data"
    processed_data_path = "path/to/processed/data"
    assembly_path = "path/to/assembly/results"
    annotation_path = "path/to/annotation/results"
    resistance_path = "path/to/resistance/results"

    # 1. Preprocesamiento
    preprocessing.run_fastp(raw_data_path, processed_data_path)

    # 2. Ensamblaje
    assembly.run_spades(processed_data_path, assembly_path)

    # 3. Anotación
    annotation.run_prokka(assembly_path, annotation_path)

    # 4. Detección de resistencia
    resistance_detection.run_abricate(annotation_path, resistance_path)

if __name__ == "__main__":
    main()
