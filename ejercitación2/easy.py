from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.edge.service import Service
import pandas as pd
import time

start_time = time.time()

# Configuración del WebDriver para Edge
options = webdriver.EdgeOptions()

options.add_argument("--start-maximized")  #esto sirve maximizar el tamaño de la pantalla del webdriver.
#options.add_argument("--headless") # esto sirve para correr en segundo plano sin que se abra ventana.

# Creación del WebDriver de Edge
driver = webdriver.Edge(options=options)

# Esperar a que la página cargue completamente
time.sleep(5)

# Definir fecha actual
fecha_actual = date.today().strftime('%d-%m-%Y')

# Resolver paginación
max_paginas = 1

secciones = [
    #"pinturas/de-interior",
    #"iluminacion-y-deco/iluminacion",
    "automotor/neumaticos-y-accesorios/neumaticos",
    ]

excel_filename = f"easy_scrap_{fecha_actual}.xlsx"

# Inicializar una lista para almacenar los DataFrames
dfs = []

with (pd.ExcelWriter(excel_filename, engine='openpyxl') as writer):
    for seccion in secciones:
        categoria = seccion.split("/")[-1]
        for i in range(1, max_paginas + 1):
            try:
                web_easy = f"https://www.easy.com.ar/{seccion}?page={i}"
                driver.get(web_easy)
                time.sleep(3)

                # Realizar un desplazamiento gradual hacia abajo en la página
                scroll_step = 1200  # Ajusta el valor según la cantidad de desplazamiento deseado
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                current_scroll = 0

                while current_scroll < scroll_height:
                    driver.execute_script(f"window.scrollTo(0, {current_scroll + scroll_step});")
                    time.sleep(1)
                    current_scroll += scroll_step

                    # Espera adicional para cargar contenido si es necesario
                    #time.sleep(2)

            except NoSuchElementException:
                print(f"La página {i} no existe.")
                break

            try:
                contenedor = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//div[contains(@class, 'vtex-search-result-3-x-loadingOverlay w-100 flex flex-column flex-grow-1 vtex-search-result-3-x-container--layout')]"))
                )
            except TimeoutException:
                print(f"No se encontraron productos de {seccion} en la página {i}. Saltando a la siguiente sección.")
                break  # Salir del bucle interno si no se encuentra el contenedor en la página actual

            articulos = contenedor.find_elements(By.XPATH,
                                                 "//div[contains(@class, 'flex mt0 mb0 pt0 pb0    justify-start vtex-flex-layout-0-x-flexRowContent items-stretch w-100')]" )

            # Inicializar las listas donde se van a cargar los datos
            lista_productos = []
            lista_precios = []
            lista_precios_lista = []
            lista_links = []
            lista_precio_regular = []
            lista_promociones = []
            lista_marca =[]

            for articulo in articulos:
                try:
                    nombre_producto = articulo.find_element(By.XPATH,"//div[contains(@class,'vtex-product-summary-2-x-nameContainer')]").text
                    
                    precio_producto = articulo.find_element(By.XPATH,
                                                            "//div[contains(@class,'sellingPriceDiv')]").text

                    link = articulo.find_element(By.XPATH, "//a[contains(@class,'vtex-product-summary-2-x-clearLink')]").get_attribute("href")
                
                    marca = articulo.find_element(By.XPATH, "//span[contains(@class,'vtex-product-summary-2-x-productBrandName')]").text
                    
                    try:
                        precio_lista = articulo.find_element(By.XPATH,"//div[contains(@class,'npprodSinDesc')]").text

                    except NoSuchElementException:
                        precio_lista = float('nan')

                    
                    try:
                        promocion = articulo.find_element(By.XPATH,                       
                                                            "//span[@class='vtex-product-price-1-x-savingsPercentage']").text
                    
                    except NoSuchElementException:
                        promocion = None

                    lista_productos.append(nombre_producto)
                    lista_precios.append(precio_producto)
                    lista_precios_lista.append(precio_lista)
                    lista_links.append(link)
                    lista_promociones.append(promocion)
                    lista_marca.append(marca)

                except StaleElementReferenceException:
                    print("El elemento se volvió 'stale'. Volviendo a buscarlo.")
                    driver.refresh()  # Refrescar la página
                    time.sleep(5)

                except NoSuchElementException as e:
                    print(f"No se encontró el elemento: {e}")

            print(lista_productos)
            print(len(lista_productos))
            print(lista_precios)
            print(len(lista_precios))
            print(lista_precios_lista)
            print(len(lista_precios_lista))
            print(lista_links)
            print(len(lista_links))
            print(lista_promociones)
            print(len(lista_promociones))
            print(marca)
            print(len(marca))

            # Crear un DataFrame con los datos
            data = {'Fecha_relevamiento': fecha_actual,
                    'Cod_informante': 'EA1',
                    'Informante': "EASY",
                    'Link': lista_links,
                    'Categoría': categoria,
                    'Producto': lista_productos,
                    'Precio': lista_precios,
                    'Precio_tachado': lista_precios_lista,
                    'Promociones': lista_promociones,
                    'Marca': lista_marca,
                    }
            df = pd.DataFrame(data)

            #df[['Precio', 'Precio_tachado']] = df[['Precio', 'Precio_tachado']].astype(str).apply(lambda x: x.str.replace('$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.',regex=False))
            #
            ## Convertir la columna 'Precio' y 'Precio_tachado' a valores numéricos
            #df[['Precio', 'Precio_tachado']] = df[['Precio', 'Precio_tachado']].apply(pd.to_numeric, errors='coerce')
            #
            ## Convertir la columna a tipo string
            #df['Precio_regular'] = df['Precio_regular'].astype(str)
            #
            ## Definir patrón de expresión regular para el precio y la unidad de medida
            #patron = r'\(\$([\d,\.]+) x ([A-Z]+)\)'
            #
            ## Aplicar la expresión regular para extraer el precio y la unidad de medida
            #df[['Precio_regular_final', 'Unidad_de_medida']] = df['Precio_regular'].str.extract(patron)
            #
            ## Limpiar el formato del precio_regular_final(eliminar comas y convertir a flotante)
            #df['Precio_regular_final'] = df['Precio_regular_final'].str.replace('.', '', regex=False).str.replace(',', '.',regex=False).astype(float)
            #
            ## Calcular el descuento y agregarlo como una nueva columna al DataFrame
            #df['Descuento'] = round(1 - (df['Precio'] / df['Precio_tachado']), 2)
            #
            ## Agregar el DataFrame a la lista
            #dfs.append(df)

    if dfs:  # Verificar si se ha recolectado al menos un DataFrame
        # Concatenar los DataFrames de todas las secciones
        final_df = pd.concat(dfs, ignore_index=True)

        # Escribir el DataFrame en el archivo Excel
        final_df.to_excel(writer, sheet_name='Easy', index=False)
    else:
        print("No se encontraron productos en ninguna sección.")

driver.quit()

end_time = time.time()
elapsed_time_seconds = end_time - start_time
elapsed_minutes = int(elapsed_time_seconds // 60)
elapsed_seconds = int(elapsed_time_seconds % 60)

print(f"El tiempo de ejecución del script de EASY fue de: {elapsed_minutes} minutos y {elapsed_seconds} segundos")
