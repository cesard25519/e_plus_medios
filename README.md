Hola, César: # olaw

Gracias por postularte a la vacante de
<. Ingeniero de Operaciones y Plataforma (DevOps / Python) de E+ Medios .>

Revisamos tu perfil y queremos que avances a la siguiente etapa: tres ejercicios cortos que son nuestro primer filtro y pesan más que el CV.


Los dos primeros caben en una cuartilla; el tercero es un script.

EJERCICIO 1 — Diagnóstico
Una tarea programada # chrono
corre cada 10 minutos # 600
en una Mac mini que funciona como servidor # problema especifico IOS?
Su log muestra, ciclo tras ciclo, estas tres líneas:

  2026-10-14 12:08:47 --- ciclo inicio ---
  Failed to authenticate: OAuth session expired and could not be refreshed
  2026-10-14 12:08:48 --- ciclo fin (exit 0) ---

  """
  2026-10-14 12:18:47 --- ciclo inicio ---
  Failed to authenticate: OAuth session expired and could not be refreshed
  2026-10-14 12:18:48 --- ciclo fin (exit 0) ---

  2026-10-14 12:28:47 --- ciclo inicio ---
  Failed to authenticate: OAuth session expired and could not be refreshed
  2026-10-14 12:28:48 --- ciclo fin (exit 0) ---

  ... # asi sucesivamente (?)
  """

El tablero de monitoreo marca la tarea en verde. # se ejecuta exitosamente por lo que podria ser problema del codigo fuente, a lo mejor una excepcion mal manejada
a) ¿Qué está pasando y cómo averiguarías desde cuándo? # revision de logs buscando "OAuth session expired"
b) ¿Qué harías hoy para arreglarlo? # re autenticarse? verificar script? re-hacer script (depende de que tan largo sea, muchas veces es mas sencillo hacer desde cero que intentar moverle)
c) ¿Qué cambiarías para que una tarea que corre pero no hace nada nunca vuelva a aparecer en verde? # dependeria de que tan permisivos sean en el entorno

EJERCICIO 2 — Secretos
Descubres que la contraseña de la base de datos de producción está escrita en un archivo de log que varias personas pueden leer, y que el proceso la sigue escribiendo en cada corrida. # cargarse las variables de una
Describe, en orden, los pasos que darías en la primera hora y en la primera semana. # instantaneamente cambiar la clave y despues revisaer que tanto afecto; entre mas tiempo pase mas problemas habra; seguido verificaria desde cuando esta suelta; revisar actividad sospechosa e intentar revertir ciertos temas (no especifico ya que es un borrador)

EJERCICIO 3 — Script
Escribe un script en Python (máximo 60 líneas) # ez
que reciba una lista de dominios de sitios WordPress, Domain[] || list[Domain]
verifique para cada uno que el sitio responde # cualquier status_code?
y que su nota más reciente tiene menos de 24 horas (la API pública de WordPress está en /wp-json/wp/v2/posts?per_page=1), # preguntar a gemini, algo superficial pero suficiente
e imprima un resumen con los sitios que fallan. Adjúntalo o compártelo como enlace a un gist. # try: httpx.get(DomainURL); Domains.append(DomainURL); excepcion Exception: print(DomainURL + 'is not valid') # o algo asi; importara el status_code?

CÓMO ENTREGAR
Responde a este mismo correo con tus respuestas antes del miércoles 22 de octubre a las 23:59 (hora de la Ciudad de México). # oka
Si tienes perfil de GitHub o GitLab, inclúyelo. # usar el secundario por ser de pruebas; deberia el repositorio ser publico o privado?
Los finalistas tendrán una entrevista técnica de 30 minutos con un caso real en pantalla, # estudiar cmd otra vez para no congelarme como la ota vez
entre el 27 y el 28 de octubre. # creo que es luns

Cualquier duda, por aquí.

Saludos,
Talento · E+ Medios
talento@emasmedios.com

