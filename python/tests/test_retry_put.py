import json

import pytest
import responses

from cacheai import Client


@responses.activate
def test_put_is_retried_on_503_then_succeeds():
    """
    This test proves retries for PUT work by simulating:
      1) 503 Service Unavailable
      2) 200 OK
    and asserting two PUT calls were made.

    NOTE: This will FAIL until you add "PUT" to Retry.allowed_methods in client.py.
    """
    base_url = "https://api.cacheai.tech/v1"
    cache_key = "abc123"
    url = f"{base_url}/cache/{cache_key}"

    # 1st response: transient failure => should trigger retry
    responses.add(
        method=responses.PUT,
        url=url,
        status=503,
        json={"error": {"message": "temporary outage"}},
        content_type="application/json",
    )

    # 2nd response: success
    responses.add(
        method=responses.PUT,
        url=url,
        status=200,
        json={"cache_key": cache_key, "updated_fields": ["output"]},
        content_type="application/json",
    )

    client = Client(api_key="test-key", base_url=base_url, max_retries=1)

    result = client.cache.update(cache_key, output="hello")

    assert result["cache_key"] == cache_key
    assert len(responses.calls) == 2
    assert responses.calls[0].request.method == "PUT"
    assert responses.calls[1].request.method == "PUT"

    body = json.loads(responses.calls[1].request.body.decode("utf-8"))
    assert body["output"] == "hello"
