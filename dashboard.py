import tkinter as tk
import json

def load_rgi_results(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

def display_dashboard(data):
    dashboard = tk.Toplevel()
    dashboard.title("RGI Analysis Dashboard")
    dashboard.geometry("600x400")

    tk.Label(dashboard, text="RGI Analysis Results", font=("Arial", 16)).pack(pady=10)

    for key, value in data.items():
        gene_info = f"Gene: {key}\nType Match: {value['gnl|BL_ORD_ID|150|hsp_num:0']['type_match']}\nModel Name: {value['gnl|BL_ORD_ID|150|hsp_num:0']['model_name']}"
        tk.Label(dashboard, text=gene_info, font=("Arial", 12), justify=tk.LEFT).pack(anchor="w", padx=10, pady=5)

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Genome Analysis Pipeline")
    app.geometry("400x300")
    
    def show_dashboard():
        json_path = "./rgi_output/rgi_output.json"  # Ajusta esta ruta según sea necesario
        rgi_data = load_rgi_results(json_path)
        display_dashboard(rgi_data)
    
    tk.Button(app, text="Show RGI Dashboard", command=show_dashboard).pack(pady=20)
    
    app.mainloop()
