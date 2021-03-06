import tkinter
from functools import partial
from tkinter import *
from tkinter import font, Tk, messagebox
import matplotlib as plt
from matplotlib import *
from utils import *
plt.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Interpolacion import *



master: Tk = Tk()
master.title("FINTER")
master.geometry('680x485')
master.resizable(0, 0)
metodo = Interpolacion(Lagrange())

puntos = []
x0 = StringVar()
y0 = StringVar()
k0 = StringVar()

fuente = font.Font(weight='bold')
tkinter.Label(master, text="X", font=fuente).place(x=240, y=0)
labelFunction = tkinter.Label(master, text="", font=fuente)
labelFunction.place(x=300, y=160)
tkinter.Label(master, text="F(X)", font=fuente).place(x=360, y=0)
textX1 = tkinter.Entry(master, textvariable=x0)
textY1 = tkinter.Entry(master, textvariable=y0)
textX1.place(x=190, y=30)
textY1.place(x=320, y=30)


def formalizarlabellistasting(label, lista):
    return label + "  " + "  ".join(map(str, lista))


def crearlistai():
    global puntos
    i = 0;
    listai = []
    while i <= len(puntos) - 1:
        listai.append(i)
        i += 1
    return listai


Etiquetai = tkinter.Label(master, text=formalizarlabellistasting("i", crearlistai()), font=fuente)
Etiquetai.place(x=10, y=80)

EtiquetaX = tkinter.Label(master, text=formalizarlabellistasting("X", map(lambda p: p.x, puntos)), font=fuente)
EtiquetaX.place(x=10, y=100)
EtiquetaY = tkinter.Label(master, text=formalizarlabellistasting("F(x)", map(lambda p: p.y, puntos)), font=fuente)
EtiquetaY.place(x=10, y=120)


def actualizarCheckLagra():
    global checkNewGreg
    global checkRegresivo
    global checkProgresivo
    global checkLagrange
    global metodo
    checkLagrange.select()
    checkProgresivo.deselect()
    checkRegresivo.deselect()
    checkProgresivo['state'] = DISABLED
    checkRegresivo['state'] = DISABLED
    checkNewGreg.deselect()
    metodo = Interpolacion(Lagrange())


def actualizarCheckNewGreg():
    global checkLagrange
    global checkRegresivo
    global checkProgresivo
    global checkNewGreg
    global metodo
    checkNewGreg.select()
    checkProgresivo.select()
    checkProgresivo['state'] = NORMAL
    checkRegresivo['state'] = NORMAL
    checkLagrange.deselect()
    checkRegresivo.deselect()
    metodo = Interpolacion(NewtonGregoryProgre())


def actualizarCheckProgre():
    global checkRegresivo
    global checkProgresivo
    global metodo
    checkProgresivo.select()
    checkRegresivo.deselect()
    metodo = Interpolacion(NewtonGregoryProgre())


def actualizarCheckRegre():
    global checkRegresivo
    global checkProgresivo
    global metodo
    checkProgresivo.deselect()
    checkRegresivo.select()
    metodo = Interpolacion(NewtonGregoryRegre())


progresivo = IntVar()
regresivo = IntVar()
lagrange = IntVar()
NewtonGreg = IntVar()

checkLagrange = tkinter.Checkbutton(master, text="Interpolación polinómica de Lagrange", variable=lagrange,
                                    state=DISABLED, command=actualizarCheckLagra)
checkLagrange.place(x=10, y=160)

checkNewGreg = tkinter.Checkbutton(master, text="Interpolación polinómica Newton-Gregory", variable=NewtonGreg,
                                   state=DISABLED, command=actualizarCheckNewGreg)
checkNewGreg.place(x=10, y=180)
checkProgresivo = tkinter.Checkbutton(master, text="Progresivo", variable=progresivo,
                                      state=DISABLED, command=actualizarCheckProgre)
