#  Índice Invertido, Proyecto BD2


## Integrantes
|  **#** | **Código** | **Apellidos, Nombre** | **% Trabajo** |
| :---: | :---: | :---: | :---: |
|  1 | 201810142 |Madera Garces, Cesar Antonio | 100% |
|  2 | 201810245 |Sobrados Burgos, Enrique Francisco | 100% |
|  3 | 201810614 |Villegas Suárez, Ariana Mirella | 100% |

## Ejecución del proyecto: 

cd web/
python3 server.py

Ingresar a localhost:8080

## Backend

### Preprocesamiento

- API de twitter \
Para obtener los tweets creamos dos métodos: 
    - get_tweets(busqueda, num):
        Esta función va a recibir un parametro llamado "busqueda", el cual va a servir para hacer filtrar los resultados con respecto a este parámetro. El segundo parámetro va a ser el número de tweets que vamos a retornar con esta función. Se utilizó la función Cursos de la librería tweepy para lograr esto. 
    - get_tweet_by_id(id) :
        Esta función va a ser útil al momento de tener los ids de los tweets, éste pueda retornar el tweet y poder tener todas sus atributos.  Esto se logró gracias a que la función "get_status" de la librería tweepy, recibe el id del tweet el cual es un entero y este te retorna el tweet como objeto.

- Tokenization, filtrar Stopwords y reducción de palabras (Stemming)

- Cada tweet sigue los siguientes pasos:

    - Pasa todos los caracteres a minúsculas.
    - Filtrar los caracteres especiales.
    - Filtrar websites y etiquetas.
    - Filtrar los stopwords.
    - Dividir el tweet en keywords.
    - Aplicar un stemmer para guardar solo las raíces de las palabras.

### Construcción del Índice

- Bloques en memoria secundaria:
    Los bloques almacenan tripletas con el término, el id del documento y el número de veces que se repite el término. Además, el tamaño del bloque es determinado por el usuario.

**Bloque 1**
|  **term** | **doc_id** | **count** |
| :---: | :---: | :---: |
|  manzan | 149 | 3 |
|  principito | 215 | 13 |
|  mund | 201 | 7 |

- Construcción del índice:	
	Para construir el índice se siguen los siguientes pasos:
    - Tokenización y filtrado del query.
    - Extraer las entradas de los bloques que coinciden con algún token del query.
    - Combinar las entradas de los bloques y formar el índice invertido.


### Consulta
Para obtener los resultados del query se siguen los siguientes pasos:
- Construir el índice basado en el query.
- Obtener el cosine score para cada tweet.
- Ordenar los tweets basados en su score.
- Obtener los primeros k tweet ids, donde k es un número ingresado por el usuario.
- Después de obtener los ids, se utiliza nuevamente el api de twitter para obtener todo el tweet.
- Una vez obtenidos los tweets completos, se devuelve al frontend y se muestra al usuario.


## Frontend

Aparecerá la pantalla del index, y se ingresa a “get started” o a la opcion “queries” para ingresar a la pantalla de visualizacion de queries.

Dentro de la pantalla de query, se le da al usuario 4 opciones: 
- Obtener un tweet por su id.
- Insertar una cantidad de tweets( y setear el tamaño de los bloques del indice invertido)
- Eliminar los bloques ya creados
- Realizar una query y setear la cantidad de resultados que se espera obtener.

Las queries pueden ser en lenguaje natural y se podran visualizar los resultados en sus tablas ya pre-definidas por seccion: una seccion unicamente para las consultas por id y la otra para las queries de lenguaje natural.

Para pasar la informacion de frontend a backend se esta utilizando json y jquery. 

## Servidor: 

Cada opcion esta llamando a una ruta diferente en el servidor: 
- POST: /query esta escuchando a las peticiones de una query por Id;
- POST: /busqueda esta escuchando a las peticiones por una query de lenguaje natural 
- DELETE: /eliminar esta escuchando la peticion de borrado del indice en el servidor
- POST: /create esta escuchando a la peticion de añadir tweets. 
