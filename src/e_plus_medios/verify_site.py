from datetime import datetime, timezone, timedelta

from httpx import Client, Response, TimeoutException, RequestError

HEADERS: dict[str, str] = {"User-Agent": "WP-Checker/1.0"}
API_PATH: str = '/wp-json/wp/v2/posts?per_page=1' # os.environ['API_PATH'] # raises if not exists
TIMEOUT_SECS: int = 10
LIMIT_HOURS: int = 24


class VerifySiteError(Exception):
    def __init__(self, domain: str, reason: str) -> None:
        super().__init__( f'{ domain }\n   [ERROR]   ->   {reason}\n')


def verify_site(client: Client, domain: str) -> None:
    response: Response = __must_response(client=client, url=domain)
    __raise_if_invalid_status_code(res=response, domain=domain)
    payload_json: dict = __must_json(res=response, domain=domain)
    posts: list[dict] = __must_list(data=payload_json, domain=domain)
    date: datetime = __must_valid_datetime(json_items=posts, domain=domain)
    __must_antique(date=date, domain=domain)


def __must_response(url: str, client: Client) -> Response:
    domain: str = url.rstrip('/') + API_PATH

    try:
        return client.get(url=domain, headers=HEADERS)

    except TimeoutException:
        raise VerifySiteError(domain=domain, reason='timeout')

    except RequestError as e:
        exc: str = e.__class__.__name__
        raise VerifySiteError(domain=domain, reason='conection error: ' + exc)


def __raise_if_invalid_status_code(domain: str, res: Response) -> None:
    if res.status_code != 200:
        raise VerifySiteError(domain=domain, reason=f'HTTP {res.status_code}')


def __must_json(domain: str, res: Response) -> dict:
    try:
        return res.json()

    except ValueError:
        raise VerifySiteError(domain=domain, reason='response with invalid json')


def __must_list(domain: str, data) -> list:
    if data and isinstance(data, list):
        return data

    raise VerifySiteError(domain=domain, reason='no posts published')


def __must_valid_datetime(domain: str, json_items: list[dict], fmt='%Y-%m-%dT%H:%M:%S') -> datetime:
    if date := json_items[0].get('date_gmt'):
        try:
            return datetime.strptime(date, fmt).replace(tzinfo=timezone.utc)

        except ValueError:
            raise VerifySiteError(domain=domain, reason='invalid date format: ' + date)

    raise VerifySiteError(domain=domain, reason='post not has date')


def __must_antique(domain: str, date: datetime) -> None:
    antique: timedelta = datetime.now(timezone.utc) - date

    if antique > timedelta(hours=LIMIT_HOURS):
        raise VerifySiteError(domain=domain, reason=f'last post has { int(antique.total_seconds()/3600) } hours')


