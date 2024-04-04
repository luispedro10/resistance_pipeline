import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from quality_control import run_fastp

class GenomeAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genome Analysis Pipeline")
        self.geometry("400x300")  # Ajusta el tamaño según necesites
        self.configure(bg='#f0f0f0')  # Color de fondo de la ventana

        self.selected_file = ""  # Variable para almacenar la ruta del archivo seleccionado

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta de bienvenida
        self.welcome_label = Label(self, text="Bienvenido al Pipeline de Análisis Genómico",
                                   pady=10, bg='#f0f0f0', font=('Arial', 12, 'bold'))
        self.welcome_label.pack()

        # Botón para seleccionar archivo FASTA/FASTQ
        self.load_button = Button(self, text="Cargar Archivo FASTQ", command=self.load_file,
                                  bg='#333', fg='#fff', font=('Arial', 12, 'bold'), borderwidth=0)
        self.load_button.pack(fill=tk.X, padx=50, pady=10)

        # Etiqueta para mostrar la ruta del archivo seleccionado
        self.file_path_label = Label(self, text="No se ha seleccionado ningún archivo.",
                                     pady=10, bg='#f0f0f0', wraplength=300, justify="center")
        self.file_path_label.pack()

        # Botón para comenzar el análisis
        self.start_analysis_button = Button(self, text="Comenzar el Análisis", command=self.start_analysis,
                                            bg='#333', fg='#fff', font=('Arial', 12, 'bold'), borderwidth=0)
        self.start_analysis_button.pack(fill=tk.X, padx=50, pady=20)

    def load_file(self):
        file_types = [('FASTA/FASTQ files', '*.fasta *.fa *.fastq *.fq'), ('All files', '*.*')]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.selected_file = file_path
            self.file_path_label.config(text=f"Archivo Cargado: {file_path}")
        else:
            self.selected_file = ""
            
    def start_analysis(self):
        if not self.selected_file:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún archivo.")
        else:
            try:
                # Asume que el archivo seleccionado es un FASTQ 
                output_fastq_clean = "path/to/clean_output.fastq"  
                output_fastq_report = "path/to/fastp_report.html"
                run_fastp(self.selected_file, output_fastq_clean, output_fastq_report)
                messagebox.showinfo("Análisis Completado", "El control de calidad ha finalizado exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Se produjo un error durante el análisis: {e}")

if __name__ == "__main__":
    app = GenomeAnalysisApp()
    app.mainloop()
