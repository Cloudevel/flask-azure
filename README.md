# flask-azure

Notebooks de [Jupyter](https://jupyter.org) que incluyen los apuntes del webinar sobre la creación de una web app de Azure para desplegar un servicio API REST. 

Una de las notebooks se debe de ejecutar utilizando el [kernel de Bash](https://github.com/takluyver/bash_kernel).

## Nuestra máquina virtual.

Para facilitar la instalación y configuración tanto de Jupyter como del kernel de Bash se recomienda descargar nuestra VM de [Virtualbox](https://virtualbox.org) la cual puede ser descargada desde https://cloudevel.com/downloads/base/view. Una vez que se ejecute la VM podrá acceder a un servidor de Jupyter totalmente funcional ingresando desde el navegador de su equipo en la dirección ```http://localhost:8999``` con la contraseña ```Jupyter```.

## Clonación del repositorio.

Para clonar el repositorio en su sistema de archivos local, ejecute desde una terminal:

``` bash
git clone https://github.com/Cloudevel/flask-azure.git
```

## Contenido:

* La notebook [01_azure_web_app.ipynb](01_azure_web_app.ipynb) corriendo el kernel de Bash, la cual incluye los apuntes con el procedimiento paso a paso para crear una apicación web con Azure. El último paso para publicar la aplicación se debe de hacer desde una terminal, tal como se inidca en los apuntes.

* La notebook [02_cliente_api_rest.ipynb](02_cliente_api_rest.ipynb) corriendo un kernel de Python contiene código capaz de consumir la API publicada.
