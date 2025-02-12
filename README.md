# Buratovich Hnos
Corporate Website developed with Python + Django stack using VanillaJs, CSS3, HTML5 and SQLite.

You can visit the site in [www.buratovich.com](www.buratovich.com)

![Buratovich Hnos](https://repository-images.githubusercontent.com/77139687/fb51bb80-ab5c-11ea-9fe1-064ea36da44d)

# Entorno de prueba en Windows

## 1. 64bits

Verificar la arquitectura del procesador y el que el python también sea de 64bits.

## 2. Remote Signed

Habilitar la ejecución de scripts en Windows.

```sh
Set-ExecutionPolicy remotesigned
```

## 3. Actualizar pip

```sh
python -m pip install --upgrade pip
```

## 4. Descargar VS Build Tools

<a>https://visualstudio.microsoft.com/es/downloads/?q=build+tools</a>

Luego de instalarlo, elegir la opción de caracteristicas principales e instalar.

## 5. SQL Server

Instalar mySQL desde <a>https://dev.mysql.com/downloads/installer/</a>

Verificar que esté en las variables de entorno de windows, si no está, agregarlo manualmente.

## 6. Instalar la lista de requerimientos de testing

```sh
pip install -r "requirements_test.txt"
```