import numpy as np
import random
import math

def main():
    establecerParametros()
    
    while True:
        print("Seleccione una opción:")
        print("1. Encriptar")
        print("2. Salir")

        opcion = input("Ingrese el número de la opción: ")

        if opcion == "1":
            encriptar()
            opcionesTodas()
        elif opcion == "2":
            print("Saliendo ... ¡Hasta luego! :p")
            break
        else:
            print("Opción no válida. Ingrese 1, 2 o 3.")
    
def opcionesTodas():
    while True:
        print("Seleccione una opción:")
        print("1. Encriptar")
        print("2. Desencriptar")
        print("3. Salir")

        opcion = input("Ingrese el número de la opción: ")

        if opcion == "1":
            encriptar()
        elif opcion == "2":
            desencriptar()
        elif opcion == "3":
            print("Saliendo ... ¡Hasta luego! :D")
            break
        else:
            print("Opción no válida. Ingrese 1, 2 o 3.")

#Ingresamos los parametros mod q, número de ecuaciones del sistema y la longitud de la clave secreta
def establecerParametros():
    global q 
    global necuaciones 
    global ClaveSecreta
    global A
    global B
    global aleatorio
    global nmuestra
    
    #Pedimos al usuario que ingrese los parámetros de seguridad
    q = int(input("Ingrese el valor de q (número primo grande): "))
    necuaciones = int(input("Ingrese el número de ecuaciones: "))
    longitudDeClave = int(input("Ingrese la longitud de la clave secreta: "))
    
    #Generamos la clave secreta de manera aleatoria
    ClaveSecreta = np.random.randint(0, q-1, size=(longitudDeClave, 1))
    print ("\nClave secreta: ", ClaveSecreta)
    
    #Generamos aleatoriamente la matriz pública de n ecuaciones
    A = np.random.randint(0, q, size=(necuaciones, longitudDeClave))
    B = (np.dot(A, ClaveSecreta))%q
    
    print("\nClave pública (A): ", A)
    
    
    
    
   
    

def encriptar():
    global u
    global v
    global necuaciones
    
    #Generamos el vector error aleatoriamente en cada encriptación en el rango [-4,4]
    E = np.random.randint(-4, 4, size=(necuaciones, 1))
    
    B_prima = (B + E)%q
    print("\nClave pública (B'): ", B_prima)
    mensaje = int(input("Ingrese el mensaje a encriptar (0 o 1): "))
    
    #Tomamos una muestra aleatoria diferente en cada encriptación
    #Vector aleatorio de 0 y 1
    aleatorio = np.random.randint(2, size=(1,necuaciones))
    
    #Número de ecuaciones de la muestra, lo usaremos en el desencriptado.
    nmuestra = np.count_nonzero(aleatorio == 1)
    
    print("El número de ecuaciones de la muestra es: ", nmuestra)
    
    #Escogemos una muestra aleatoria de las n ecuaciones y sumamos
    #Calculamos los valores u y v
    u = (np.dot(aleatorio, A))%q
    v = (np.dot(aleatorio, B_prima))%q
    v = (v + math.floor(q // 2) * mensaje)%q
    
    
    print("El mensaje encriptado es: ({}, {})".format(u, v))
    
def desencriptar():
    print("Ingrese el mensaje encriptado: ")
    
    u = np.array([int(x) for x in (input("Ingrese u (separado por comas y sin espacios): ")).split(',')])
    v = int(input("Ingrese v: "))
    
    #Pedimos el numero de ecuaciones de la muestra ya que varía para cada encriptación
    #Es necesario conocer nmuestra para calcular el intervalo en el que se encuentre Dec
    nmuestra =int (input("Ingrese el número de ecuaciones de la muestra: "))
    
    #Verificación de la clave secreta
    
    intento = 0

    while (intento < 3):
        s = np.array([int(x) for x in (input("Ingrese la clave secreta (separado por comas y sin espacios): ")).split(',')])

        if np.array_equal(s.reshape(-1, 1), ClaveSecreta):
            print("Desencriptando ...")
            break
        else:
            intento+= 1
            intentosrestantes = 3 - intento
            print(f"Clave incorrecta. Te quedan {intentosrestantes} intentos.")
    
    if (intento == 3):
        print("Has agotado todos los intentos")
        opcionesTodas();
    
    
    #Desencriptado. Calculamos Dec
    
    Dec = (v - np.dot(s,u))%q
    
    if (q/2 + nmuestra*-4 <= Dec <= q/2 + nmuestra*4) or (q/2 + nmuestra*-4 <= Dec - q <= q/2 + nmuestra*4):
	    print("El mensaje es 1")
    
    if (nmuestra*-4 <= Dec <= nmuestra*4) or (nmuestra*-4 <= Dec - q <= nmuestra*4):
	    print("El mensaje es 0")

    
main();
    