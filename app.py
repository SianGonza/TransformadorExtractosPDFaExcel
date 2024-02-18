import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from src.process_extractos_credicoop import convertir_extracto_credicoop
from src.procesar_extractos_meridian import convertir_extractos_meridian
from src.procesar_extractos_santander import convertir_extractos_santander
from src.procesar_extracto_provincia import convertir_extractos_provincia
from src.procesar_extracto_masventas import convertir_extractos_masventas
from src.procesar_extractos_galicia import convertir_extractos_galicia
from src.procesar_exctractos_nacion import convertir_extractos_nacion
from src.procesar_extracto_icbc import convertir_extractos_icbc
from src.procesar_extracto_icbc_mati import convertir_extractos_icbc_mati
from src.procesar_extractos_bind import convertir_extractos_bind
from src.procesar_extractos_frances import convertir_extractos_frances
from src.procesar_extractos_ciudad import convertir_extractos_ciudad
from src.procesar_extractos_HSBC import convertir_extractos_hsbc
from src.procesar_extractos_galicia_2022 import convertir_extractos_galicia_2022
from src.procesar_extractos_comercio import convertir_extractos_comercio
from src.procesar_extractos_macro import convertir_extractos_macro
from src.procesar_extracto_provincia_harlye import convertir_extractos_provincia_harlye
import time


