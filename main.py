import tkinter as tk
from tkinter import ttk


class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.geometry("1080x720")

        # variables para toda la app
        self.automata_de_pila = {}
        self.simbolos_entrada = []
        self.simbolos_pila = []
        self.configuracion_inicial = ["▼"]
        self.transicion = ""
        self.input_position = 0

        self.pila = []
        self.secuencia = ""
        self.posicion_secuencia = 0

        # Componentes de la UI
        self.ls_entrada = tk.Label(self, text="Ingrese los simbolos de entrada separados por espacios:")
        self.ls_entrada.grid(column=0, row=0, pady=10, padx=10, sticky="w")

        self.ls_pila = tk.Label(self, text="Ingrese los simbolos de pila separados por espacios:")
        self.ls_pila.grid(column=0, row=1, pady=10, padx=10, sticky="w")

        self.lc_inicial = tk.Label(self, text="Ingrese la configuración inicial de la pila:")
        self.lc_inicial.grid(column=0, row=2, pady=10, padx=10, sticky="w")

        self.grid_columnconfigure(1, weight=1)
        self.s_entrada = tk.Entry(self)
        self.s_entrada.grid(column=1, row=0, pady=10, padx=10, sticky="ew")

        self.s_pila = tk.Entry(self)
        self.s_pila.grid(column=1, row=1, pady=10, padx=10, sticky="ew")

        self.c_inicial = tk.Entry(self)
        self.c_inicial.grid(column=1, row=2, pady=10, padx=10, sticky="ew")

        self.ingresar_automata = tk.Button(self, text="Ingresar automata",
                                           command=lambda: self.read_ap(self.s_entrada.get(), self.s_pila.get(),
                                                                        self.c_inicial.get()))
        self.ingresar_automata.grid(column=0, row=3, pady=20, padx=10, sticky="e")

    # Lectura de los simbolos de entrada y de pila y la configuración inicial del automata
    def read_ap(self, s_entrada, s_pila, c_inicial):
        self.input_position = 0
        self.automata_de_pila = {}
        self.simbolos_entrada = s_entrada.split()
        self.simbolos_pila = s_pila.split()
        simbolos = c_inicial.split()
        for simbolo in simbolos:
            self.configuracion_inicial.append(simbolo)
        print(self.simbolos_entrada, self.simbolos_pila, self.configuracion_inicial)

        self.vl_transiciones = tk.StringVar(
            value=f"Ingrese las transiciones de {self.simbolos_pila[0]} para cada símbolo de "
                  f"entrada ({','.join(self.simbolos_entrada)}):")
        self.l_transiciones = tk.Label(self, textvariable=self.vl_transiciones)
        self.l_transiciones.grid(column=0, row=4, pady=20, padx=10, sticky="w")

        self.transiciones = tk.Entry(self)
        self.transiciones.grid(column=1, row=4, pady=10, padx=10, sticky="ew")

        self.v_ingresar_transicion = tk.StringVar(value="Ingresar transiciones")
        self.ingresar_transicion = tk.Button(self, textvariable=self.v_ingresar_transicion,
                                             command=lambda: self.input_simbol_transitions(
                                                 self.transiciones.get()))
        self.ingresar_transicion.grid(column=0, row=5, pady=20, padx=10, sticky="e")

    # Se leen las transiciones del automata ingresadas por el usuario
    def input_simbol_transitions(self, transiciones):
        if self.input_position > len(self.simbolos_pila):
            self.ingresar_transicion.destroy()
            self.l_transiciones.destroy()
            self.transiciones.destroy()
            del self.vl_transiciones
            self.input_position = 0
            self.show_automata_de_pila()
        else:
            # ▼ significa pila vacia
            transiciones = transiciones.split()

            #Control transiciones
            for trans in transiciones:
                if trans[0] not in ["A", "R", "D", "a", "r"] or trans[-1] not in ["R", "A", "a", "r"] or (trans[-1] in ["R", "A"] and len(trans) != 1):
                    transiciones_error = tk.Toplevel(app)
                    self.l_error = tk.Label(transiciones_error, text="Hubo un error al ingresar las transiciones, por favor reintentar:")
                    self.l_error.grid(column=0, row=0, pady=10, padx=10, sticky="w")
                    return

            simbolo = "▼"
            self.vl_transiciones.set(
                f"Ingrese las transiciones de ▼ para cada símbolo de entrada ({','.join(self.simbolos_entrada)}):")
            if self.input_position != len(self.simbolos_pila):
                simbolo = self.simbolos_pila[self.input_position]

            if len(transiciones) == len(self.simbolos_entrada):
                transicion = self.automata_de_pila[simbolo] = {}
                for entrada in self.simbolos_entrada:
                    transicion[entrada] = transiciones[self.simbolos_entrada.index(entrada)]

                self.input_position += 1
                if self.input_position == len(self.simbolos_pila):
                    self.v_ingresar_transicion.set("Terminar transiciones")
                print(self.automata_de_pila)
                if self.input_position < len(self.simbolos_pila):
                    self.vl_transiciones.set(
                        f"Ingrese las transiciones de {self.simbolos_pila[self.input_position]} para cada símbolo de "
                        f"entrada ({','.join(self.simbolos_entrada)}):")
            else:
                transiciones_error = tk.Toplevel(app)
                self.l_error = tk.Label(transiciones_error,
                                        text="Hubo un error al ingresar las transiciones, por favor reintentar:")
                self.l_error.grid(column=0, row=0, pady=10, padx=10, sticky="w")
                return

    # se adapta y se muestra al usuario el automata de pila, la notación es igual a la de el profe Roberto Florez
    def show_automata_de_pila(self):
        ventana_show = tk.Toplevel(app)
        self.simbolos_pila.append("▼")
        print(self.automata_de_pila)
        for entrada in self.simbolos_entrada:
            self.celda = tk.Label(ventana_show, text=entrada)
            self.celda.grid(column=self.simbolos_entrada.index(entrada)+1, row=0, pady=5, padx=5)
        for simbolo_pila in self.simbolos_pila:
            self.celda = tk.Label(ventana_show, text=simbolo_pila)
            self.celda.grid(column=0, row=self.simbolos_pila.index(simbolo_pila)+1, pady=5, padx=5)
        for row in range(1, len(self.simbolos_pila) + 1):
            for column in range(1, len(self.simbolos_entrada) + 1):
                self.celda = tk.Label(ventana_show, text=self.automata_de_pila[self.simbolos_pila[row-1]][self.simbolos_entrada[column-1]])
                self.celda.grid(column=column, row=row, pady=5, padx=5)
        try:
            self.ls_entrada.destroy()
            self.ls_pila.destroy()
            self.lc_inicial.destroy()
            self.s_entrada.destroy()
            self.s_pila.destroy()
            self.c_inicial.destroy()
            self.ingresar_automata.destroy()
        except:
            pass

        try:
            self.edit_bs_entrada in locals()
        except:
            self.edit_bs_entrada = tk.Button(self, text="cambiar símbolos de entrada", command=lambda: self.update_entry_simbols())
            self.edit_bs_entrada.grid(column=1, row=0, pady=10, padx=10, sticky="w")

            self.edit_bs_pila = tk.Button(self, text="cambiar símbolos de pila", command=lambda:self.update_stack_simbols())
            self.edit_bs_pila.grid(column=1, row=1, pady=10, padx=10, sticky="w")

            self.edit_bc_inicial = tk.Button(self, text="cambiar configuración inicial", command=lambda:self.update_ci())
            self.edit_bc_inicial.grid(column=1, row=2, pady=10, padx=10, sticky="w")

            self.edit_b_transicion = tk.Button(self, text="cambiar transición",
                                             command=lambda: self.update_transicion())
            self.edit_b_transicion.grid(column=1, row=3, pady=10, padx=10, sticky="w")

            self.edit_s_entrada = tk.Entry(self)
            self.edit_s_entrada.grid(column=0, row=0, pady=10, padx=10, sticky="ew")

            self.edit_s_pila = tk.Entry(self)
            self.edit_s_pila.grid(column=0, row=1, pady=10, padx=10, sticky="ew")

            self.edit_c_inicial = tk.Entry(self)
            self.edit_c_inicial.grid(column=0, row=2, pady=10, padx=10, sticky="ew")

            self.edit_transicion = tk.Entry(self)
            self.edit_transicion.grid(column=0, row=3, pady=10, padx=10, sticky="ew")

            self.ingresar_b_secuencia = tk.Button(self, text="Ingresar secuencia",
                                               command=lambda: self.entry_secuencia())
            self.ingresar_b_secuencia.grid(column=1, row=4, pady=20, padx=10, sticky="w")

            self.ingresar_secuencia = tk.Entry(self)
            self.ingresar_secuencia.grid(column=0, row=4, pady=20, padx=10, sticky="ew")


    # Función para cambiar los simbolos de entrada
    def update_entry_simbols(self):
        simbolos_entrada = self.edit_s_entrada.get().split()
        if len(simbolos_entrada) != len(self.simbolos_entrada):
            transiciones_error = tk.Toplevel(app)
            self.l_error = tk.Label(transiciones_error,
                                    text="Hubo un error al ingresar los símbolos de entrada, por favor reintentar:")
            self.l_error.grid(column=0, row=0, pady=10, padx=10, sticky="w")
        else:

            for key in self.simbolos_pila:
                for entrada in self.simbolos_entrada:
                    self.automata_de_pila[key][simbolos_entrada[self.simbolos_entrada.index(entrada)]] = self.automata_de_pila[key].pop(entrada)
            self.simbolos_entrada = simbolos_entrada
            self.simbolos_pila.pop()
            self.show_automata_de_pila()

    # Función para cambiar los símbolos de pila
    def update_stack_simbols(self):
        simbolos_pila = self.edit_s_pila.get().split()
        if len(simbolos_pila) != len(self.simbolos_pila)-1:
            transiciones_error = tk.Toplevel(app)
            self.l_error = tk.Label(transiciones_error,
                                    text="Hubo un error al ingresar los símbolos de pila, por favor reintentar:")
            self.l_error.grid(column=0, row=0, pady=10, padx=10, sticky="w")
        else:
            simbolos_pila.append("▼")
            for key in self.simbolos_pila:
                self.automata_de_pila[simbolos_pila[self.simbolos_pila.index(key)]] = self.automata_de_pila.pop(key)
            self.simbolos_pila = simbolos_pila[:-1]
            self.show_automata_de_pila()

    # Función para cambiar la configuración inicial
    def update_ci(self):
        simbolos = self.edit_c_inicial.get().split()
        self.configuracion_inicial = ["▼"]
        for simbolo in simbolos:
            self.configuracion_inicial.append(simbolo)

    # Función para cambiar una transición
    def update_transicion(self):
        ruta_transicion = self.edit_transicion.get().split()
        if len(ruta_transicion) != 3:
            self.error_transiciones()
        else:
            simbolo_pila = ruta_transicion[0]
            simbolo_entrada = ruta_transicion[1]
            trans = ruta_transicion[2]
            if simbolo_pila not in self.simbolos_pila:
                self.error_transiciones()
            elif simbolo_entrada not in self.simbolos_entrada:
                self.error_transiciones()
            elif trans[0] not in ["A", "R", "D", "a", "r"] or trans[-1] not in ["R", "A", "a", "r"] or (trans[-1] in ["R", "A"] and len(trans) != 1):
                self.error_transiciones()
            else:
                self.automata_de_pila[simbolo_pila][simbolo_entrada] = trans
                self.show_automata_de_pila()

    # Función para leer la secuencia que el usuario desee ingresar para su AP
    def entry_secuencia(self):
        self.secuencia = self.ingresar_secuencia.get()
        try:
            self.edit_bs_entrada.destroy()
            self.edit_s_entrada.destroy()
            self.edit_transicion.destroy()
            self.edit_b_transicion.destroy()
            self.edit_c_inicial.destroy()
            self.edit_bc_inicial.destroy()
            self.edit_s_pila.destroy()
            self.edit_bs_pila.destroy()
            self.ingresar_secuencia.destroy()
            self.ingresar_b_secuencia.destroy()
        except:
            pass
        for value in self.configuracion_inicial:
            self.pila.append(value)
        self.leer_secuencia = tk.StringVar(value="Próximo valor a leer: (" + self.secuencia[self.posicion_secuencia] + "), símbolo más alto en la pila: (" + self.pila[-1] + ")")

        self.ls_pila = tk.Label(self,  textvariable=self.leer_secuencia)
        self.ls_pila.grid(column=0, row=5, pady=10, padx=10, sticky="e")

        self.ls_pila = tk.Label(self, text="secuencia ingresada: " + self.secuencia)
        self.ls_pila.grid(column=0, row=4, pady=10, padx=10)

        self.leer_siguiente = tk.Button(self, text="Leer siguiente símbolo",
                                             command=lambda: self.leer_siguente_simbolo())
        self.leer_siguiente.grid(column=0, row=6, pady=20, padx=10, sticky="e")

    # lectura del siguiente símbolo en la secuencia
    def leer_siguente_simbolo(self):
        simbolo_de_entrada = self.secuencia[self.posicion_secuencia]
        print(self.pila)
        transicion = self.automata_de_pila[self.pila[-1]][simbolo_de_entrada]
        avs = transicion[-1]
        if transicion == "R":
            self.rechace()
        elif transicion == "A":
            self.acepte()
        elif transicion[0] == "D":
            self.desapile()
        elif transicion[0] == "a":
            self.apile(transicion[2:-2])
        elif transicion[0] == "r":
            self.desapile()
            self.apile(transicion[2:-2])

        if avs == "a":
            self.avance()
        print(self.posicion_secuencia)
        if self.posicion_secuencia <= len(self.secuencia)-1:
            self.leer_secuencia.set("Próximo valor a leer: (" + self.secuencia[self.posicion_secuencia] + "), símbolo más alto en la pila: (" + self.pila[-1])
        else:
            self.leer_secuencia.set("Fin de secuancia, símbolo más alto en la pila: (" + self.pila[-1])

    def desapile(self):
        self.pila.pop()

    def apile(self, secuencia):
        secuencia = secuencia.split(",")
        for x in secuencia:
            self.pila.append(x)

    def avance(self):
        self.posicion_secuencia += 1

    def acepte(self):
        acepte = tk.Toplevel(app)
        self.l_error = tk.Label(acepte,
                                text="Acepta")
        self.l_error.grid(column=0, row=0, pady=10, padx=10, sticky="w")

    def rechace(self):
        rechazo_error = tk.Toplevel(app)
        self.l_error = tk.Label(rechazo_error,
                                text="Rechaza")
        self.l_error.grid(column=0, row=0, pady=10, padx=10, sticky="w")

    def error_transiciones(self):
        transiciones_error = tk.Toplevel(app)
        self.l_error = tk.Label(transiciones_error,
                                text="Hubo un error al ingresar la transición, por favor reintentar")
        self.l_error.grid(column=0, row=0, pady=10, padx=10, sticky="w")



if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(1080, 720)
    app = Application(root)
    app.pack(expand=True, fill='both')
    root.mainloop()
