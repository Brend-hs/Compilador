import tkinter as tk
from tkinter import filedialog
import subprocess

L=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
D=['0','1','2','3','4','5','6','7','8','9']
Es=[' ']
O=['+','-','*','/','=','(',')',',']


def cadena_sin_letras(cadena):
    return not any(caracter.isalpha() for caracter in cadena)

#--------------------Automata---------------------------
def q0(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        if(w[i] in Es):
            i=i+1
            tipo_token.append('e')
            cadena.append('e')
            q0(w,i,tipo_token)
        elif(w[i] in D):
            q1(w,i,tipo_token)
        elif(w[i]== 'i'):
            q7(w,i,tipo_token)
        elif(w[i]== 'p'):
            q8(w,i,tipo_token)
        elif(w[i] in L):
            q2(w,i,tipo_token)
        elif(w[i] in O):
            q5(w,i,tipo_token)
        elif(w[i] == '\n'):
            q6(w,i,tipo_token)
        elif(w[i] == '$'):
            q9(w,i,tipo_token)
        elif(w[i] == '"'):
            q10(w,i,tipo_token)
        else:
            i=i+1
            tipo_token.append('nv')
            cadena.append('nv')
            q0(w,i,tipo_token)
            
def q1(w,i,tipo_token):
    global cadena
    entero = ''
    if(i<len(w)):
        while(i<len(w) and w[i] in D):
            entero=entero+w[i]
            i=i+1
        tipo_token.append('#')
        cadena.append(entero)
        q0(w,i,tipo_token)
        
def q2(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        letra = ''
        letra=letra+w[i]
        i=i+1
        if(i<len(w) and w[i] in L):
            q3(letra, w, i,tipo_token)
        else:
            tipo_token.append('id')
            cadena.append(letra)
            q0(w,i,tipo_token)

def q3(letra, w, i, tipo_token):
    global cadena
    if(i<len(w)):
        letra=letra+w[i]
        i=i+1
        if(i<len(w) and w[i] in L):
            q4(letra, w, i, tipo_token)
        else:
            tipo_token.append('id')
            cadena.append(letra)
            q0(w,i,tipo_token)
        
def q4(letra, w, i,tipo_token):
    global cadena
    if(i<len(w)):
        while(i<len(w) and w[i] in L):
            letra=letra+w[i]
            i=i+1
        tipo_token.append('nv')
        cadena.append('nv')
        q0(w,i,tipo_token)

def q5(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        tipo_token.append(w[i])
        cadena.append(w[i])
        i=i+1
        q0(w,i,tipo_token)

def q6(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        tipo_token.append('sl')
        cadena.append('sl')
        i=i+1
        q0(w,i,tipo_token)

def q7(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        if(w[i+1] == 'n' and w[i+2]== 't'):
            tipo_token.append('int')
            cadena.append('int')
            i=i+3
            q0(w,i,tipo_token)
        elif(w[i+1] == 'm' and w[i+2]== 'p'):
            tipo_token.append('imp')
            cadena.append('imp')
            i=i+3
            q0(w,i,tipo_token)
        else:
            q2(w,i,tipo_token)

def q8(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        if(w[i+1] == 'o' and w[i+2]== 't'):
            tipo_token.append('pot')
            cadena.append('pot')
            i=i+3
            q0(w,i,tipo_token)
        else:
            q2(w,i,tipo_token)

def q9(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        tipo_token.append(w[i]) #$
        cadena.append(w[i])
        i=i+1
        q0(w,i,tipo_token)

def q10(w,i,tipo_token):
    global cadena
    if(i<len(w)):
        tipo_token.append('"')
        cadena.append('"')
        if(i<len(w) and w[i+1]!='$'):
            i=i+1
            q11(w,i,tipo_token)
        else:
            i=i+1
            q9(w,i,tipo_token)
            
def q11(w,i,tipo_token):
    global cadena
    letra = ''
    while(w[i]!='"' and i<len(w) and w[i]!='$'):
        letra=letra+w[i]
        i=i+1
    tipo_token.append('cadena')
    cadena.append(letra)
    if(w[i]=='"'):
        tipo_token.append('"')
        cadena.append('"')
        i=i+1
        q0(w,i,tipo_token)
    elif(w[i]=='$'):
        q9(w,i,tipo_token)

#-------------------Fin Automata-------------------------

#--------------------Lexico------------------------------
def lexico(tipo_token):
    global pos
    global token
    if(tipo_token[pos]=='+'):
        pos=pos+1
        token='+'
        return 1
    elif(tipo_token[pos]=='-'):
        pos=pos+1
        token='-'
        return 2
    elif(tipo_token[pos]=='*'):
        pos=pos+1
        token='*'
        return 3
    elif(tipo_token[pos]=='/'):
        pos=pos+1
        token='/'
        return 4
    elif(tipo_token[pos]=='#'): #numero
        pos=pos+1
        token='#'
        return 5
    elif(tipo_token[pos]=='id'): #id
        pos=pos+1
        token='id'
        return 6
    elif(tipo_token[pos]=='('):
        pos=pos+1
        token='('
        return 7
    elif(tipo_token[pos]==')'):
        pos=pos+1
        token=')'
        return 8
    elif(tipo_token[pos]=='int'):
        pos=pos+1
        token='int'
        return 9
    elif(tipo_token[pos]=='e'):
        pos=pos+1
        token='e'
        return 10
    elif(tipo_token[pos]=='sl'):
        pos=pos+1
        token='sl'
        return 11
    elif(tipo_token[pos]=='='):
        pos=pos+1
        token='='
        return 12
    elif(tipo_token[pos]=='imp'):
        pos=pos+1
        token='imp'
        return 13
    elif(tipo_token[pos]=='pot'):
        pos=pos+1
        token='pot'
        return 14
    elif(tipo_token[pos]=='"'):
        pos=pos+1
        token='"'
        return 15
    elif(tipo_token[pos]=='cadena'):
        pos=pos+1
        token='cadena'
        return 16
    elif(tipo_token[pos]==','):
        pos=pos+1
        token=','
        return 17
    else:
        token=' '
        return 0

#--------------------Fin Lexico---------------------------

#---------------------Sintactico--------------------------
def var(tipo_token):
    global pos
    global nombre
    global cadena
    global valor
    global linea
    auxpos=0
    pos_actual = pos
    if(lexico(tipo_token)==5): # #
        return 1
    pos=pos_actual
    if(lexico(tipo_token)==6): #id
        if(cadena[pos-1] not in nombre):
            msj='Error no declaraste la variable '+cadena[pos-1]+ ' que estas usando en la linea '+ str(linea)
            pilamsj.append(msj)
        elif(cadena[pos-1] in nombre):
            auxpos=nombre.index(cadena[pos-1])
            if(valor[auxpos]==''):
                msj='Error no inicializaste la variable '+cadena[pos-1]+ ' que estas usando en la linea '+str(linea)
                pilamsj.append(msj)
        return 1
    pos=pos_actual
    return 0

def arg(tipo_token):
    global pos
    global cadena
    global nombre
    global valor
    auxpos=0
    pos_actual = pos
    if(lexico(tipo_token)==15): #"
        if(lexico(tipo_token)==16): #cadena
            if(lexico(tipo_token)==15): #"
                return 1
    pos=pos_actual
    if(lexico(tipo_token)==5): # #
        return 1
    pos=pos_actual
    if(lexico(tipo_token)==6): #id
        if(cadena[pos-1] not in nombre):
            msj='Error no declaraste la variable '+cadena[pos-1]+ ' que estas usando en la linea '+  str(linea)
            pilamsj.append(msj)
        elif(cadena[pos-1] in nombre):
            auxpos=nombre.index(cadena[pos-1])
            if(valor[auxpos]==''):
                msj='Error no inicializaste la variable '+cadena[pos-1]+' que estas usando en la linea '+ str(linea)
                pilamsj.append(msj)
        return 1
    pos=pos_actual
    return 0

def iniciop(tipo_token):
    global pos
    if(tipo_token[pos]=='$'):
        return 1
    elif(inicio(tipo_token)==1):
        return 1
    return 1

def inicio(tipo_token):
    global pos
    global linea
    global cadena
    global nombre
    global valor
    global auxvalor
    global flag
    auxvalor = ''
    auxid=''
    auxpos=0
    flag=0
    pos_actual=pos
    if(lexico(tipo_token)==6): #id
        if(cadena[pos-1] not in nombre):
            msj='Error no declaraste la variable '+cadena[pos-1]+ ' que estas usando en la linea '+ str(linea)
            pilamsj.append(msj)
            auxid=cadena[pos-1]
        else:
            auxid=cadena[pos-1]
            auxpos=nombre.index(cadena[pos-1])
        if(lexico(tipo_token)==12): #=
            if(E(tipo_token)==1):
                if(auxid not in nombre):
                    auxvalor=''
                if(len(nombre)!=0 and auxid in nombre and flag==1): #Esta condicion la pusimos porque marcaba error cuando se intentaba guardar algo cuando no habias declarado nada
                    valor[auxpos]=auxvalor
                if(lexico(tipo_token)==11): #sl
                    linea=linea+1
                    if(iniciop(tipo_token)==1):
                        return 1
    pos=pos_actual
    if(lexico(tipo_token)==13): #imp
        if(lexico(tipo_token)==7): #(
            if(arg(tipo_token)==1):
                if(lexico(tipo_token)==8): #)
                    if(lexico(tipo_token)==11): #sl
                        linea=linea+1
                        if(iniciop(tipo_token)==1):
                            return 1
    pos=pos_actual
    if(lexico(tipo_token)==14): #pot
        if(lexico(tipo_token)==7): #(
            if(var(tipo_token)==1):
                if(lexico(tipo_token)==17): # ,
                    if(var(tipo_token)==1):
                        if(lexico(tipo_token)==8): #)
                            if(lexico(tipo_token)==11): #sl
                                linea=linea+1
                                if(iniciop(tipo_token)==1):
                                    return 1
    pos=pos_actual
    if(lexico(tipo_token)==11):#sl
        linea=linea+1
        if(iniciop(tipo_token)==1):
            return 1
    pos=pos_actual
    msj='Hay un error en la linea '+str(linea)
    pilamsj.append(msj)
    return 0

def F(tipo_token):
    global pos
    global cadena
    global nombre
    global valor
    global auxvalor
    global flag
    auxpos=0
    pos_actual = pos
    if(lexico(tipo_token)==7): #(
        auxvalor=auxvalor+cadena[pos-1]
        if(E(tipo_token)==1):
            if(lexico(tipo_token)==8): #)
                auxvalor=auxvalor+cadena[pos-1]
                return 1
    pos=pos_actual
    if(lexico(tipo_token)==5): #entero
        if(cadena_sin_letras(auxvalor)==True):
            auxvalor=auxvalor+cadena[pos-1]
            flag=1
        else:
            auxvalor=auxvalor+cadena[pos-1]
        return 1
    pos=pos_actual
    if(lexico(tipo_token)==6): #id
        if(cadena[pos-1] not in nombre):
            flag=0
            msj='Error no declaraste la variable '+cadena[pos-1]+ ' que estas usando en la linea '+ str(linea)
            pilamsj.append(msj)
            auxvalor=auxvalor+cadena[pos-1] 
        elif(cadena[pos-1] in nombre):
            flag=1
            auxpos=nombre.index(cadena[pos-1])
            if(valor[auxpos]==''):
                msj='Error no inicializaste la variable '+cadena[pos-1]+' que estas usando en la linea '+ str(linea)
                pilamsj.append(msj)
            else:
                auxvalor=auxvalor+cadena[pos-1] 
        return 1
    pos=pos_actual
    return 0

def Tp(tipo_token):
    global pos
    global auxvalor
    pos_actual=pos
    if(lexico(tipo_token)==4): #/
        auxvalor=auxvalor+cadena[pos-1]
        if(F(tipo_token)==1):
            if(Tp(tipo_token)==1):
                return 1
    pos=pos_actual
    if(lexico(tipo_token)==3): #*
        auxvalor=auxvalor+cadena[pos-1]
        if(F(tipo_token)==1):
            if(Tp(tipo_token)==1):
                return 1
    pos=pos_actual
    return 1

def T(tipo_token):
    global pos
    if(F(tipo_token)==1):
        if(Tp(tipo_token)==1):
            return 1
    return 0

def Ep(tipo_token):
    global pos
    global auxvalor
    pos_actual=pos
    if(lexico(tipo_token)==1): #+
        auxvalor=auxvalor+cadena[pos-1]
        if(T(tipo_token)==1):
            if(Ep(tipo_token)==1):
                return 1
    pos=pos_actual
    if(lexico(tipo_token)==2): #-
        auxvalor=auxvalor+cadena[pos-1]
        if(T(tipo_token)==1):
            if(Ep(tipo_token)==1):
                return 1
    pos=pos_actual
    return 1

def E(tipo_token):
    global pos
    if(T(tipo_token)==1):
        if(Ep(tipo_token)==1):
            return 1
    return 0

def inicializacion(tipo_token):
    global pos
    global linea
    global tablaSimb
    global valor
    global nombre
    global cadena
    auxpos=0
    pos_actual=pos
    if(lexico(tipo_token)==6): #id
        if(lexico(tipo_token)==12): #=
            if(lexico(tipo_token)==5): # #
                if(cadena[pos-3] not in nombre):
                    msj='Error no declaraste la variable ' +cadena[pos-3]+ ' que estas usando en la linea '+ str(linea)
                    pilamsj.append(msj)
                else:
                    auxpos=nombre.index(cadena[pos-3])
                    valor[auxpos]=cadena[pos-1]
                if(lexico(tipo_token)==11): #sl
                    linea=linea+1
                    if(inicializacion(tipo_token)==1):
                        return 1
    pos=pos_actual
    if(lexico(tipo_token)==11):#sl
        if(inicializacion(tipo_token)==1):
            linea=linea+1
            return 1
    pos=pos_actual
    return 1

def declaracion(tipo_token):
    global pos
    global linea
    global tablaSimb
    global tipo
    global nombre
    pos_actual=pos
    if(lexico(tipo_token)==9): #int
        if(lexico(tipo_token)==10): #e
            if(lexico(tipo_token)==6): # id  
                if(lexico(tipo_token)==11): #sl
                    if(cadena[pos-2] in nombre):
                        msj='Error ya has declarado la variable '+cadena[pos-2]
                        pilamsj.append(msj)
                    else:
                        tipo.append('int')
                        nombre.append(cadena[pos-2])
                    linea=linea+1
                    if(declaracion(tipo_token)==1):
                        return 1
    if(tipo_token[pos]=='int'):
        pos=pos-1
    else:
        pos=pos_actual
    if(lexico(tipo_token)==11):#sl
        msj='Hay un error en la linea '+str(linea)
        pilamsj.append(msj)
        if(declaracion(tipo_token)==1):
            linea=linea+1
            return 1
    pos=pos_actual
    return 1

def programa(tipo_token):
    global pos
    global pilamsj
    global tablaSimb
    global tipo
    global nombre
    global valor
    if(declaracion(tipo_token)==1):
        tablaSimb.append(tipo)
        tablaSimb.append(nombre)
        valor = [''] * len(tipo)
        if(inicializacion(tipo_token)==1):
            tablaSimb.append(valor)
            if(inicio(tipo_token)==1):
                return 1
    msj='Hay un error en la linea '+str(linea)
    pilamsj.append(msj)
    return 0
        

#-----------------Fin Sintactico--------------------------

#--------------------Interfaz----------------------------
def enviar_cadenas():
    global w
    global pilamsj
    w = entrada_texto.get("1.0", tk.END)
    todo()
    pilamsj = list(set(pilamsj))
    pilamsj.sort()
    mostrar_mensaje(pilamsj)

def cancelar():
    global w
    w = ""
    ventana.destroy()

def mostrar_mensaje(mensaje):
    mensaje_texto.config(state=tk.NORMAL)
    mensaje_texto.delete("1.0", tk.END)
    
    for m in mensaje:
        mensaje_texto.insert(tk.END, m + "\n")
    
    mensaje_texto.config(state=tk.DISABLED)

def update_line_numbers(event=None):
    # Obtener número de líneas en el editor
    lines = entrada_texto.get("1.0", "end-1c").split("\n")
    line_count = len(lines)
    
    # Actualizar el widget de números de línea
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete("1.0", tk.END)
    line_numbers.insert(tk.END, "\n".join(str(i) for i in range(1, line_count+1)))
    line_numbers.config(state=tk.DISABLED)

def on_scroll(*args):
    line_numbers.yview(*args)
    entrada_texto.yview(*args)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            entrada_texto.delete("1.0", tk.END)
            entrada_texto.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(entrada_texto.get("1.0", tk.END))

#-------------------Fin Interfaz------------------------

def todo():
    global w
    global i
    global tipo_token
    global token
    global pos
    global linea
    global pilamsj
    global tablaSimb
    global cadena
    global tipo
    global nombre
    global valor
    global auxvalor
    global flag
    tipo=[]
    nombre=[]
    valor=[]
    cadena=[]
    tablaSimb=[]
    w=w+'$'
    i=0
    tipo_token=[]
    token=[]
    pilamsj=[]
    q0(w,i,tipo_token)
    print(tipo_token)
    print(cadena)
    pos=0
    linea=1

    programa(tipo_token)
    while(pos<len(tipo_token)-1 and tipo_token[pos]!='$'):
        inicio(tipo_token)
        pos=pos+1

    print(tablaSimb)
    

if __name__== '__main__':
    ventana = tk.Tk()
    ventana.title("Proyecto Final")

    contenedor_principal = tk.Frame(ventana, bg="#E0D8DE")
    contenedor_principal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    panel1 = tk.Frame(contenedor_principal, bg="#E0D8DE")
    panel1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    panel2 = tk.Frame(contenedor_principal, bg="#E0D8DE")
    panel2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    etiqueta = tk.Label(panel1, text="Código Fuente", bg="#E0D8DE", font=("Arial",11))
    etiqueta.pack()

    etiqueta = tk.Label(panel2, text="Mensajes de error", bg="#E0D8DE", font=("Arial",11))
    etiqueta.pack()

    line_numbers = tk.Text(panel1, width=4, padx=5, pady=5, bg="#c9b7c7")
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)
    line_numbers.config(state=tk.DISABLED)

    scrollbar = tk.Scrollbar(panel1, bg="#E0D8DE")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    entrada_texto = tk.Text(panel1, height=47, width=65)
    entrada_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    entrada_texto.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=on_scroll)

    entrada_texto.bind("<Key>", update_line_numbers)
    entrada_texto.bind("<Button-1>", update_line_numbers)
    entrada_texto.bind("<MouseWheel>", update_line_numbers)

    update_line_numbers()

    boton_enviar = tk.Button(contenedor_principal, text="Compilar", command=enviar_cadenas, bg="#523961", fg="white", bd=2, relief=tk.RAISED, font=("Arial",12))
    boton_enviar.pack(side=tk.BOTTOM, pady=5)

    boton_cancelar = tk.Button(contenedor_principal, text="Cancelar", command=cancelar, bg="#c9b7c7", fg="black", bd=2, relief=tk.RAISED, font=("Arial",12))
    boton_cancelar.pack(side=tk.BOTTOM, pady=5)

    open_button = tk.Button(contenedor_principal, text="Abrir archivo", command=open_file, bg="#c9b7c7", fg="black", bd=2, relief=tk.RAISED, font=("Arial",12))
    open_button.pack(side=tk.BOTTOM, pady=5)

    save_button = tk.Button(contenedor_principal, text="Guardar archivo", command=save_file, bg="#c9b7c7", fg="black", bd=2, relief=tk.RAISED, font=("Arial",12))
    save_button.pack(side=tk.BOTTOM, pady=5)

    mensaje_texto = tk.Text(panel2, height=47, width=80)
    mensaje_texto.pack()
    mensaje_texto.config(state=tk.DISABLED)
    w = ""
    ventana.mainloop()
    print("Cadena ingresada por el usuario:")
    print(w)