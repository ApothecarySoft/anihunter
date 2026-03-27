import time
from gql import gql, Client
from gql.transport.httpx import HTTPXTransport
from gql.transport.exceptions import TransportQueryError, TransportServerError
import queries
from cachefiles import saveUserDataFile


_transport = HTTPXTransport(url="https://graphql.anilist.co", timeout=120)
_client = Client(transport=_transport, fetch_schema_from_transport=False)


def _fetchDataForPage(page: int, tag: str):
    print(f"fetching for page #{page}")
    query = gql(queries.mainQuery)
    result = None
    MAX_RETRIES = 3
    retries = 0
    while result == None and retries <= MAX_RETRIES:
        try:
            result = _client.execute(
                query,
                variable_values={
                    "tag": tag,
                    "sort": "ID",
                    "status": "NOT_YET_RELEASED",
                    "page": page,
                },
            )
        except TransportQueryError as e:
            errorCode = e.errors[0]["status"]
            if errorCode == 429:
                print(
                    f"got http {errorCode}, server is rate limiting us. waiting to continue fetching data"
                )
                countdownTimer_s(65)
            else:
                print(f"unhandled http error {errorCode}. trying again in 10 seconds")
                countdownTimer_s(10)
        except TransportServerError as e:
            print(e)
            countdownTimer_s(10)
        finally:
            retries += 1
    page = result["Page"]
    return page["media"], page["pageInfo"]["hasNextPage"]


def countdownTimer_s(seconds: int, silent: bool = False):
    while seconds > 0:
        if not silent:
            print(seconds)
        time.sleep(1)
        seconds -= 1


def fetchDataForTag(tag: str):
    print(f"fetching data for tag {tag}")
    pageNum = 0
    hasNextPage = True
    entries = []

    while hasNextPage:
        pageNum += 1
        newEntries, hasNextPage = _fetchDataForPage(page=pageNum, tag=tag)
        entries += newEntries
    entries = {str(x["id"]): x for x in entries}
    saveUserDataFile(tag=tag, entries=entries)

    return entries
