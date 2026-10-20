# EJERCICIO 1 - Diagnóstico

Una tarea programada corre cada 10 minutos en una Mac mini que funciona como servidor. Su log muestra, ciclo tras ciclo, estas tres líneas:



### Formato y ejemplos

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

...



# El tablero de monitoreo marca la tarea en verde

La tarea al ser marcada en verde, esta confirma que estuvo en lo esperado por lo tanto, posiblemente este se ejecute en un bloque "global" de excepciones similar a:

```python
    try:
        chrono_task()

    except Exception as e:
        print(e) # e == 'OAuth session expired anc colud not be refreshed'
```


me esperaria ver algo como:
```python
    res: Response = httpx.post(URL_SERVE, json=Payload, auth=AUTH_TOKEN_SERVE_NAME)

    # o mejor dicho:
    res = httpx.post(...)
```

con ello, este solo confirmaria que retorne un status code sin verificar cual seria dejando pasar cualquier cosa y con ello haciendo algo como:

```python
    print(str(res.content))

```
antes del `try-except` o inclusive dentro de este


una mejora que personalmente haria seria algo como usar:
```python
    res.raise_for_status()
```

y con ello ahorraria problemas; eso suponiendo que es un script python, si es un script bash realmente no sabria que esperar en si



# ¿Qué está pasando y cómo averiguarías desde cuándo?

revisar logs buscando el print/log con algo como:
```python
    for log in logs:
        if 'Failed to authenticate' in log:
            print(log.datetime) # asumiendo que esten ordenados por fecha de el mas antiguo primero al mas nuevo como final
            return
```

o revisar usando utilidades unix (ya que es macos el sistema, con ello cercano a bsd) como:

`grep 'Failed to authenticate' /ruta/al/log | head -n 1`


si es sql usaria algo parecido a esto:
```sql
    SELECT * FROM logs
    WHERE msg lIKE '%Failed to authenticate%'
    ORDER BY date ASC
    LIMIT 1
    -- suponiendo que asi sea el esquema pero lo ajustaria para hacerlo mas preciso y rapido
```


# ¿Qué harías hoy para arreglarlo?

- podria hacer el proceso manualmente y corregir cosas puntuales del script original
- re-hacer el script desde cero siendo cuidadoso en escribirlo (si aplica)
- re-autenticar el script
- buscar con chatgpt/deepseek alguna solucion por si es problema del servidor, del entorno, de como se hace la peticion o algun area especifica para poder encontrar el error mas rapidamente



personalmente primero intentaria hacer una autenticacion y probar el script, en caso de no funcionar, revisar el script para arreglarlo y ver si es problema del codigo fuente, en caso de no serlo a lo mejor podria ser el propio servidor al haber un cambio; esto dependera; inclusive si se presta el script podria re-hacerlo desde cero para facilitar una implementacion mas precisa y con mejor calidad


# ¿Qué cambiarías para que una tarea que corre pero no hace nada nunca vuelva a aparecer en verde?

volveria a escribir el script desde cero; dado que es un script, este posiblemente no pase de 200 LoC lo cual es algo bastante barato de escribir tanto manualmente como por un modelo ML
tambien manejaria especificamente los casos que esperaria lanzando una excepcion ante algo extrano para facilitar los problemas en lugar de imprimir/loggear cualquier error arbitrariamente
