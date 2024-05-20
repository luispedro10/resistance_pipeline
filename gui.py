import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox, Tk, Canvas, PhotoImage, font
from quality_control import run_fastp
import threading  
from assembly import run_spades
from annotation import run_prokka
from resistance_detection import run_rgi
import json
from tkinter import ttk
import sys
from PyQt5.QtWidgets import QApplication
from results import ResultsWindow
import subprocess
from subprocess import call
import os

class GenomeAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genome Analysis Pipeline")
        self.geometry("750x480")  # Tamaño
        self.configure(bg='#202020')  # Color de fondo de la ventana
        self.selected_file = ""  # Variable para almacenar la ruta del archivo seleccionado
        self.selected_files = None
        self.output_directory = "./"  # Directorio de salida predeterminado
        self.identity_threshold = tk.StringVar(self)  # Asegúrate de pasar self aquí
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_app)
         
#   WIDGETS
    def create_widgets(self):  
        # Crear un Canvas para el fondo del título
        title_background = tk.Canvas(self, bg='#FFFFFF', height=60)  
        title_background.pack(fill='x', side='top')

        self.title_id = None

        # Título en el Canvas centrado
        title_text = "Antimicrobial Resistance Gene Detection Tool"
        def create_title(event):
            # Eliminar el objeto de texto anterior si existe
            if self.title_id is not None:
                title_background.delete(self.title_id)

            # Crear el nuevo texto del título
            self.title_id = title_background.create_text(
                title_background.winfo_width() / 2, 30,
                text=title_text,
                fill="black",
                font=('Helvetica', 16, 'bold'),
                anchor='center',
                width=title_background.winfo_width()
            )

        title_background.bind('<Configure>', create_title)
        
        
        # Botón para comenzar análisis
        self.start_analysis_button = Button(self, text="Start Analysis", command=self.start_analysis_thread,
                                            bg='#333', fg='#fff', font=('Arial', 12, 'bold'), relief='flat', borderwidth=0,
                                            highlightthickness=0, highlightbackground="#333", highlightcolor="#333", height=2, width=20)
        self.start_analysis_button.pack(expand=False, padx=100, pady=(0,20), side='bottom')
        

        # Texto de progreso
        self.progress_label = Label(self, text="Ready to start...", bg='#202020', fg='#fff', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.progress_label.pack(side='bottom', fill='x')
        
        
        # Línea horizontal
        progress_line = tk.Canvas(self, height=2, bg='#555555', highlightthickness=0)
        progress_line.pack(fill='x', padx=20, pady=(0, 10),side='bottom',)
        
        
        #Directorio de salida
        self.select_output_dir_button = Button(self, text="Select Output Directory", command=self.select_output_directory,
                                               bg='#333', fg='#fff', font=('Arial', 10, 'bold'), relief='flat', borderwidth=0,
                                               highlightthickness=0, highlightbackground="#333", highlightcolor="#333", height=1, width=25)
        self.select_output_dir_button.pack(side='bottom',expand=False, padx=100, pady=(10, 15))
       
        
        # Añadir un ComboBox para seleccionar el porcentaje de identidad
        identity_options = ttk.Combobox(self, textvariable=self.identity_threshold, values=["80%", "85%", "90%", "95%"], state='readonly')
        identity_options.set("90%")  # Valor por defecto
        identity_options.pack(side='bottom', pady=(0, 30))
        
        identity_label = Label(self, text="Identity Threshold:", bg='#202020', fg='#fff', font=('Arial', 11))
        identity_label.pack(side='bottom', pady=(0, 0))
        
        # Texto de archivo
        self.file_path_label = Label(self, text="No file uploaded.",
                                    pady=10, bg='#202020', fg='#fff', wraplength=300, justify="center", font=('Arial', 11))
        self.file_path_label.pack(side='bottom',pady=(0,30))

        
        # Botón 1
        self.load_button = Button(self, text="Load FASTQ File(s)", command=self.load_file,
                                bg='#333', fg='#fff', font=('Arial', 12, 'bold'), relief='flat', borderwidth=0,
                                highlightthickness=0, highlightbackground="#333", highlightcolor="#333", height=2, width=20)
        self.load_button.pack(expand=False, padx=100, pady=(0,0),side='bottom')
        
        


#OUTPUT
    def select_output_directory(self):
        # Abrir el diálogo para seleccionar el directorio
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory = directory
            messagebox.showinfo("Output Directory", f"Output directory set to: {directory}")


    def load_file(self):
        file_types = [('FASTQ files', '*.fasta *.fa *.fastq *.fq'), ('All files', '*.*')] 
        file_paths = filedialog.askopenfilenames(filetypes=file_types)  # Note el uso de askopenfilenames
        if file_paths:
            if len(file_paths) == 1:
                self.selected_file = file_paths[0]
                self.file_path_label.config(text=f"Archivo Cargado: {self.selected_file}")
            elif len(file_paths) == 2:
                self.selected_files = file_paths  # Almacenar ambos archivos
                self.file_path_label.config(text=f"Archivos Cargados: {', '.join(file_paths)}")
            else:
                messagebox.showerror("Error", "Please select one or two FASTQ files.")
                self.selected_file = ""
                self.selected_files = None
        else:
            self.selected_file = ""
            self.selected_files = None
                
          
            
    def start_analysis_thread(self):
        # Iniciar el análisis en un hilo separado para evitar bloquear la GUI
        analysis_thread = threading.Thread(target=self.start_analysis)
        analysis_thread.start()
     
     
     #KRAKEN       
    def run_kraken2(self, input_file, output_directory, database_path):
        kraken_output_dir = os.path.join(output_directory, "kraken_output")
        os.makedirs(kraken_output_dir, exist_ok=True)  # Asegura que el directorio existe
        
        output_file = os.path.join(kraken_output_dir, "kraken_report.txt")
        classified_out = os.path.join(kraken_output_dir, "classified_reads.fastq")
        unclassified_out = os.path.join(kraken_output_dir, "unclassified_reads.fastq")
        kraken_summary = os.path.join(kraken_output_dir, "kraken_summary.txt")

        command = [
            'kraken2',
            '--db', database_path,
            '--output', output_file,
            '--report', kraken_summary,
            '--classified-out', classified_out,
            '--unclassified-out', unclassified_out,
            input_file
        ]
        subprocess.run(command, check=True)
        print(f"Kraken2 analysis completed. Reports and reads saved to {kraken_output_dir}") 
            
            
    def start_analysis(self):
        if not self.selected_files and not self.selected_file:
            self.progress_label.config(text="Warning: No file selected")
            return  # Regresar si no hay archivos seleccionados

        try:
            
            #FASTP AND SPADES
            self.progress_label.config(text="Quality Control started..")
            if self.selected_files and len(self.selected_files) == 2:  # Si se seleccionaron dos archivos
                input_fastq1, input_fastq2 = self.selected_files
                output_fastq_clean1 = f"{self.output_directory}/clean_output_R1.fastq"
                output_fastq_clean2 = f"{self.output_directory}/clean_output_R2.fastq"
                output_fastq_report = f"{self.output_directory}/fastp_report.html"
                run_fastp(input_fastq1, output_fastq_clean1, output_fastq_report, input_fastq2, output_fastq_clean2)

                # Ensamblaje con SPAdes para lecturas pareadas
                self.progress_label.config(text="Quality Control finished, Assembly started...")
                spades_output_dir = f"{self.output_directory}/spades_output"
                stdout, stderr, returncode = run_spades(output_fastq_clean1, spades_output_dir, output_fastq_clean2)
            else:  # Si solo se seleccionó un archivo
                output_fastq_clean = f"{self.output_directory}/clean_output.fastq"
                output_fastq_report = f"{self.output_directory}/fastp_report.html"
                run_fastp(self.selected_file, output_fastq_clean, output_fastq_report)

                # Ensamblaje con SPAdes para una sola lectura
                self.progress_label.config(text="Quality Control finished, Assembly started...")
                spades_output_dir = f"{self.output_directory}/spades_output"
                stdout, stderr, returncode = run_spades(output_fastq_clean, spades_output_dir)
            
            if returncode != 0:
                messagebox.showerror("Error en SPAdes", f"SPAdes failed, error: {stderr}")
                return
            
            
            #Kraken
            kraken_db_path = "./kraken"
            self.progress_label.config(text="Assembly finished. Running genomic classification analysis...")
            self.run_kraken2(f"{spades_output_dir}/contigs.fasta", self.output_directory, kraken_db_path)
            
            
            
            # Anotación con Prokka
            self.progress_label.config(text="Genomic classification analysis finished. Annotation started...")
            prokka_output_dir = f"{self.output_directory}/prokka_output"
            run_prokka(spades_output_dir, prokka_output_dir)
            
            
            
            # Detección con RGI
            self.progress_label.config(text="Annotation finished, looking for genes...")
            rgi_output_dir = f"{self.output_directory}/rgi_output"
            run_rgi(prokka_output_dir + "/annotated_contigs.fna", rgi_output_dir)  
            self.progress_label.config(text="Analysis finished successfully")
            
            identity_percent = self.identity_threshold.get().strip('%')
            print("Identity Threshold set to:", identity_percent)
            rgi_output_json_path = f"{self.output_directory}/rgi_output/rgi_output.json"
            subprocess.Popen(["python", "results.py", rgi_output_json_path, identity_percent])
            
        except Exception as e:
            messagebox.showerror("Error", f"There was an error during the analysis: {e}")


                
       
                            
    
    def close_app(self):
        # Metodo para cerrar la aplicacion
        self.destroy()

if __name__ == "__main__":
    app = GenomeAnalysisApp()
    app.mainloop()
