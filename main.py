import os
import time
import threading
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk

OPEN_WEBUI_API_URL = "http://localhost:9090/api/chat/completions"  # Conectar con Open WebUI
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjZjYzYzOTdmLThhODItNDgzMy1iMjQ2LWU3YTY4OTNmMzBkMyJ9.IAZCthFCQRkD8Z63zp-tsA9MGscS_AwAOZEsHEDiTlE"  # Reemplazar con la API Key de Open WebUI

class TxtFileHandler(FileSystemEventHandler):
    def __init__(self, text_widget, model_var):
        self.text_widget = text_widget
        self.file_sizes = {}
        self.model_var = model_var  # Variable para el modelo seleccionado
    
    def on_created(self, event):
        if event.src_path.endswith(".txt"):
            self.check_txt_changes(event.src_path)
    
    def on_modified(self, event):
        if event.src_path.endswith(".txt"):
            self.check_txt_changes(event.src_path)
    
    def check_txt_changes(self, file_path):
        file_size = os.path.getsize(file_path) / 1024  # Tamaño en KB
        
        if file_path not in self.file_sizes or self.file_sizes[file_path] != file_size:
            self.file_sizes[file_path] = file_size
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:  # Solo mostrar si hay contenido
                self.text_widget.insert(tk.END, f"\nArchivo detectado/modificado: {file_path} ({file_size:.2f} KB)\n{content}\n{'-'*40}\n")
                self.text_widget.see(tk.END)
                self.send_to_open_webui(content)
    
    def send_to_open_webui(self, text):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_var.get(),  # Usar el modelo seleccionado
            "messages": [
                {"role": "user", "content": text}
            ]
        }
        try:
            response = requests.post(OPEN_WEBUI_API_URL, headers=headers, json=data)
            response_json = response.json()
            print("DEBUG: Response JSON:", response_json)  # Depuración en consola
            
            if response.status_code == 200 and "choices" in response_json:
                result = response_json["choices"][0]["message"]["content"]
                self.text_widget.insert(tk.END, f"\nRespuesta de {self.model_var.get()}:\n{result}\n{'-'*40}\n")
                self.text_widget.see(tk.END)
            else:
                self.text_widget.insert(tk.END, f"\nError en la respuesta de Open WebUI: {response.status_code}\n{response_json}\n")
        except Exception as e:
            self.text_widget.insert(tk.END, f"\nError al conectar con Open WebUI: {str(e)}\n")

def get_available_models():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get("http://localhost:9090/api/models", headers=headers)
    if response.status_code == 200:
        models = [model["id"] for model in response.json().get("data", [])]
        return models if models else ["No models found"]
    return ["No models found"]

def on_model_selected(event):
    text_output.insert(tk.END, f"\nConectado con {model_var.get()}\n{'-'*40}\n")
    text_output.see(tk.END)

def send_manual_prompt():
    user_prompt = prompt_entry.get()
    if user_prompt and handler:
        text_output.insert(tk.END, f"\nUsuario: {user_prompt}\n")
        text_output.see(tk.END)
        handler.send_to_open_webui(user_prompt)

def start_monitoring():
    global observer, folder_selected, handler
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        return
    
    text_output.insert(tk.END, f"Monitoreando carpeta: {folder_selected}\n{'-'*40}\n")
    text_output.see(tk.END)
    handler = TxtFileHandler(text_output, model_var)
    observer = Observer()
    observer.schedule(handler, folder_selected, recursive=False)
    observer.start()

def stop_monitoring():
    global observer
    if observer:
        observer.stop()
        observer.join()
        text_output.insert(tk.END, "\nMonitoreo detenido.\n")
        text_output.see(tk.END)

# Crear interfaz gráfica
root = tk.Tk()
root.title("Monitor de Archivos TXT")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(pady=10)

start_button = tk.Button(frame, text="Seleccionar carpeta y empezar", command=start_monitoring)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(frame, text="Detener monitoreo", command=stop_monitoring)
stop_button.pack(side=tk.LEFT, padx=5)

model_var = tk.StringVar()
available_models = get_available_models()
model_var.set(available_models[0])
model_dropdown = ttk.Combobox(root, textvariable=model_var, values=available_models)
model_dropdown.pack(pady=5)
model_dropdown.bind("<<ComboboxSelected>>", on_model_selected)

prompt_entry = tk.Entry(root, width=50)
prompt_entry.pack(pady=5)

send_button = tk.Button(root, text="Enviar Prompt", command=send_manual_prompt)
send_button.pack(pady=5)

text_output = scrolledtext.ScrolledText(root, width=80, height=20)
text_output.pack(padx=10, pady=10)

observer = None
folder_selected = ""
handler = None

root.mainloop()