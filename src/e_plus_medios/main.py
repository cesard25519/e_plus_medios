from datetime import datetime, timezone, timedelta
from typing import NamedTuple


from httpx import Client, Response, TimeoutException, RequestError


HEADERS: dict[str, str] = {"User-Agent": "WP-Checker/1.0"}
API_PATH: str = '/wp-json/wp/v2/posts?per_page=1' # os.environ['API_PATH'] # raises if not exists
TIMEOUT_SECS: int = 10
LIMIT_HOURS: int = 24


class VerifySiteError(Exception):
    def __init__(self, domain: str, reason: str) -> None:
        super().__init__( f'{ domain }\n   [ERROR]   ->   {reason}\n')


class VerifySite(NamedTuple):
    client: Client
    domain: str


    def __call__(self) -> None:
        response: Response = self.__must_response()
        self.__raise_if_invalid_status_code(res=response)
        payload_json: dict = self.__must_json(res=response)
        posts: list[dict] = self.__must_list(data=payload_json)
        date: datetime = self.__must_valid_datetime(json_items=posts)
        self.__must_antique(date=date)


    def __must_response(self) -> Response:
        domain: str = self.domain.rstrip('/') + API_PATH

        try:
            return self.client.get(url=domain, headers=HEADERS)

        except TimeoutException:
            raise VerifySiteError(domain=domain, reason='timeout')

        except RequestError as e:
            exc: str = e.__class__.__name__
            raise VerifySiteError(domain=domain, reason='conection error: ' + exc)


    def __raise_if_invalid_status_code(self, res: Response) -> None:
        if res.status_code != 200:
            raise VerifySiteError(domain=self.domain, reason=f'HTTP {res.status_code}')


    def __must_json(self, res: Response) -> dict:
        try:
            return res.json()

        except ValueError:
            raise VerifySiteError(domain=self.domain, reason='response with invalid json')


    def __must_list(self, data) -> list:
        if data and isinstance(data, list):
            return data

        raise VerifySiteError(domain=self.domain, reason='no posts published')


    def __must_valid_datetime(self, json_items: list[dict], fmt='%Y-%m-%dT%H:%M:%S') -> datetime:
        if date := json_items[0].get('date_gmt'):
            try:
                d: datetime = datetime.strptime(date, fmt)
                return d.replace(tzinfo=timezone.utc)

            except ValueError:
                raise VerifySiteError(domain=self.domain, reason='invalid date format: ' + date)

        raise VerifySiteError(domain=self.domain, reason='post not has date')


    def __must_antique(self, date: datetime) -> None:
        antique: timedelta = datetime.now(timezone.utc) - date

        if antique > timedelta(hours=LIMIT_HOURS):
            raise VerifySiteError(domain=self.domain, reason=f'last post has { int(antique.total_seconds()/3600) } hours')

