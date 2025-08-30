import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import requests
import threading
import subprocess
import sys
from datetime import datetime

class MiApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mi Primera App")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # URLs de configuración (CAMBIAR POR TUS URLs DE GITHUB)
        self.config_url = "https://raw.githubusercontent.com/JacoboBN/MiPrimeraApp/main/config.json"
        self.app_url = "https://raw.githubusercontent.com/JacoboBN/MiPrimeraApp/main/main.py"
        
        self.user_data_file = "user_data.json"
        self.version_file = "version.txt"
        
        # Verificar actualizaciones al iniciar
        self.check_updates()
        
        # Cargar o solicitar datos del usuario
        self.setup_ui()
        
    def check_updates(self):
        """Verifica si hay actualizaciones disponibles"""
        try:
            # Obtener versión remota
            response = requests.get(self.config_url, timeout=5)
            if response.status_code == 200:
                remote_config = response.json()
                remote_version = remote_config.get("version", "1.0.0")
                
                # Obtener versión local
                local_version = self.get_local_version()
                
                if remote_version != local_version:
                    self.update_app(remote_version)
                    
        except Exception as e:
            print(f"No se pudo verificar actualizaciones: {e}")
    
    def get_local_version(self):
        """Obtiene la versión local de la aplicación"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r') as f:
                    return f.read().strip()
        except:
            pass
        return "1.0.0"
    
    def update_app(self, new_version):
        """Actualiza la aplicación descargando nuevo código"""
        try:
            # Descargar nueva versión del código
            response = requests.get(self.app_url)
            if response.status_code == 200:
                # Guardar nueva versión
                with open("main_new.py", 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                # Actualizar archivo de versión
                with open(self.version_file, 'w') as f:
                    f.write(new_version)
                
                # Mostrar mensaje de actualización
                self.show_update_message()
                
        except Exception as e:
            print(f"Error al actualizar: {e}")
    
    def show_update_message(self):
        """Muestra mensaje de actualización disponible"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg="#e3f2fd")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Icono de actualización (usando texto)
        icon_label = tk.Label(main_frame, text="🔄", font=("Arial", 48), bg="#e3f2fd")
        icon_label.pack(pady=20)
        
        # Mensaje
        update_text = "¡Actualización disponible!\n\nSe ha descargado una nueva versión.\nReinicia la aplicación para aplicar los cambios."
        update_label = tk.Label(main_frame, text=update_text, 
                               font=("Arial", 12), 
                               bg="#e3f2fd", fg="#1976d2",
                               justify="center")
        update_label.pack(pady=20)
        
        # Botón para reiniciar manualmente
        restart_btn = tk.Button(main_frame, text="Reiniciar ahora", 
                               font=("Arial", 12, "bold"),
                               bg="#2196F3", fg="white",
                               padx=20, pady=10,
                               command=self.manual_restart)
        restart_btn.pack(pady=10)
        
        # Botón para continuar sin actualizar
        continue_btn = tk.Button(main_frame, text="Continuar con versión actual", 
                                font=("Arial", 10),
                                command=self.continue_without_update)
        continue_btn.pack(pady=5)
    
    def manual_restart(self):
        """Reinicia manualmente la aplicación"""
        try:
            # Ejecutar nueva versión si existe
            if os.path.exists("main_new.py"):
                subprocess.Popen([sys.executable, "main_new.py"])
            sys.exit()
        except Exception as e:
            print(f"Error al reiniciar: {e}")
            # Si falla, continuar normal
            self.continue_without_update()
    
    def continue_without_update(self):
        """Continúa sin actualizar"""
        self.setup_ui()
    
    def load_user_data(self):
        """Carga los datos del usuario desde archivo local"""
        if os.path.exists(self.user_data_file):
            try:
                with open(self.user_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def save_user_data(self, name, birth_year):
        """Guarda los datos del usuario localmente"""
        data = {
            "name": name,
            "birth_year": birth_year,
            "saved_date": datetime.now().isoformat()
        }
        with open(self.user_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def calculate_age(self, birth_year):
        """Calcula la edad actual"""
        current_year = datetime.now().year
        return current_year - birth_year
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        user_data = self.load_user_data()
        
        if user_data:
            # Usuario ya registrado - mostrar saludo
            self.show_greeting(user_data["name"], user_data["birth_year"])
        else:
            # Nuevo usuario - solicitar datos
            self.show_registration()
    
    def show_registration(self):
        """Muestra el formulario de registro"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Título
        title_label = tk.Label(self.root, text="¡Bienvenido!", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Frame para el formulario
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=20)
        
        # Campo nombre
        tk.Label(form_frame, text="Tu nombre:", font=("Arial", 12)).pack(pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.name_entry.pack(pady=5)
        
        # Campo año de nacimiento
        tk.Label(form_frame, text="Año de nacimiento:", font=("Arial", 12)).pack(pady=5)
        self.year_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.year_entry.pack(pady=5)
        
        # Botón guardar
        save_btn = tk.Button(form_frame, text="Guardar", font=("Arial", 12), 
                            bg="#4CAF50", fg="white", command=self.save_data)
        save_btn.pack(pady=20)
        
        # Focus en el primer campo
        self.name_entry.focus()
        
        # Enter para continuar
        self.root.bind('<Return>', lambda event: self.save_data())
    
    def save_data(self):
        """Guarda los datos ingresados"""
        name = self.name_entry.get().strip()
        year_text = self.year_entry.get().strip()
        
        # Validaciones
        if not name:
            messagebox.showerror("Error", "Por favor ingresa tu nombre")
            return
        
        try:
            birth_year = int(year_text)
            current_year = datetime.now().year
            
            if birth_year < 1900 or birth_year > current_year:
                messagebox.showerror("Error", f"Por favor ingresa un año válido (1900-{current_year})")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un año válido (solo números)")
            return
        
        # Guardar datos
        self.save_user_data(name, birth_year)
        
        # Mostrar saludo
        self.show_greeting(name, birth_year)
    
    def show_greeting(self, name, birth_year):
        """Muestra el saludo personalizado"""
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        age = self.calculate_age(birth_year)
        
        # Marco principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mensaje de saludo
        greeting_text = f"BUENASSSSSS {name}!\n\nTienes {age} años"
        greeting_label = tk.Label(main_frame, text=greeting_text, 
                                 font=("Arial", 18, "bold"), 
                                 bg="#f0f0f0", fg="#2196F3")
        greeting_label.pack(expand=True)
        
        # Botón para cambiar datos
        change_btn = tk.Button(main_frame, text="Cambiar mis datos", 
                              font=("Arial", 10), command=self.reset_data)
        change_btn.pack(pady=10)
        
        # Información de versión (opcional)
        version = self.get_local_version()
        version_label = tk.Label(main_frame, text=f"Versión: {version}", 
                                font=("Arial", 8), bg="#f0f0f0", fg="gray")
        version_label.pack(side="bottom")
    
    def reset_data(self):
        """Elimina los datos guardados y vuelve al registro"""
        if os.path.exists(self.user_data_file):
            os.remove(self.user_data_file)
        self.show_registration()
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MiApp()
    app.run()