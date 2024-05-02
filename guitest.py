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