checkProgresivo.place(x=30, y=200)
checkRegresivo = tkinter.Checkbutton(master, text="Regresivo", variable=regresivo,
                                     state=DISABLED, command=actualizarCheckRegre)
checkRegresivo.place(x=30, y=220)

def alterarPunto(punto, lista):
    if any(list(filter(lambda puntolista:puntolista.x == punto.x,lista))):
        lista.remove(list(filter(lambda puntolista:puntolista.x == punto.x,lista))[0])
    lista.append(punto)
    return lista

def agregarrpuntos():
    global puntos
    if x0.get().lstrip('-+').isdigit() & y0.get().lstrip('-+').isdigit():
        punto = Punto(int(x0.get()), int(y0.get()))
        puntos= alterarPunto(punto,puntos)
        actualizarlista()
        calcular()
    else:
        messagebox.showinfo("Warning", "Punto debe estar compuesto de numeros")


def deletearpuntos():
    global puntos
    if x0.get().lstrip('-+').isdigit() & y0.get().lstrip('-+').isdigit():
        punto = Punto(int(x0.get()), int(y0.get()))
        if punto in puntos:
            puntos.remove(punto)
            actualizarlista()
        else:
            messagebox.showinfo("Warning", "El punto no se encuentra en la lista")
    else:
        messagebox.showinfo("Warning", "Punto debe estar compuesto de numeros")


def actualizarlista():
    global puntos
    puntos = utils.ordernarpuntos(puntos)
    solopuntosx = map(lambda p: p.x, puntos)
    textX1.delete(0, END)
    textY1.delete(0, END)
    actualizarlabelpuntos()
    if len(puntos) >= 2:
        activarCheckBox()


def activarCheckBox():
    global checkNewGreg
    global checkLagrange
    checkNewGreg['state'] = "normal"
    checkLagrange['state'] = "normal"
    actualizarCheckLagra()


def actualizarlabelpuntos():
    global Etiquetai
    global EtiquetaY
    global EtiquetaX
    Etiquetai.config(text=formalizarlabellistasting("i       ", crearlistai()))
    EtiquetaX.config(text=formalizarlabellistasting("X     ", map(lambda p: p.x, puntos)))
    EtiquetaY.config(text=formalizarlabellistasting("F(X)", map(lambda p: p.y, puntos)))


def verificarequidistancia(listapuntos):
    if len(set(utils.diferenciaDeValoresLista(utils.puntosx(listapuntos)))) == 1:
        return "Los puntos son equidistantes"
    else:
        return "Los puntos no equidistan"


def graficarPolinomio(funcion, puntosx, puntosy):
    global labelFunction
    rango = range(puntosx[0], puntosx[-1] * 5)
    f = Figure(figsize=(4, 4), dpi=100)
    x = rango
    y = utils.pasarFuncionAPuntos(str(funcion), rango)
    a = f.add_subplot(111)
    a.plot(x, y, 'r-', label="P(x)=" + str(funcion))
    a.plot(puntosx, puntosy, 'k.', label="Puntos")
    a.legend()
    a.grid(linestyle='-', linewidth=1)
    canvas = FigureCanvasTkAgg(f, master)
    canvas.draw()
    canvas.get_tk_widget().place(x=10, y=30)
    canvas._tkcanvas.place(x=290, y=105)
    messagebox.showinfo("Polinomio encontrado", "F(x) = " + str(funcion))


def activarBotones():
    global botonPoliK
    global botonHistorial
    botonPoliK['state'] = NORMAL
    botonHistorial['state'] = NORMAL


def calcular():
    if puntos:
        metodo.strategy.historia = []
        metodo.calcularpolinomio(puntos)
        graficarPolinomio(metodo.polinomio, utils.puntosx(puntos), utils.puntosy(puntos))
        metodo.strategy.historia.append(verificarequidistancia(puntos))
        metodo.strategy.historia.append("Grado:" + utils.calcularGradoPolinomio(str(metodo.polinomio)))
        activarBotones()
    else:
        messagebox.showinfo("Warning",
                            "La lista de puntos esta vacia, complete los campos y haga click en 'Agregar/Alterar Punto'")


