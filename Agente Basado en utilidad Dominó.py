from random import shuffle
import random
from itertools import combinations_with_replacement, chain
from collections import Counter
def seleccionar_ficha_utilidad(fichas_computadora, serpiente, ubicacion):
    puntuaciones = []  # Lista para almacenar las puntuaciones de cada ficha disponible

    # Calcular la puntuación de cada ficha disponible
    for i, ficha in enumerate(fichas_computadora):
        ficha = fichas_computadora[i]
        
        if ubicacion == "derecha":
            extremo = serpiente[-1][-1]  # Extremo derecho de la serpiente
            if extremo in ficha or extremo == ficha[::-1]:
                puntuaciones.append(ficha[0] + ficha[1])  # Sumar los valores de la ficha
            else:
                puntuaciones.append(0)  # Ficha no válida
        elif ubicacion == "izquierda":
            extremo = serpiente[0][0]  # Extremo izquierdo de la serpiente
            if extremo in ficha or extremo == ficha[::-1]:
                puntuaciones.append(ficha[0] + ficha[1])  # Sumar los valores de la ficha
            else:
                puntuaciones.append(0)  # Ficha no válida
        else:
            puntuaciones.append(0)  # Ubicación inválida

    # Obtener el índice de la ficha con la puntuación más alta
    if len(puntuaciones) > 0:
        indice_max_puntuacion = puntuaciones.index(max(puntuaciones))
        return indice_max_puntuacion
    else:
        return None


# Define la función de turno
def turno(func_input, func_pieces, placement):
    # Detener si no hay fichas
    if int(func_input) == 0 and len(fichas_stock) == 0:
        return None
    # Darle una ficha al jugador o a la computadora
    elif int(func_input) == 0 and len(fichas_stock) > 0:
        func_pieces.append(fichas_stock[-1])
        fichas_stock.remove(fichas_stock[-1])
        return None 
    # Colocar la ficha en el lado derecho de la serpiente
    if int(func_input) > 0:
        ficha_a_extremo = func_pieces[int(func_input) - 1]
        if placement == "derecha":
            if  serpiente[-1][-1] == ficha_a_extremo[1] :#[1,5][3,5] --> serpiente[[0][0][-1][-1]] ficha[0,1]
                ficha_a_extremo.reverse()
                serpiente.append(ficha_a_extremo)#Insertar al lado derecho
                
            elif serpiente[-1][-1] == ficha_a_extremo[0] :#[1,5][5,3] --> serpiente[[0][0][-1][-1]] ficha[0,1] 
                serpiente.append(ficha_a_extremo)#Insertar al lado derecho
        func_pieces.remove(func_pieces[int(func_input) - 1])
        
    else:
        ficha_a_extremo = func_pieces[-int(func_input) - 1]
        if placement == "izquierda":
            if ficha_a_extremo[1] == serpiente[0][0]: #[2,5][5,2] --> ficha[0,1] serpiente[[0][0][-1][-1]]
               serpiente.insert(0, ficha_a_extremo)#Insertar al lado izquierdo de serpiente
            elif ficha_a_extremo[0] == serpiente[0][0]: #[6,2][6,2] --> ficha[0,1] serpiente[[0][0][-1][-1]]
                ficha_a_extremo.reverse() #Invertir la ficha del jugador para que coincida con la puesta en el tablero
                
                serpiente.insert(0,ficha_a_extremo)#Insertar al lado izquierdo
        func_pieces.remove(func_pieces[-int(func_input) - 1])
       
# Comprobar si esta serpiente es ganadora
def serpiente_ganadora(func_serpiente):
    if func_serpiente[0][0] == func_serpiente[-1][-1] and sum(x.count(func_serpiente[0][0]) for x in func_serpiente) == 8:
        return True

