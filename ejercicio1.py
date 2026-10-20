# === === === === === EJERCICIO 1 - Diagnóstico === === === === === #
"""
    Una tarea programada corre cada 10 minutos en una Mac mini que funciona como servidor Su log muestra, ciclo tras ciclo, estas tres líneas:


  // === === === === === Formato y ejemplos === === === === === #
  <datetime.now> --- <msg> ---


  2026-10-14 12:08:47 --- ciclo inicio ---
  Failed to authenticate: OAuth session expired and could not be refreshed
  2026-10-14 12:08:48 --- ciclo fin (exit 0) ---


  2026-10-14 12:18:47 --- ciclo inicio ---
  Failed to authenticate: OAuth session expired and could not be refreshed
  2026-10-14 12:18:48 --- ciclo fin (exit 0) ---


  2026-10-14 12:28:47 --- ciclo inicio ---
  Failed to authenticate: OAuth session expired and could not be refreshed
  2026-10-14 12:28:48 --- ciclo fin (exit 0) ---


  ... # asi sucesivamente (?)
"""


# === === === === === El tablero de monitoreo marca la tarea en verde === === === === === #
"""
    La tarea al ser marcada en verde, esta confirma que estuvo en lo esperado por lo tanto, posiblemente este se ejecute en un bloque "global" de excepciones similar a:
    try:
        chrono_task()

    except Exception as e: print(e) # e == 'OAuth session expired anc colud not be refreshed'


    me esperaria ver algo como:
    res: Response = httpx.post(URL_SERVE, json=Payload, auth=AUTH_TOKEN_SERVE_NAME)

    o mejor dicho:
    res = httpx.post(...)

    con ello, este solo confirmaria que retorne un status code sin verificar cual seria dejando pasar cualquier cosa y con ello haciendo algo como:

    print(str(res.content))

    antes del try-except o inclusive dentro de este

    una mejora que personalmente haria seria algo como usar:

    res.raise_for_status()

    y con ello ahorraria problemas
"""

# === === === === === a) ¿Qué está pasando y cómo averiguarías desde cuándo? === === === === === #
"""
    revisar logs buscando el print/log con algo como:
    for log in logs:
        if 'Failed to authenticate' in log:
            print(log.datetime) # asumiendo que esten ordenados por fecha de el mas antiguo primero al mas nuevo como final
            return


    o revisar usando utilidades unix como:
    grep 'Failed to authenticate' /ruta/al/log | head -n 1


    si es sql usaria:
    SELECT * FROM logs
    WHERE msg lIKE '%Failed to authenticate%'
    ORDER BY date ASC
    LIMIT 1

"""

# === === === === === b) ¿Qué harías hoy para arreglarlo? === === === === === #
"""
    - podria hacer el proceso manualmente
    - re-hacer el script desde cero siendo cuidadoso en escribirlo
    - re-autenticar el script
    - buscar con chatgpt/deepseek alguna solucion por si es problema del servidor

    personalmente primero intentaria hacer una autenticacion y probar, en caso de no funcionar, revisar el script para arreglarlo y ver si es problema del codigo fuente, en caso de no serlo a lo mejor podria ser el propio servidor al haber un cambio; esto dependera

"""

# === === === === ===  c) ¿Qué cambiarías para que una tarea que corre pero no hace nada nunca vuelva a aparecer en verde? === === === === === #
"""
    volveria a escribir el script desde cero; dado que es un script, este posiblemente no pase de 200 LoC y con ello es algo bastante barato de escribir tanto manualmente como por un modelo ML
    tambien manejaria especificamente los casos que esperaria lanzando una excepcion ante algo extrano
"""


