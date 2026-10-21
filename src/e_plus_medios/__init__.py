from sys import argv as terminal_args


import httpx


from .main import VerifySite, TIMEOUT_SECS, VerifySiteError


DOMAINS_TEST: list[str] = [ # pruebas
    "https://wordpress.org/news",
    "https://ma.tt",
]


def main() -> None:
    domains: list[str] = terminal_args[1:] or DOMAINS_TEST
    fails: list[str] = []

    with httpx.Client(timeout=TIMEOUT_SECS, follow_redirects=True) as client:
        print(f'verificando { len(domains) } dominios: ...')

        for dom in domains:
            try:
                VerifySite(client=client, domain=dom)
                print(f'   [OK]   { dom }')

            except VerifySiteError as exc:
                fails.append(str(exc))


    print('\n' + '-' * 60)
    print(f'RESUMEN: { len(domains) - len(fails) } OK / { len(fails) } has fails')
    print('-' * 60)

    if fails:
        print('\nSites with fails')
        for f in fails:
            print(f'   - {f}')

        exit(1)

    print('\nTodos los sitios responden y publicaron en las ultimas 24 horas')


if __name__ == '__main__':
    main()