# Definir la lista de fichas
fichas_domino = list(combinations_with_replacement(range(0, 7), 2))
# Convertir la lista de tuplas a lista de listas
fichas_domino = [list(x) for x in fichas_domino]
# Barajar las fichas
shuffle(fichas_domino)
# Definir el coeficiente igual a la mitad del número de fichas
coeficiente = len(fichas_domino) // 2
# Obtener la primera mitad de las fichas
fichas_stock = fichas_domino[:coeficiente]
# Obtener las fichas de la computadora y del jugador
fichas_computadora = fichas_domino[coeficiente:int(coeficiente * 1.5)]
fichas_jugador = fichas_domino[int(coeficiente * 1.5):]
# Encontrar la serpiente
serpiente = [max([[x, y] for x, y in fichas_computadora + fichas_jugador if x == y])]
# Quitar la serpiente de las fichas de la computadora o del jugador
if serpiente[0] in fichas_computadora:
    fichas_computadora.remove(serpiente[0])
else:
    fichas_jugador.remove(serpiente[0])

# Definir quién juega primero
num_turno = 0 if len(fichas_jugador) > len(fichas_computadora) else 1

# Comenzar el juego
while True:
    # Mostrar el stock, las fichas del jugador y de la computadora
    print("\033[32m=\033[0m"*70)

    print('Cantidad en stock:', len(fichas_stock))
    print('Fichas de la computadora:', len(fichas_computadora), '\n')
    print(*serpiente, '\n', sep='') if len(serpiente) <= 6 else print(*serpiente[:3], '...', *serpiente[-3:], '\n', sep='')
    print("Tus fichas:")
    for num, ficha in enumerate(fichas_jugador):
        print(f"{num + 1}: {ficha}")

    # Condición para la victoria del jugador
    if len(fichas_jugador) == 0 or (serpiente_ganadora(serpiente) and num_turno == 0):
        print("\nEstado: El juego ha terminado. ¡Ganaste!")
        break
    # Condición para la victoria de la computadora
    if len(fichas_computadora) == 0 or (serpiente_ganadora(serpiente) and num_turno == 1):
        print("\nEstado: El juego ha terminado. ¡Ganó la computadora!")
        break
    # Definir los extremos de la serpiente
    keys_conexion = [serpiente[0][0], serpiente[-1][-1]]
    # Condición para el empate
    if len(fichas_stock) == 0 and not any(item in keys_conexion for item in list(chain(*(fichas_jugador + fichas_computadora)))):
        # Calcular puntos totales de cada jugador
        puntos_jugador = sum(sum(ficha) for ficha in fichas_jugador)
        puntos_computadora = sum(sum(ficha) for ficha in fichas_computadora)

        if puntos_jugador < puntos_computadora:
            print("\nEstado: ¡El jugador ha ganado la partida! (Menos puntos)")
        elif puntos_jugador > puntos_computadora:
            print("\nEstado: ¡La computadora ha ganado la partida! (Menos puntos)")
        else:
            print("\nEstado: El juego ha terminado. ¡Es un empate!")
        break


    # Turno del jugador
    if num_turno % 2 == 0:
        # Contar el número de turno
        num_turno += 1
        # Mostrar mensaje
        print("\033[91mEstado: Es tu turno. Ingresa tu comando.  \033[0m")
        # Obtener la entrada del jugador
        entrada_usuario = input()
        # Comprobar si el jugador quiere pasar el turno
        if entrada_usuario.strip().lower() == "pass":
            continue
        # Comprobar si el jugador quiere robar una ficha
        if entrada_usuario.strip().lower() == "robar":
            # Verificar si hay fichas disponibles en el stock
            if len(fichas_stock) > 0:
                # Robar una ficha del stock
                fichas_jugador.append(fichas_stock[-1])
                fichas_stock.pop(-1)
                # Continuar con el turno
                continue
            else:
                print("\033[91m No hay fichas disponibles para robar. Ingresa tu comando nuevamente.\033[0m")
                num_turno -= 1
                continue
        # Comprobar si la entrada del jugador es válida
        # Si la cadena restante después de eliminar el signo negativo es un número entero 
        # Y  corresponde a los índices válidos para acceder a las fichas del jugador.
        if entrada_usuario.lstrip("-").isdigit() and int(entrada_usuario) in range(-len(fichas_jugador)-1, len(fichas_jugador) + 1):
            # Darle una ficha al jugador
            if int(entrada_usuario) == 0 :
                    turno(entrada_usuario, fichas_jugador,"derecha")
                    continue
               
            
            # Definir la ficha actual
            #fichas_jugador empiezan en el indice 0, las entrada_usuario inician en 1
            #entradas_usuario (ya sea positivo o negativo)-1, para encontrar la ficha correspondiente en fichas_jugador 
            ficha_actual = fichas_jugador[int(entrada_usuario) - 1] if int(entrada_usuario) > 0 else fichas_jugador[-int(entrada_usuario) - 1]
            # Comprobar si la ficha es válida
            if keys_conexion[-1] in ficha_actual and int(entrada_usuario) > 0:#keys_conexion[-1]) representa el extremo derecho de la serpiente.
                    turno(entrada_usuario, fichas_jugador, "derecha")
            elif keys_conexion[0] in ficha_actual and int(entrada_usuario) < 0:#keys_conexion[0]) representa el extremo izquierdo de la serpiente.
                    turno(entrada_usuario, fichas_jugador, "izquierda")
            else:
                print("Movimiento ilegal. Por favor, inténtalo de nuevo.")
                num_turno -= 1
                continue
        else:
            print("\033[91mEntrada inválida. Por favor, inténtalo de nuevo.\033[0m")
            num_turno -= 1
            continue
    # Turno de la computadora
    else:
        # Contar el número de turno
        num_turno += 1
        # Mostrar mensaje
        print("\033[35m\nEstado: La computadora está a punto de jugar. Presiona Enter para continuar...\033[0m")
        # Esperar la entrada del jugador
        input()
        # Comprobar si la computadora tiene fichas válidas para colocar
        fichas_validas= []
        puntuar = []
        for i, ficha in enumerate(fichas_computadora):
            if keys_conexion[-1] in ficha :#Hay fichas validas a la derecha
                fichas_validas.append(fichas_computadora[i]) 
            elif keys_conexion[0] in ficha:#Hay fichas validas a la izquierda
                fichas_validas.append(fichas_computadora[i]) 
                
        if len(fichas_validas) > 0 :# Hay fichas validas a la derecha o a la izquierda 
            # Seleccionar la mejor ficha utilizando la función de utilidad
            indice_mejor_ficha = seleccionar_ficha_utilidad(fichas_computadora, serpiente, "derecha")
            fichaD = fichas_computadora[indice_mejor_ficha]#La mejor ficha para colocar a la derecha 
            indexD=  indice_mejor_ficha
            puntuar.append(fichaD[0] + fichaD[1]) #Se adiciona a la lista puntuar 
       
                
            indice_mejor_ficha = seleccionar_ficha_utilidad(fichas_computadora, serpiente, "izquierda")
            fichaI = fichas_computadora[indice_mejor_ficha]#La mejor ficha para colocar a la izquierda 
            indexI=  indice_mejor_ficha 
            puntuar.append(fichaI[0] + fichaI[1]) #Se adiciona a la lista puntuar
        
            ficha_index = puntuar.index(max(puntuar))#De la lista puntuar se extrae la ficha con mayor puntuación 
            
            if  ficha_index == 0: #Ficha valida para Derecha
                ficha_index = indexD
            elif ficha_index == 1: #Ficha valida para izq
                 ficha_index = indexI
                
            # Comprobar si la ficha se coloca a la derecha o izquierda de la serpiente
            if keys_conexion[0] in fichas_computadora[ficha_index]:
                ubicacion = "izquierda"
                turno(str((ficha_index + 1) * -1), fichas_computadora, ubicacion)#Si es a la izq se coloca el indice en negativo
                print("\033[35mLa computadora ha colocado una ficha\033[0m")
            elif keys_conexion[-1] in fichas_computadora[ficha_index]:
                ubicacion = "derecha"
                turno(str(ficha_index + 1), fichas_computadora, ubicacion)
                print("\033[35mLa computadora ha colocado una ficha\033[0m")
                
           
            
        else:
            # La computadora no tiene fichas válidas para colocar, robar una ficha si es posible
            if len(fichas_stock) > 0:
                fichas_computadora.append(fichas_stock[-1])
                fichas_stock.pop(-1)
                print("\033[35mLa computadora ha robado una ficha.\033[0m")
            else:
                print("\033[35mLa computadora no tiene fichas válidas ni puede robar. Pasa el turno.\033[0m")
                turno("0", fichas_computadora, "")#derecha
                

# Fin del juego
print("Gracias por jugar. ¡Hasta la próxima!")