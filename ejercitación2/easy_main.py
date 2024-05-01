import pandas as pd
from easy_funciones import easy_session, scraping_easy
import random
import time
from datetime import date

######## Definición de parámetros a utlizar
max_paginas = 5

secciones = [
    "pinturas/de-interior",
    #"iluminacion-y-deco/iluminacion",
    #"automotor/neumaticos-y-accesorios/neumaticos",
    #"muebles-de-interior/comedor"
    ]
    
codigo_partido_dict = {'Morón' : '1708',
                       'San Martín' : '1650' }
                  
CANTIDAD_INTENTOS = 2 
###############
 
# Configuración del sistema de registro

start_time = time.time()

# Definir fecha actual
fecha_actual = date.today().strftime('%d-%m-%Y')

#Nombre de cadena
CADENA = 'Easy'

#Nombre del archivo
excel_filename = f"{CADENA}_scrap_por_partido_{fecha_actual}.xlsx"
excel_sheet_name = f"{CADENA}"

# Se inicializa variable para el contador de iteraciones
iteracion = 0
# Se inicializa diccionario con todas los partidos de interés
partidos_a_iterar = codigo_partido_dict
# Se inicializa diccionario para guardar el df de cada iteración
dict_iteraciones = {}
df_iteracion = pd.DataFrame()

# Df con la suma de precios por partido
df_super_total = []

# Iteramos partido a partido mientras haya partidos no iterados
# (Son todas en la iteración 0 o las que dieron error en las diferentes iteraciones)
while len(partidos_a_iterar)!=0 and iteracion<CANTIDAD_INTENTOS:
    
    print(f'Iteración {iteracion}:')
    
    # Desde la segunda iteración en adelante (iteración==1), iteramos sólo las que dieron ERROR
    if iteracion!=0:    
        # Obtener las partidos con resultado 'OK' del DataFrame
        partidos_con_ok = df_iteracion.loc[df_iteracion['resultado'] == 'OK', 'partido'].tolist()   
        # Filtrar el diccionario original eliminando las partidos con resultado 'OK'
        partidos_a_iterar = {partido: partido for partido, partido in partidos_a_iterar.items() if partido not in partidos_con_ok}

    partidos_restantes = ', '.join(partidos_a_iterar.keys())
    partidos_restantes_count = len(partidos_a_iterar)
    print(f'Restan las partidos ({partidos_restantes_count}): {partidos_restantes}.')

    # Se inicializa dataframe para guardar los resultados de cada iteración
    df_iteracion = pd.DataFrame()
     
    # Se crea un dataframe para guardar los resultados de cada partido
    
    df_super = []
    
    # Iteramos partido a partido
    for nombre_partido_item, partido_item in partidos_a_iterar.items():

        print(f'\nSe ejecuta el siguiente lote: {nombre_partido_item} - {partido_item} ', end="")
        try: # Se hace la llamada a la función
        
            
            driver_navegador = easy_session(
                                            codigo_partido=partido_item,
                                            verbose=True
                                            )
            
            #########################################################
            # Aquí deberían ir las funciones de scraping de precios #
            #########################################################
            
            
            RESULTADO = 'OK'
            DESCRIPCION_ERROR = None
            

            df_precios = scraping_easy(driver=driver_navegador,
                                       secciones=secciones,
                                       max_paginas=max_paginas,
                                       codigo_partido=nombre_partido_item,
                                       verbose=True)
                                      
            #Se van juntando los data.frames de cada iteración
            df_super.append(df_precios[1])
                
            
                    
            
            
        except Exception as e:

            RESULTADO = 'ERROR'
            DESCRIPCION_ERROR = str(e)
    
        # Incorporo el resultado al print en pantalla
        print(f'{RESULTADO}.')
        
        # Incorporo los resultados al df de esta iteración
        iteracion_partido = pd.DataFrame({'partido': [partido_item], 
                                           'resultado': [RESULTADO],
                                           'descripcion_error': [DESCRIPCION_ERROR]})
        
        df_iteracion = pd.concat([df_iteracion, iteracion_partido], ignore_index=True)
        
        # Se define un tiempo random entre un request y otro
        # Igualmente habría que evaluar definir múltiples usuarios
        tiempo_espera = random.uniform(1, 10)
        print(f"Se esperarán {round(tiempo_espera, 2)} segundos para el próximo GET.\n")
        time.sleep(tiempo_espera)
        
        if RESULTADO == 'OK':
            driver_navegador.close()
        
        #Se concatena el data.frame general por iteración
        if df_super:  # Verificar si se ha recolectado al menos un DataFrame
        # Concatenar los DataFrames de todas las secciones
           final_tienda = pd.concat(df_super, ignore_index=True)
        
        else:
          print("No se guardó el data.frame")

    # Se guardan los resultados de la iteración en un diccionario y se incrementa en 1 el contador
    dict_iteraciones[iteracion] = df_iteracion
    iteracion+=1
    
    # Se va guardando la suma de data.frame para cada interacción
    df_super_total.append(final_tienda)
    
    if df_super_total:
      final_tienda_total = pd.concat(df_super_total, ignore_index=True)
    
    else:
      print("No se guardó la suma de data.frames por iteración")
      
    # Guardar el data.frame total en excel:
    final_tienda_total.to_excel(excel_filename,sheet_name=excel_sheet_name, index=False)
    
end_time = time.time()
elapsed_time_seconds = end_time - start_time
elapsed_minutes = int(elapsed_time_seconds // 60)
elapsed_seconds = int(elapsed_time_seconds % 60)

print(f"El tiempo de ejecución del script de {CADENA} fue de: {elapsed_minutes} minutos y {elapsed_seconds} segundos")
