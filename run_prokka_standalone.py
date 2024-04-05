from annotation import run_prokka

# Asegúrate de que estas rutas sean correctas para tu setup
spades_output_dir = "./spades_output"
prokka_output_dir = "./prokka_output"

# Llama a la función run_prokka con las rutas de los directorios
run_prokka(spades_output_dir, prokka_output_dir)