def transformar_pdf(selected_tarjeta, carpeta_pdf):
    if selected_tarjeta == "Credicoop":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extracto_credicoop(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Meridian":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_meridian(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Santander":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_santander(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Provincia":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_provincia(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "MasVentas":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_masventas(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Galicia":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_galicia(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Nacion":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_nacion(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "ICBC":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_icbc(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Bind":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_bind(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Frances":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_frances(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Ciudad":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_ciudad(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "HSBC":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_hsbc(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Galicia 2022":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_galicia_2022(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Comercio":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_comercio(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Macro":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_macro(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "Provincia Formato 2":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_provincia_harlye(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")

    if selected_tarjeta == "ICBC Formato 2":
        if not os.path.exists(carpeta_pdf):
            messagebox.showerror("Error", f"La carpeta {carpeta_pdf} no existe.")

        # Llama directamente a la función de transformación del módulo
        convertir_extractos_icbc_mati(carpeta_pdf)

        # Muestra un mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF de {selected_tarjeta} transformado con éxito!")


class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Transformación de PDF a Excel")
        self.window.geometry("900x450")
        self.window.minsize(width=600, height=400)

        # --- ESTILO ---
        # Tema personalizado con accesibilidad y contraste adecuados
        style = ttk.Style()
        style.theme_create("custom", parent="vista", settings={
            "TLabel": {
                "font": ("Helvetica", 12),
                "foreground": "#333",
            },
            "TButton": {
                "font": ("Helvetica", 12),
                "foreground": "#fff",
                "background": "#0078D7",
                "borderwidth": 1,
                "relief": "raised",
            },
            "TEntry": {
                "font": ("Helvetica", 12),
                "foreground": "#333",
                "background": "#fff",
                "borderwidth": 1,
                "relief": "solid",
            },
            "TCombobox": {
                "font": ("Helvetica", 12),
                "foreground": "#333",
                "background": "#fff",
                "borderwidth": 1,
                "relief": "solid",
            },
            "TFrame": {
                "borderwidth": 0,
                "relief": "flat",
            },
            "TProgressbar": {
                "troughcolor": "#ddd",
                "bordercolor": "#ccc",
                "background": "#0078D7",
            },
            "TListbox": {
                "font": ("Helvetica", 12),
                "foreground": "#333",
                "background": "#fff",
                "borderwidth": 1,
                "relief": "solid",
                "highlightthickness": 0,  # Eliminar borde de enfoque
            },
            "TScrollbar": {
                "troughcolor": "#ddd",
                "bordercolor": "#ccc",
                "background": "#ddd",
                "arrowcolor": "#777",
            },
        })
        style.theme_use("custom")

        # Marco principal
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- IZQUIERDA ---

        # Sección de selección de carpeta
        self.carpeta_frame = ttk.Frame(self.main_frame, padding="10")
        self.carpeta_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Agregar un título en el sector izquierdo
        self.titulo_label = ttk.Label(self.carpeta_frame, text="Transformador PDF a Excel", font=("Helvetica", 14))
        self.titulo_label.pack(anchor=tk.W, pady=10)

        self.carpeta_label = ttk.Label(self.carpeta_frame, text="Selecciona la carpeta de PDF:")
        self.carpeta_label.pack(anchor=tk.W)

        self.carpeta_entry = ttk.Entry(self.carpeta_frame, width=40)
        self.carpeta_entry.pack(anchor=tk.W, pady=5)

        # Botón para seleccionar carpeta
        self.seleccionar_carpeta_button = ttk.Button(
            self.carpeta_frame,
            text="Seleccionar Carpeta",
            command=self.seleccionar_carpeta_pdf
        )
        self.seleccionar_carpeta_button.pack(anchor=tk.W, pady=10)

        self.search_frame = ttk.Frame(self.carpeta_frame, padding="10")
        self.search_frame.pack(anchor=tk.W, fill=tk.X)

        self.search_label = ttk.Label(self.search_frame, text="Buscar banco:")
        self.search_label.pack(side=tk.LEFT)

        self.search_entry = ttk.Entry(self.search_frame, width=20, font=("Helvetica", 12))
        self.search_entry.pack(side=tk.LEFT)

        self.search_entry.bind("<KeyRelease>", self.on_search)

        # Sección de selección de tarjeta

        # Selección de banco con Listbox y scrollbar
        self.tarjetas_frame = ttk.Frame(self.carpeta_frame, padding="10")
        self.tarjetas_frame.pack(anchor=tk.W, fill=tk.Y)

        self.tarjetas_label = ttk.Label(self.tarjetas_frame, text="Selecciona Banco:", font=("Helvetica", 12))
        self.tarjetas_label.pack(anchor=tk.W)

        self.tarjetas = ["Credicoop", "Meridian", "Galicia", "ICBC", "ICBC Formato 2", "MasVentas",
                         "Nacion", "Bind", "Provincia", "Provincia Formato 2", "Macro",
                         "Frances", "Santander", "Ciudad", "Comercio", "Galicia 2022", "HSBC"]

        self.tarjeta_var = tk.StringVar()

        self.scrollbar = ttk.Scrollbar(self.tarjetas_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tarjeta_list = tk.Listbox(self.tarjetas_frame, yscrollcommand=self.scrollbar.set, height=10,
                                       font=("Helvetica", 12))
        for tarjeta in self.tarjetas:
            self.tarjeta_list.insert(tk.END, tarjeta)
        self.tarjeta_list.pack(anchor=tk.W)

        self.tarjeta_list.bind("<<ListboxSelect>>", self.on_select)

        # Botón para iniciar la transformación
        self.transformar_button = ttk.Button(
            self.main_frame,
            text="Transformar PDF",
            command=self.transformar
        )
        self.transformar_button.pack(side=tk.BOTTOM, pady=20)

        # --- DERECHA ---

        # Sección de progreso
        self.progress_frame = ttk.Frame(self.main_frame, padding="10")
        self.progress_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=200, mode="indeterminate")
        self.progress_bar.pack(anchor=tk.W)

        self.text_widget = tk.Text(self.progress_frame, height=20, width=60, font=("Helvetica", 12))

        self.text_widget.pack(anchor=tk.W)

    # --- FUNCIONES ---

    def on_search(self, event):
        search_text = self.search_entry.get().lower()
        self.tarjeta_list.delete(0, tk.END)
        for tarjeta in self.tarjetas:
            if search_text in tarjeta.lower():
                self.tarjeta_list.insert(tk.END, tarjeta)

    def on_select(self, event):
        selected_tarjeta = self.tarjeta_list.get(self.tarjeta_list.curselection()[0])
        print(selected_tarjeta)

    def seleccionar_carpeta_pdf(self):
        carpeta_pdf = filedialog.askdirectory()
        self.carpeta_entry.delete(0, tk.END)
        self.carpeta_entry.insert(0, carpeta_pdf)

    def transformar(self):
        selected_tarjeta = self.tarjeta_list.get(self.tarjeta_list.curselection()[0])

        # selected_tarjeta = self.tarjeta_var.get()
        carpeta_pdf = self.carpeta_entry.get()

        if not selected_tarjeta or not carpeta_pdf:
            messagebox.showerror("Error", "Selecciona una tarjeta y una carpeta PDF primero.")

        else:
            self.text_widget.delete(1.0, tk.END)  # Limpiar el área de progreso
            self.text_widget.insert(tk.END, f"Transformando PDF de {selected_tarjeta}...\n")
            self.window.update()  # Actualizar la interfaz gráfica para que se muestre el mensaje
            self.progress_bar.start()  # Iniciar la barra de progreso
            # transformar_pdf(selected_tarjeta, carpeta_pdf)
            # self.progress_bar.stop()  # Detener la barra de progreso
            # self.text_widget.insert(tk.END, f"\nTransformación completa para {selected_tarjeta}.\n")

        hilo_transformar = threading.Thread(target=self.transformar_en_hilo, args=(selected_tarjeta, carpeta_pdf))
        hilo_transformar.start()

        # Actualizar la UI periódicamente
        while hilo_transformar.is_alive():
            self.text_widget.insert(tk.END, ".")  # Mostrar progreso
            self.window.update()
            time.sleep(0.1)  # Esperar un poco

        # Hilo finalizado
        self.text_widget.insert(tk.END, f"\nTransformación completa para {selected_tarjeta}.\n")

    def transformar_en_hilo(self, selected_tarjeta, carpeta_pdf):
        """
        Función que ejecuta la transformación en un hilo independiente.
        """
        transformar_pdf(selected_tarjeta, carpeta_pdf)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
