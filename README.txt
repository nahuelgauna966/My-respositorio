README - Trabajo Práctico: menú de carpetas (Gauna Nahuel)

El script crea un workspace en /tmp/tp_carpetas_$USER y trabaja solo allí.
Usé mkdir para crear directorios, mv para renombrar, rmdir para borrar si están vacíos,
y rm -r (solo si el usuario lo confirma) para forzar borrado recursivo. Para listar
directorio de nivel 1 empleé find -maxdepth 1 -type d y ordené con sort. Las entradas
se leen con read y validé nombres (sin rutas absolutas, '/', '.' o '..') usando sed para
recortar espacios y comprobaciones en bash. El menú funciona en un bucle while con case,
mostrando mensajes claros de error/éxito.
