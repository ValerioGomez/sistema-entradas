Sistema de Entradas
===================

Este repositorio contiene el código fuente del sistema de entradas, listo para ser desplegado y utilizado.

Clonar el repositorio
---------------------

Para comenzar, clone este repositorio en su máquina local con el siguiente comando:

    git clone https://github.com/ValerioGomez/sistema-entradas.git
    cd sistema-entradas

Instalación de dependencias
---------------------------

Instale las dependencias necesarias utilizando el siguiente comando:

    python -m pip install -r requirements.txt

Ejecución del servidor
----------------------

Para ejecutar el servidor, utilice el siguiente comando:

    uvicorn api_server:app --host 0.0.0.0 --port 8000

Nota sobre despliegue en múltiples nodos
----------------------------------------

Este sistema puede desplegarse en diferentes nodos o computadoras. Por lo tanto, es necesario ejecutar el comando
`uvicorn` en cada nodo por separado, asegurándose de que cada instancia se ejecute con la configuración adecuada
para su entorno y red.

Documentación
-------------

En este repositorio también encontrará documentación técnica que detalla la instalación, configuración y uso del sistema.

¡Gracias por usar este proyecto!
