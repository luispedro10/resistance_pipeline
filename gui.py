import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from quality_control import run_fastp
from assembly import run_spades


class GenomeAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genome Analysis Pipeline")
        self.geometry("400x300")  # Tamaño
        self.configure(bg='#f0f0f0')  # Color de fondo de la ventana

        self.selected_file = ""  # Variable para almacenar la ruta del archivo seleccionado
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        # Widgets
        self.create_widgets()

    def create_widgets(self):
        # Etiqueta de bienvenida
        self.welcome_label = Label(self, text="Bienvenido al Pipeline de Análisis Genómico",
                                   pady=10, bg='#f0f0f0', font=('Arial', 12, 'bold'))
        self.welcome_label.pack()

        # Boton para seleccionar archivo FASTA/FASTQ
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
                output_fastq_clean = "./clean_output.fastq"  
                output_fastq_report = "./fastp_report.html"
                run_fastp(self.selected_file, output_fastq_clean, output_fastq_report)
                
                spades_output_dir = "./spades_output"
                stdout, stderr, returncode = run_spades(output_fastq_clean, spades_output_dir)
                
                if returncode != 0:  # Verificar si hubo un error en SPAdes
                    messagebox.showerror("Error en SPAdes", f"SPAdes falló con el error: {stderr}")
                else:
                    messagebox.showinfo("SPAdes completado", "El ensamblaje con SPAdes ha finalizado exitosamente.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Se produjo un error durante el análisis: {e}")
                
                
    
    def close_app(self):
        # Método para cerrar la aplicación
        self.destroy()

if __name__ == "__main__":
    app = GenomeAnalysisApp()
    app.mainloop()
