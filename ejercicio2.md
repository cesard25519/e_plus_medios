# EJERCICIO 2 — Secretos

Descubres que la contraseña de la base de datos de producción está escrita en un archivo de log
que varias personas pueden leer, y que el proceso la sigue escribiendo en cada corrida.
Describe, en orden, los pasos que darías en la primera hora y en la primera semana.


# Primera hora

al darme cuenta de que el token es visible en los logs, lo primero que haria es deprecar el token y poner el sistema en modo mantenimientto para restringir operaciones temporalmente para minimizar danos

seguido de esto, buscaria en los logs el registro mas antiguo donde se mencione el token para poder saber desde cuando es visible

al saber desde cuando es posible verlo mas o menos comprenderia que tan a tiempo se reacciono

seguido de esto, buscaria el codigo fuente que emitio el token para cambiarlo y corregirlo para poder deployarlo despues

al tener la version estable del nuevo codigo fuente, ahora si buscaria subirlo para poder ahora si bajar el modo mantenimiento y volver a la normalidad

el modo mantenimiento es vital para poder hacer que el usuario no se alarme ya que este estaria ansioso si de momento ve errores en toda operacion que hace por el contrario de ver un "estamos en mantenimiento" y esperar, es mas tolerable esto


# Primera semana

crearia un script para observar trafico extrano a la base de datos o inclusive ver si la plataforma donde esta corriendo el programa puede bloquear el token; cambiaria la db completamente a otro servidor; haria una copia de seguridad en otro servidor (si aplica) y estaria al pendiente de que los logs no muestren el token o permisos relacionadoos a este

haria un script basico de revision de logs cada 5 minutos o un tiempo parecido para buscar algun log de el token

si es posible crear reglas propias, bloquear el token directamente haria bastante efecto al no permitir actividad

se podrian hacer guardias anti-fraude o similares para verificar actividad extrana

revisaria las operaciones en db durante el primer dia de loggeado el token para ver si hubo alguna operacion anormal como el crear otro usuario de lectura, otro usuario de escritura, la creacion de registros fraude para usarse despues, buscar ataques tipo xss para eliminarlos directamente, eliminar y cambiar caracteres especiales para evitar problemas de interpretacion, ...


