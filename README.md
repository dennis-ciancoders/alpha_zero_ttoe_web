# Proyecto de prueba inicial de Tensorflow y Keras, con frontend en javascript

**Estudiante**: Dennis Xiloj
**Carnet**: 22006829


Para ejecutar este proyecto se debe instalar los requerimientos de python con el comando:

pip install -r requirements.txt

Para ejecutar el proyecto se debe ejecutar el comando:

python manage.py runserver

Despues de esto el proyecto se ejecutara en el puerto 8000, solo es necesario visitar la
url http://localhost:8000


Si no se puede ejecutar el proyecto, se puede ver una version en funcionamiento en la url
https://playagainst.ai/



## Directorios importantes:


**/ttoe**: Contiene el codigo de la aplicacion, backend y frontend
**/ttoe/ai**: Contiene el codigo de la inteligencia artificial y el modelo en .h5 (no transformado a javascript)
**/ttoe/serializers.py**: Contiene el código de backend que hace funcionar al modelo pre-entrenado
**/ttoe/templates/index.html**: Contiene el codigo del frontend, html y javascript
**/ttoe/static/ttoe**: Contiene los archivos de estilos y javascript