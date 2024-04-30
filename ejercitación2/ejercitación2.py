# Ejercitación taller 'Web Scraping con Python y Selenium'

# Nahuel Bargas

# Punto 1


#a) 

# Librerías

from bs4 import BeautifulSoup
import requests
import pandas as pd

# Dirección web formulario

formulario = 'https://jumafernandez.github.io/soco-web_scraping/data/encuentro-02/formulario-tp.html'

# Consulta al formulario

response = requests.get(formulario)

html = BeautifulSoup(response.text, 'html.parser')

# Mostrar todos los elementos HTML


for elemento_html in html.find_all():
    print(elemento_html.name)
 
# Mostrar atributos


nombres_atributos = []
valor_atr = [] 

for elemento_html  in html.find_all():
   nombres_atributos += list(elemento_html.attrs)
   valor_atr += list(elemento_html.attrs.values())
   
data = {'Atributo': nombres_atributos,
        'Valor': valor_atr
                        }

df = pd.DataFrame(data)

print(df)
 


#b)

# Librerías
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


# Configuración del WebDriver para Chrome
options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")  # maximizar el tamaño de la pantalla del webdriver.


# Creación del WebDriver de Chrome
driver = webdriver.Chrome(options=options)



# Navegación en el formulario
driver.get(formulario)

## Correo
ingreso_correo = driver.find_element(By.ID, "email")
ingreso_correo.send_keys("nahuelbargas@hotmail.com")

## Password
ingreso_contraseña = driver.find_element(By.ID, "passwd")
ingreso_contraseña.send_keys("prueba")

## Botón que recuerda el ingreso
boton_recordar = driver.find_element(By.ID, "recordar")
boton_recordar.click()

## Botón que selecciona el país  
seleccionar_pais = driver.find_element(By.ID, "pais")
seleccionar_pais_boton = seleccionar_pais.find_element(By.XPATH, "//option[contains(text(), 'Uruguay')]")
seleccionar_pais_boton.click()

## Botón para ingresar nuestras credenciales
ingresar_credenciales = driver.find_element(By.CSS_SELECTOR,'button')
ingresar_credenciales.click()


## Mostrar en consola la ifnormación que se ingresó en el formulario

contenido_mostrado = driver.find_element(By.ID, "contenidoMostrado")

texto_ingresado = contenido_mostrado.find_elements(By.TAG_NAME, 'p')
texto_ingresado_lista = []

for texto in texto_ingresado:
   texto_ingresado_lista.append(texto.text)
   
print(texto_ingresado_lista)


# Punto 2



#script easy.py

            
