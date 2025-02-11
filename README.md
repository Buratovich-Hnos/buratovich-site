# Buratovich Hnos
Corporate Website developed with Python + Django stack using VanillaJs, CSS3, HTML5 and SQLite.

You can visit the site in [www.buratovich.com](www.buratovich.com)

![Buratovich Hnos](https://repository-images.githubusercontent.com/77139687/fb51bb80-ab5c-11ea-9fe1-064ea36da44d)

# Testing

El siguiente proceso es realizado para levantar el sistema en un entorno de prueba en windows.

## 1. Verificar que la versión de python sea para 64bits
Este equipo, click derecho, propiedades.
## 2. Establecer las politicas de entorno Remote Signed como Sí
Abrir el powershell como administrador y ejecutar:
```sh
Set-ExecutionPolicy RemoteSigned
```
Luego insertar 'S'
## 3. Actualizar pip
```sh
python -m pip install --upgrade pip
```
## 4. Crear un entorno virtual
Puedes ejecutar el siguiente comando:
```sh
python -m venv nombre_del_entorno
```

## 5. Instalar setuptools
```sh
pip install setuptools
```
## 6. Instalar Visual Studio Tools
Luego de instalarlo desde el sitio oficial desde el apartado de Herramientas para visual studio, instalaremos solo las caracterisiticas principales.

Desarollo C++ para escritorio.

<a>https://visualstudio.microsoft.com/es/downloads/</a>

## 7. Instalar MySqlServer

Desde aquí <a>https://dev.mysql.com/downloads/installer/</a>

Instalar el **mysql server** y si se quiere tambien el workbench.

## 8. Modificar requirements txt

Eliminar Pillow, Pytype y typed-ast.

Instalar las versiones más nuevas de cada dependencia, es decir, elimine en el txt las versiones (tener en cuenta la compatibilidad si es que afectó en algo)

## 9. Instalar requirements.txt
Ejecutar el comando:
```sh
pip install -r "requirements.txt"
```

