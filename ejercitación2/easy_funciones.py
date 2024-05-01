from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.edge.service import Service
import pandas as pd
import time




# Configuración del WebDriver para Edge
options = webdriver.EdgeOptions()

options.add_argument("--start-maximized")  #esto sirve maximizar el tamaño de la pantalla del webdriver.
#options.add_argument("--headless") # esto sirve para correr en segundo plano sin que se abra ventana.




def easy_session(codigo_partido, verbose=False):
    # Creación del WebDriver de Edge
    driver = webdriver.Edge(options=options)
    
    # Esperar a que la página cargue completamente
    time.sleep(5)
    
    sitio_web = 'https://www.easy.com.ar/'
    
    # Accede al sitio web y espera 10 segundos
    driver.get(sitio_web)
    
    time.sleep(10)
    
    if verbose:
            print(f'1. Se hace el GET a {sitio_web}')
            
    # Se toca el botón a ingresar ubicación
    
    try:
            # Encontrar el elemento por su clase
            icono_ubicacion = driver.find_element(By.CLASS_NAME, "arcencohogareasy-cencosud-polygon-1-x-GeoSecondaryButton")
            # Hacer clic en el elemento
            icono_ubicacion.click()
    except StaleElementReferenceException:
            # Encontrar el elemento por su clase
            icono_ubicacion = driver.find_element(By.CLASS_NAME, "arcencohogareasy-cencosud-polygon-1-x-GeoSecondaryButton")
            # Hacer clic en el elemento
            icono_ubicacion.click()       
    
    if verbose:
            print('2. Se presiona el botón "Ingresa tu ubicación"')
    
    
    # Se ingresa el código de partido
    
    time.sleep(1) #Esperar 1 segundo
    codigo_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Introduce una ubicación"]')
    
    codigo_input.send_keys(codigo_partido)
    
    if verbose:
            print('3. Se ingresa el código del partido:  {codigo_partido}')
    
    # Se seleciona la primera opción del desplegable
    
    time.sleep(2) #Esperar 2 segundos
    
    driver.find_element(By.XPATH, "//button[contains(@class,'bn tl pointer')]").click()
    
    if verbose:
            print('4. Se selecciona el código del partido:  {codigo_partido}')
    
    # Se confirma la selección
    
    time.sleep(2) #Esperar 2 segundos
    
    driver.find_element(By.XPATH, "//button[contains(@class,'rcencohogareasy-cencosud-polygon-1-x-ConfirmButton')]").click()
    
    if verbose:
            print('5. Se confirma la selección del partido')
    
    # Se cierra el botón para subscribirse
    
    time.sleep(5) #Esperar 5 segundos para que se cargue la página
    
    rechazar_subs = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.ID, "btnNoIdWpnPush")))
    rechazar_subs.click()
    
    time.sleep(2)
    
    if verbose:
            print('6. Se cierra la opción de subscripción')
            
    return driver
    
def scraping_easy(driver, secciones, max_paginas, codigo_partido, verbose=False):
    if verbose:
        print('Scraping de EASY:\n')
        
    # Definir fecha actual
    fecha_actual = date.today().strftime('%d-%m-%Y')

    # Inicializar una lista para almacenar los DataFrames
    dfs_paginas = []
    
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
                    EC.presence_of_element_located((By.ID,
                                                    "gallery-layout-container"))
                )
            except TimeoutException:
                print(f"No se encontraron productos de {seccion} en la página {i}. Saltando a la siguiente sección.")
                break  # Salir del bucle interno si no se encuentra el contenedor en la página actual

            articulos = contenedor.find_elements(By.XPATH,
                                                 ".//section[contains(@class, 'vtex-product-summary-2-x-container')]" )

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
                    nombre_producto = articulo.find_element(By.XPATH,".//div[contains(@class,'vtex-product-summary-2-x-nameContainer')]").text
                    
                    precio_producto = articulo.find_element(By.XPATH,
                                                            ".//div[contains(@class,'sellingPriceDiv')]").text

                    link = articulo.find_element(By.XPATH, ".//a[contains(@class,'vtex-product-summary-2-x-clearLink')]").get_attribute("href")
                
                    marca = articulo.find_element(By.XPATH, ".//span[contains(@class,'vtex-product-summary-2-x-productBrandName')]").text
                    
                    try:
                        precio_lista = articulo.find_element(By.XPATH,".//div[contains(@class,'npprodSinDesc')]").text

                    except NoSuchElementException:
                        precio_lista = float('nan')

                    
                    try:
                        promocion = articulo.find_element(By.XPATH,                       
                                                            ".//span[@class='vtex-product-price-1-x-savings vtex-product-price-1-x-savings--shelf-discount-price']/span").text
                    
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
            print(lista_marca)
            print(len(lista_marca))

            # Crear un DataFrame con los datos
            data = {'Fecha_relevamiento': fecha_actual,
                    'Partido': codigo_partido,
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

            df[['Precio', 'Precio_tachado']] = df[['Precio', 'Precio_tachado']].astype(str).apply(lambda x: x.str.replace('$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.',regex=False))
            
            ## Convertir la columna 'Precio' y 'Precio_tachado' a valores numéricos
            df[['Precio', 'Precio_tachado']] = df[['Precio', 'Precio_tachado']].apply(pd.to_numeric, errors='coerce')
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
            df['Descuento'] = round(1 - (df['Precio'] / df['Precio_tachado']), 2)
            #
            ## Agregar el DataFrame a la lista
            dfs_paginas.append(df)

    if dfs_paginas:  # Verificar si se ha recolectado al menos un DataFrame
        # Concatenar los DataFrames de todas las secciones
        final_df = pd.concat(dfs_paginas, ignore_index=True)
        
    else:
        print("No se encontraron productos en ninguna sección.")
        
    return driver, final_df


    
if __name__ == "__main__":

  codigo_partido = ('San Martín', 1650)
  
  max_paginas = 5

  secciones = [
    "pinturas/de-interior",
    "iluminacion-y-deco/iluminacion",
    "automotor/neumaticos-y-accesorios/neumaticos",
    "muebles-de-interior/comedor"
    ]
  
  driver_edge = easy_session(codigo_partido=codigo_partido[1],verbose=True)
  
  df_precios = scraping_easy(driver=driver_edge,
                             secciones=secciones,
                             max_paginas=max_paginas,
                             codigo_partido=codigo_partido[0],
                             verbose=True)
