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
from subprocess import call

class GenomeAnalysisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Genome Analysis Pipeline")
        self.geometry("700x400")  # Tamaño
        self.configure(bg='#202020')  # Color de fondo de la ventana
        self.selected_file = ""  # Variable para almacenar la ruta del archivo seleccionado
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.create_widgets()

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

        
        # Texto de progreso
        self.progress_label = Label(self, text="Ready to start...", bg='#202020', fg='#fff', font=('Arial', 12, 'bold'), padx=20, pady=10)
        self.progress_label.pack(side='bottom', fill='x')
        
        # Línea horizontal
        progress_line = tk.Canvas(self, height=2, bg='#555555', highlightthickness=0)
        progress_line.pack(fill='x', padx=20, pady=(0, 10),side='bottom',)
        
        # Botón para comenzar análisis
        self.start_analysis_button = Button(self, text="Start Analysis", command=self.start_analysis_thread,
                                            bg='#333', fg='#fff', font=('Arial', 12, 'bold'), relief='flat', borderwidth=0,
                                            highlightthickness=0, highlightbackground="#333", highlightcolor="#333", height=2, width=20)
        self.start_analysis_button.pack(expand=False, padx=100, pady=(0,40), side='bottom')
        
        # Texto de archivo
        self.file_path_label = Label(self, text="No file uploaded.",
                                    pady=10, bg='#202020', fg='#fff', wraplength=300, justify="center", font=('Arial', 11))
        self.file_path_label.pack(side='bottom',pady=(0,40))

        
        # Botón 1
        self.load_button = Button(self, text="Load FASTQ File", command=self.load_file,
                                bg='#333', fg='#fff', font=('Arial', 12, 'bold'), relief='flat', borderwidth=0,
                                highlightthickness=0, highlightbackground="#333", highlightcolor="#333", height=2, width=20)
        self.load_button.pack(expand=False, padx=100, pady=(50,15),side='bottom')





    def load_file(self):
        file_types = [('FASTQ files', '*.fasta *.fa *.fastq *.fq'), ('All files', '*.*')]
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            self.selected_file = file_path
            self.file_path_label.config(text=f"Archivo Cargado: {file_path}")
        else:
            self.selected_file = ""
            
          
            
    def start_analysis_thread(self):
        # Iniciar el análisis en un hilo separado para evitar bloquear la GUI
        analysis_thread = threading.Thread(target=self.start_analysis)
        analysis_thread.start()
            
            
            
            
    def start_analysis(self):
        if not self.selected_file:
            self.progress_label.config(text="Warning: No file selected")
        else:
            try:
                self.progress_label.config(text="Quality Control started..")
                output_fastq_clean = "./clean_output.fastq"
                output_fastq_report = "./fastp_report.html"
                run_fastp(self.selected_file, output_fastq_clean, output_fastq_report)
                

                # Ensamblaje con SPAdes
                self.progress_label.config(text="Quality Control finished, Assembly started...")
                spades_output_dir = "./spades_output"
                stdout, stderr, returncode = run_spades(output_fastq_clean, spades_output_dir)
                if returncode != 0:
                    messagebox.showerror("Error en SPAdes", f"SPAdes failed, error: {stderr}")
                    return
                
                
                # Anotacion con Prokka
                self.progress_label.config(text="Assembly finished. Annotation started...")
                prokka_output_dir = "./prokka_output"
                run_prokka(spades_output_dir, prokka_output_dir)
                
                
                # Deteccion con rgi
                self.progress_label.config(text="Annotation finished, looking for genes...")
                rgi_output_dir = "./rgi_output"
                run_rgi(prokka_output_dir + "/annotated_contigs.fna", rgi_output_dir)  
                self.progress_label.config(text="Analysis finished succesfully")
                
                self.show_results(rgi_output_dir + "/rgi_output.json")
            
            except Exception as e:
                messagebox.showerror("Error", f"There was an error during the analysis: {e}")
                
       
                
                    
    def show_results(self, json_file_path):
        #abre en pestana para mostrar los resultados
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not read JSON file: {e}")
            return

        results_window = tk.Toplevel(self)
        results_window.title("Results of Antimicrobial Resistant Genes Analysis")
        results_window.geometry("800x600")

        # Definir el Treeview
        tree = ttk.Treeview(results_window, columns=("RGI Criteria", "ARO Term", "Detection Criteria", "AMR Gene Family", "Drug Class", "Resistance Mechanism", "% Identity"), show="headings")
        tree.heading("RGI Criteria", text="RGI Criteria")
        tree.heading("ARO Term", text="ARO Term")
        tree.heading("Detection Criteria", text="Detection Criteria")
        tree.heading("AMR Gene Family", text="AMR Gene Family")
        tree.heading("Drug Class", text="Drug Class")
        tree.heading("Resistance Mechanism", text="Resistance Mechanism")
        tree.heading("% Identity", text="% Identity")

        # Ajustar el ancho de las columnas
        for col in tree["columns"]:
            tree.column(col, width=100)

        # Posicionar el Treeview en la ventana
        tree.pack(expand=True, fill="both")

        # Procesar y anadir los datos al Treeview
        for key, value in data.items():
            for sub_key, sub_value in value.items():
                rgi_criteria = sub_value.get("type_match", "N/A")
                perc_identity = sub_value.get("perc_identity", 0)  # Asumiendo un valor predeterminado de 0 si no se encuentra
                partial = sub_value.get("partial", "1")  # Asumiendo "1" como predeterminado para indicar genes parciales

                # Aplicar filtros
                if rgi_criteria in ["Perfect", "Strict", "Loose"] and partial == "0" and perc_identity >= 90:
                    # Extracción de la información relevante para cada columna
                    aro_term = sub_value.get("model_name", "N/A")
                    detection_criteria = sub_value.get("model_type", "N/A")
                    # Es necesario iterar por ARO_category para extraer 'AMR Gene Family', 'Drug Class', 'Resistance Mechanism'
                    amr_gene_family = ", ".join([v.get("category_aro_name", "N/A") for k, v in sub_value.get("ARO_category", {}).items() if "AMR Gene Family" in v.get("category_aro_class_name", "")])
                    drug_class = ", ".join([v.get("category_aro_name", "N/A") for k, v in sub_value.get("ARO_category", {}).items() if "Drug Class" in v.get("category_aro_class_name", "")])
                    resistance_mechanism = ", ".join([v.get("category_aro_name", "N/A") for k, v in sub_value.get("ARO_category", {}).items() if "Resistance Mechanism" in v.get("category_aro_class_name", "")])

                    # Insertar los datos que pasan los filtros en el Treeview
                    tree.insert("", tk.END, values=(rgi_criteria, aro_term, detection_criteria, amr_gene_family, drug_class, resistance_mechanism, perc_identity))
                            
    
    def close_app(self):
        # Metodo para cerrar la aplicacion
        self.destroy()

if __name__ == "__main__":
    app = GenomeAnalysisApp()
    app.mainloop()
