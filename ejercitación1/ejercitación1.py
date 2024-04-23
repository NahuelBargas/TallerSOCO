# Ejercitación taller 'Web Scraping con Python y Selenium'

# Nahuel Bargas

## Punto 1

''' Selecciono Easy : https://www.easy.com.ar/ '''

## Punto 2

'''

Etiqueta: link, línea 16 del código de fuente de la página

a) Según 'w3schools' se utiliza para vincular hojas de estilos externas e íconos para la la url en los navegadores.

b) rel, class, href, as, crossorigin, id, onload, onerror

c) rel ='preload' indica que el navegador debe tener cómo prioridad cargar este recurso al comienzo de la consulta.
   class ='vtex_io_uncritical_css' Es el nombre de la clase del elemento y se asocia con un estilo.
   href ='https://...' Indica la ubicación del elemento a cargar.
   as ='style' Especifica el contenido cargado por el elemento. Cuando se establece rel="preload", es prioritario su definición.   
   crossorigin = '' Establece cómo responde el elemento ante consultas de origen cruzado.
   id = 'uncritical_style_0' Es la clave única de identificación del elemento.
   onload="..." La acción llevada a cabo cuando se carga el elemento.
   onerror="..." El script a ejecutar cuando ocurre un error al cargar el elemento.
   
   
Etiqueta: noscript, línea 17 del código de fuente de la página

a) Según 'w3schools' define el contenido a mostrar para los usuarios que hayan deshabilitado los scripts en sus navegadores o
   que posean un navegador que no soporte scripts.
   
b) id

c) id="styles_overrides" Es la clave única de identificación del elemento.


Etiqueta: template, línea 237 del código de fuente de la página

a) Siguiendo con 'w3schools', sirve para mantener cierto contenido HTML escondido para la vista del usuario hasta que la página se cargue.
   Posteriormente, el contenido puede ser 'renderizado' via JavaScript.
   
b) data-type, data-varname

c) Ambos atributos brindan la posibilidad de meter datos personalizados en el elemento  y luego pueden ser utilizados 
   en alguna función de JavaScrip para mejorar la experiencia del usuario al navegar por la web. 

   
'''

### Punto 3

'''

a) html, head, meta charset=”utf-8″, title, style, body, h1, p, table, thead,tbody, tr, td, a, div y img.

b) y c)

html :

lang="es". Indica el lenguaje de la página


h1:

align="center" . La alineación horizontal del texto del encabezado más grande.
class="marca".  El nombre de la clase del elemento.

p: 

align="center".  La alineación horizontal del texto del elemento p.

table:

border="1" El tipo de borde de la tabla. Con el valor '1', el grosor del borde es más fino.

align="center" La alineación de la tabla en la página web. En este caso, centrada.

td:

class="marca". El nombre de la clase del elemento.

a:

href="" El hipervínculo del link, es una dirección hacía un elemento exterior.


div:

class='image-container'. El nombre de la clase del elemento.

img

src= "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" La ubicación del archivo en formato imágen.

alt= "Logo de Python". La descripción de la imágen. Es útil para que los navegadores identifiquen el contenido de la imágen y ayuda 
                       a las personas con disminución visual que utilizan programas de lectura.


'''

## Punto 4

from bs4 import BeautifulSoup
import requests

### Web
url = "https://raw.githubusercontent.com/jumafernandez/soco-web_scraping/main/data/encuentro-01/example-01.html"

### Consulta a la url
response = requests.get(url)

### Obtener el html

print(response.text)

### otra forma utilizando BeautifulSoup

html_bruto = BeautifulSoup(response.text, 'html.parser')
print(html_bruto.prettify())

## Punto 5




### a) Obtener el título del documento:

print(html_bruto.find('title').get_text())


### b) Cargar la tabla en un data.frame

import pandas as pd # importar pandas

tabla= html_bruto.find('table') #obtener la tabla en base al elemento


nombre_lista = [] 
enlaces_lista =[]

for fila in tabla.tbody.find_all('tr'):    
    columnas = fila.find_all('td')
    
    if(columnas != []):
       nombre = columnas[0].text
       enlace = columnas[1].text
       nombre_lista.append(nombre)
       enlaces_lista.append(enlace)
	   
	   
df = pd.DataFrame({'tienda': nombre_lista, 'sitio_web' : enlaces_lista})



### c) 


elementos_p = html_bruto.find_all('p')

for i in range((len(elementos_p)-1),1):
                            print(elementos_p[i].get_text())

### d) 

filas_marca = html_bruto.find_all('td', class_='marca')

filas_marca_texto_lista = []
for j in range(0,len(filas_marca),1):
                            texto = filas_marca[j].get_text()
                            filas_marca_texto_lista.append(texto)

marca_que_cumplen_condicion = []

for palabra in filas_marca_texto_lista:
    if palabra.endswith('o'):
        marca_que_cumplen_condicion.append(palabra)
        
print(marca_que_cumplen_condicion)


### e) 'Guardar tabla en excel'

df.to_excel('Tabla_ejercitación_1.xlsx',index=False)