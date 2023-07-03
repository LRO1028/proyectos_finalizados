import tkinter as tk
import datetime
from playsound import playsound

class AppDespertador():

    def __init__(self, maestro):
        #cronometro
        self.h=0
        self.m=0
        self.s=0
        self.ms=0
        self.band=0

        self.master = maestro
        self.master.title("Despertador")
        self.master.config(bg="black")
        self.master.geometry("700x700")
        self.direccion_alarma = 'proyectos_prueba\\alarma.mp3'
        #Boton funcion cronometro
        self.boton=tk.Button(self.master, text = "Cronometro", command = self.cronometro,state=tk.NORMAL, font=("Times New Roman", 20), bg = "gray", fg = "black")
        self.boton.pack()

        #obtener el tiempo actual en segundos
        self.tiempo_actual_segundos = datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60 + datetime.datetime.now().second
        self.tiempo_restante = 0

        self.label = tk.Label(self.master, text="Crear una alarma: ", font=("Times New Roman", 28), bg="black", fg="white")
        self.label.pack(pady=20)

        #barra de texto para ingresar el nombre de la alarma
        self.label = tk.Label(self.master, text="Ingrese el nombre de la alarma", font=("Times New Roman", 16), bg="black", fg="white")
        self.label.pack(pady=20)
        self.nombre_ventana_nueva = tk.Entry(self.master, font=("Times New Roman", 16), width=20, background="gray", foreground="black", justify=tk.CENTER)
        self.nombre_ventana_nueva.pack(pady=10)

        #barra de texto para ingresar la hora de la alarma en formato HH:MM
        self.label3 = tk.Label(self.master, text="Ingrese la hora en formato HH:MM", font=("Times New Roman", 16), bg="black", fg="white")
        self.label3.pack(pady=20)
        self.time_entry = tk.Entry(self.master, font=("Arial", 24), width=10, background="gray", foreground="black", justify=tk.CENTER)
        self.time_entry.pack(pady=10)

        #boton de guardar
        self.log_button = tk.Button(self.master, text = "Guardar", command = self.guardar_tiempo,state=tk.NORMAL, font=("Times New Roman", 20), bg = "gray", fg = "black")
        self.log_button.pack(pady=20)

        #boton para resetear el temporizador al lado del boton de guardar
        self.resetear_button = tk.Button(self.master, text = "Resetear", command = self.reset, font=("Times New Roman", 20), bg = "gray", fg = "black")
        self.resetear_button.pack(pady=20)

    def guardar_tiempo(self):
        #obtener la hora ingresada por el usuario
        tiempo_ingresado = self.time_entry.get()
        tiempo_ingresado = tiempo_ingresado.split(":")
        try:
            tiempo_ingresado = sum([int(tiempo_ingresado[0]) * 3600, int(tiempo_ingresado[1]) * 60])
        except ValueError:
            self.label.configure(text="Ingrese un tiempo valido")
            self.time_entry.delete(0, tk.END)
            return
        
        #verificar si el tiempo ingresado es mayor al tiempo actual
        if tiempo_ingresado > self.tiempo_actual_segundos:
            #iniciar el temporizador
            self.tiempo_restante = tiempo_ingresado - self.tiempo_actual_segundos
            #crear una etiqueta para mostrar el tiempo restante
            self.etiqueta_debajo = tk.Label(self.master, text= f"Tiempo restante para la alarma:{self.tiempo_restante//3600}:{self.tiempo_restante%3600//60}")
            self.etiqueta_debajo.pack(pady=20)
            self.log_button.config(state=tk.DISABLED)
            self.descuento_hasta_hora_deseada(self.tiempo_restante)
        else:
            self.label3.configure(text="Ingrese un tiempo valido")
            self.time_entry.delete(0, tk.END)
            return #si el tiempo ingresado es menor al tiempo actual, salir de la funcion
    
    #funcion que resetea el temporizador
    def reset(self):
        #detener el temporizador
        self.master.after_cancel(self.tiempo_restante)
        self.tiempo_restante = 0
        #borrar la etiqueta
        self.etiqueta_debajo.destroy()
        #habilitar el boton de guardar
        self.log_button.config(state=tk.NORMAL)
        #borrar las barras de texto
        self.time_entry.delete(0, tk.END)
        self.nombre_ventana_nueva.delete(0, tk.END)
        self.label3.configure(text="Ingrese la hora en formato HH:MM")
    
    #funcion que descuenta el tiempo hasta la hora deseada
    def descuento_hasta_hora_deseada(self, tiempo):
        #si el tiempo restante es mayor a 0
        if tiempo > 0:
            #restar un segundo
            tiempo -= 1
            #actualizar la etiqueta
            tiempo_actualizar = "{:2d} horas, {:2d} minutos y {:2d} segundos".format(tiempo//3600, tiempo%3600//60, tiempo%60)
            self.etiqueta_debajo.configure(text="Tiempo restante para la alarma:"+ tiempo_actualizar, font=("Times New Roman", 16), bg="black", fg="white")
            #esperar un segundo
            self.tiempo_restante = self.master.after(1000, lambda: self.descuento_hasta_hora_deseada(tiempo))
        else:
            #llamar a la funcion de alarma
            self.alarma(self.nombre_ventana_nueva.get())
    
    #Funcion que cuando llegue el descuento a 0 cree otra ventana con la alarma y un boton para detenerla
    def alarma(self,nombre_alarma):
        #crear una nueva ventana
        self.ventana_alarma = tk.Toplevel(self.master)
        self.ventana_alarma.config(bg="black")
        self.ventana_alarma.title("Alarma")
        #crear una etiqueta con el nombre de la alarma
        self.etiqueta_alarma = tk.Label(self.ventana_alarma, text=nombre_alarma, font=("Times New Roman", 28), bg="black", fg="white")
        self.etiqueta_alarma.pack(pady=20)
        #crear un boton para detener la alarma
        self.boton_detener = tk.Button(self.ventana_alarma, text="Detener", command=self.stop_alarm, font=("Times New Roman", 20), bg = "red", fg = "white")
        self.boton_detener.pack(pady=20)
        #crea un boton para aplazar la alarma
        self.boton_aplazar=tk.Button(self.ventana_alarma, text="Aplazar", command=self.aplazar_alarma,font=("Times New Roman", 20), bg="blue", fg="white")
        self.boton_aplazar.pack(pady=20)
        #sonar la alarma
        self.ventana_alarma.after(100, self.reproducir_musica, self.direccion_alarma)
        #destruir la ventana secundaria despues de 15 segundos
        self.ventana_alarma.after(15000, self.ventana_alarma.destroy)


    #funcion que detiene la alarma
    def stop_alarm(self):
        #detener la alarma
        self.ventana_alarma.destroy()
        #resetear el temporizador
        self.reset()
    
    def aplazo_10seg(self):
        # obtener la hora ingresada por el usuario
        tiempo_ingresado=self.tiempo_actual_segundos+10

        # verificar si el tiempo ingresado es mayor al tiempo actual
        if tiempo_ingresado > self.tiempo_actual_segundos:
            # iniciar el temporizador
            self.tiempo_restante = tiempo_ingresado - self.tiempo_actual_segundos
            # crear una etiqueta para mostrar el tiempo restante
            self.etiqueta_debajo.config(text=f"Tiempo restante para la alarma:{self.tiempo_restante // 3600}:{self.tiempo_restante % 3600 // 60}")
            self.etiqueta_debajo.pack(pady=20)
            self.log_button.config(state=tk.DISABLED)
            self.descuento_hasta_hora_deseada(self.tiempo_restante)
        else:
            self.label3.configure(text="Ingrese un tiempo valido")
            self.time_entry.delete(0, tk.END)
            return  # si el tiempo ingresado es menor al tiempo actual, salir de la funcion

    def aplazar_alarma(self):
        # Aplazar la alarma
        self.ventana_alarma.destroy()
        self.aplazo_10seg()

    #funcion para reproducir sonido.  
    def reproducir_musica(self, ruta):    
        playsound(ruta)
    
    #Inicio de metodos para el cronometro
    def detener_c(self):
       self.ventana_cronometro.after_cancel(self.t)
       self.etiq.configure(bg="black",fg="white")

    def salir_c(self):
       self.h=0
       self.m=0
       self.s=0
       self.ms=0   
       self.ventana_cronometro.destroy()

    def iniciar_c(self):
       self.pausar.config(state=tk.NORMAL)
       self.reiniciar.config(state=tk.NORMAL)
       self.ms=self.ms+1
       if self.ms==999:
            self.ms=0
            self.s+=1
            if self.s==59:
                 self.s=0
                 self.m+=1
       self.etiq.configure(text=f"{self.h}:{self.m}:{self.s}:{self.ms}",font=("Times New Roman", 70),bg="black",fg="yellow")
       self.t=self.ventana_cronometro.after(1,self.iniciar_c)

    def reiniciar_c(self):
       self.ventana_cronometro.after_cancel(self.t)
       self.h=0
       self.m=0
       self.s=0
       self.ms=0
       self.etiq.configure(text=f"{self.h}:{self.m}:{self.s}:{self.ms}",font=("Times New Roman", 70),bg="black",fg="red")      

    def cronometro(self):
       #ventana
       self.ventana_cronometro = tk.Toplevel(self.master)
       self.ventana_cronometro.config(bg="black")
       self.ventana_cronometro.title("Cronometro")
       self.ventana_cronometro.geometry("600x200")
       self.ventana_cronometro.resizable(width=False,height=False)
       #botones y etiquetas
       self.iniciar=tk.Button(self.ventana_cronometro,text="Iniciar",command=self.iniciar_c,bg="yellow",font=("Times New Roman", 35))
       self.pausar=tk.Button(self.ventana_cronometro,text="Pausar",command=self.detener_c,state="disabled",bg="white",fg="black")
       self.salir=tk.Button(self.ventana_cronometro,text="Salir",command=self.salir_c)
       self.reiniciar=tk.Button(self.ventana_cronometro,text="Reiniciar",command=self.reiniciar_c,state="disabled")
       self.salir.pack()
       self.iniciar.pack()
       self.pausar.pack()
       self.reiniciar.pack()
       self.reiniciar.place(x=380,y=170)
       self.iniciar.place(x=10,y=10,width=180,height=180)
       self.pausar.place(x=325,y=170)
       self.salir.place(x=450,y=170)
       #mensaje
       self.etiq=tk.Label(self.ventana_cronometro,text=f"{self.h}:{self.m}:{self.s}:{self.ms}",font=("Times New Roman", 70),bg="black",fg="white")
       self.etiq.pack()
       self.etiq.place(x=200,y=40)

if __name__ == "__main__":
    # Crear la ventana principal de la aplicación
    root = tk.Tk()
    # Crear una instancia de la aplicación de temporizador
    timer_app = AppDespertador(root)
    # Iniciar el bucle principal de la interfaz de usuario
    root.mainloop()