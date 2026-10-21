from datetime import datetime, timezone, timedelta

from httpx import Client, Response, TimeoutException, RequestError

HEADERS: dict[str, str] = {"User-Agent": "WP-Checker/1.0"}
API_PATH: str = '/wp-json/wp/v2/posts?per_page=1' # os.environ['API_PATH'] # raises if not exists
TIMEOUT_SECS: int = 10
LIMIT_HOURS: int = 24
DATE_FMT: str = '%Y-%m-%dT%H:%M:%S'


class VerifySiteError(Exception):
    def __init__(self, domain: str, reason: str) -> None:
        super().__init__( f'{ domain }\n   [ERROR]   ->   {reason}\n')


def verify_site(client: Client, domain: str) -> None:
    domain: str = domain.rstrip('/') + API_PATH

    try:
        cli: Response = client.get(url=domain, headers=HEADERS)

    except TimeoutException:
        raise VerifySiteError(domain=domain, reason='timeout')

    except RequestError as e:
        exc: str = e.__class__.__name__
        raise VerifySiteError(domain=domain, reason='conection error: ' + exc)


    if cli.status_code != 200:
        raise VerifySiteError(domain=domain, reason=f'HTTP {cli.status_code}')

    try:
        data = cli.json()

    except ValueError:
        raise VerifySiteError(domain=domain, reason='response with invalid json')


    if not data or not isinstance(data, list):
        raise VerifySiteError(domain=domain, reason='no posts published')

    json_items: list = data

    if not ( date := json_items[0].get('date_gmt') ):
        raise VerifySiteError(domain=domain, reason='post not has date')

    try:
        date_gmt: datetime = datetime.strptime(date, DATE_FMT).replace(tzinfo=timezone.utc)

    except ValueError:
        raise VerifySiteError(domain=domain, reason='invalid date format: ' + date)

    antique: timedelta = datetime.now(timezone.utc) - date_gmt

    if antique > timedelta(hours=LIMIT_HOURS):
        raise VerifySiteError(domain=domain, reason=f'last post has { int(antique.total_seconds()/3600) } hours')