def quit():
    global master
    master.destroy()


def pasar():
    pass


def insertarLista(listbox, listaLxODiferencias):
    for lxOd in listaLxODiferencias[0]:
        listbox.insert(END, lxOd)
    listbox.insert(END, "Polinomio final = " + listaLxODiferencias[1])
    listbox.insert(END, "Polinomio simplificado = " + str(listaLxODiferencias[2]))
    listbox.insert(END, listaLxODiferencias[3])
    listbox.insert(END, listaLxODiferencias[4])


def pantallaHistorial():
    win = Toplevel(master)
    win.title("Pasos")
    win.geometry('640x480')
    # img = ImageTk.PhotoImage(file=".img\\"+metodo.strategy.definicionPhoto())
    # panel = Label(win, image=img)
    # panel.image=img
    # panel.image = "C:/Users/Ivan/PycharmProjects/TPMATESUPERIOR_2C_2019/megamanX.jpg"
    # panel.pack(side=TOP, expand = "yes")
    scrollbar = Scrollbar(win)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbarX = Scrollbar(win)
    scrollbarX.pack(side=BOTTOM, fill=X)
    listbox = Listbox(win, yscrollcommand=scrollbar.set,xscrollcommand=scrollbarX.set)
    insertarLista(listbox, metodo.strategy.historia)
    listbox.pack(fill=BOTH, expand=1)
    scrollbar.config(command=listbox.yview)
    scrollbarX.config(command=listbox.xview,orient=HORIZONTAL)
    # win.protocol("WM_DELETE_WINDOW", pasar)


def pantallaValorK():
    global botonPoliK
    global k0
    global master
    win = Toplevel(master)
    win.title("Valor K")
    win.geometry('320x240')
    textK = tkinter.Entry(win, textvariable=k0)
    textK.place(x=100, y=60)
    botonPoliK['state'] = DISABLED
    botonVolver = tkinter.Button(win, text="Volver", command=partial(quitK, win))
    botonVolver.place(x=105, y=80)
    botonCalcularK = tkinter.Button(win, text="Calcular", command=calcularK)
    botonCalcularK.place(x=165, y=80)
    #   Etiquetak = tkinter.Label(win, text="P(k) =", font=fuente)
    #  Etiquetak.place(x=0, y=180)
    win.protocol("WM_DELETE_WINDOW", pasar)


def quitK(win):
    global botonPoliK
    win.destroy()
    botonPoliK['state'] = NORMAL


def calcularK():
    global metodo
    global k0
    if k0.get().lstrip('-+').isdigit():
        fk = str(metodo.polinomio).replace('x', str(k0.get()))
        messagebox.showinfo("Information", "P(" + str(k0.get()) + ") = " + str(utils.simplificarFuncion(fk)))
    else:
        messagebox.showinfo("Warning", "Valor mal ingresado, porfavor ingrese un numero")


Figure
tkinter.Button(master, text="Agregar/Alterar Punto", command=agregarrpuntos).place(x=186, y=50)
tkinter.Button(master, text="Eliminar Punto", command=deletearpuntos).place(x=340, y=50)
botonHistorial = tkinter.Button(master, text="Mostrar pasos de cálculo", command=pantallaHistorial, width=35,
                                state=DISABLED)
botonHistorial.place(x=15, y=300)
botonPoliK = tkinter.Button(master, text="Especializar el polinomio en un valor K", command=pantallaValorK, width=35,
                            state=DISABLED)
botonPoliK.place(x=15, y=340)
tkinter.Button(master, text="Finalizar", command=quit, width=35).place(x=15, y=380)
botonCalcular = tkinter.Button(master, text="Calcular Polinomio", command=calcular, width=35)
botonCalcular.place(x=15, y=260)
master.mainloop()
