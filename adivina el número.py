import random
import sys
from sqlitedict import SqliteDict

MIN = 0
MAX_SIMPLE = 100
MAX_INTERMEDIO = 1000
MAX_AVANZADO = 1000000
MAX_EXPERTO = 1000000000000

dificultad = {
    1:[MAX_SIMPLE, 10],
    2:[MAX_INTERMEDIO, 20],
    3:[MAX_AVANZADO, 35],
    4:[MAX_EXPERTO, 50],
}

def guardar_datos_sql():
 db = SqliteDict("records.sqlite")
 for key,value in records.items():
        db[int(key)] = value
 db.commit()       
 db.close()

def ordena_lista(lista):
    nueva_lista =  sorted(lista, key = lambda elemento:elemento[1], reverse = True)
    return nueva_lista

def elemento_en_dic(diccionario, elemento, punto):
      for numero in diccionario:
        if numero[0] == elemento:
          if numero[1] > punto:
            return True

def include_punto(diccionario, elemento, punto):
 if not elemento_en_dic(diccionario, elemento, punto):
    for numero in diccionario:
        if numero[0] == elemento:
            diccionario.remove(numero)
    diccionario.append((elemento, punto))

def si_o_no(pregunta):
  while True:
    ayuda = input(pregunta + " si/no\n")
    if ayuda == "si":
     return True
    elif ayuda == "no":
      return False
    else:
      print("responde con si o no")  

def menu():
    pregunta = si_o_no("¿Quieres jugar una partida?")
    if not pregunta:
        sys.exit()
    selección_dificultad = numentre("Selecciona una dificultad entre 1 y 4 ", 1,4, False)
    ayuda = si_o_no("¿Quieres ver el mínimo y máximo deducido?")
    return selección_dificultad, ayuda

def inputint(texto):
  while True:
    num = input(texto)
    try:
        num = int(num)
    except:
        print("no es un numero entero") 
    else:    
       return num
  

def numentre(texto, min, max, ayuda):
    if ayuda:
        texto += f"entre {min} y {max} \n"
    while True:
        num = inputint(texto)
        if num <= max and num >= min:
            return num
  

def gameloop(minimo, maximo, turnos, ayuda):
 numero = random.randint(minimo, maximo) 
 valmin = minimo
 valmax = maximo 
 ganar = False
 while turnos>0:
  num = numentre(f"adivina el número entero ", valmin, valmax, ayuda)#que no sea ni mayor ni menor al ()
  if num == numero:
      print("¡Has hacertado!")
      ganar = True
      break
  elif num > numero:
      print("un número más pequeño")
      valmax = num - 1
      turnos -= 1
  else:
      print("un número más grande")
      valmin = num + 1
      turnos -= 1
 return turnos,valmin, valmax, ganar  
         
records = {
    1:[],
    2:[],
    3:[],
    4:[]
}
db = SqliteDict("records.sqlite")
try:
 for key, item in db.items():
   records[key] = item
except:
    pass
db.close()

while True:     
        seleccion_dificultad, ayuda = menu()
        turnos, valmin, valmax, ganar = gameloop(MIN, dificultad[seleccion_dificultad][0], dificultad[seleccion_dificultad][1], ayuda)
        if ganar == True:
            print("Te han sobrado:", turnos, "turnos\n", f"Y entre los números {valmin} y {valmax}")
            nombre = input("Dame tu nombre para poder guaradar tu puntuación:\n")
            include_punto(records[seleccion_dificultad], nombre, turnos)
            records[seleccion_dificultad] = ordena_lista(records[seleccion_dificultad])
            guardar_datos_sql()
        else: 
             print("perdiste")
