# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Python SDK (`sendbee-api` on PyPI, packaged via PEP 621 `pyproject.toml` with the `setuptools` build backend) for the AI Number / Sendbee public API. Server-side counterpart lives at `/Users/ivanarar/work/sendbee/sendbee-backend/sendbee_app/public_api_v2/` — when extending this client, mirror endpoints declared in that backend's `urls.py`. The default base URL is `https://api-v2.sendbee.io` (overridable by setting `SendbeeApi.base_url` / `SendbeeApi.protocol` before constructing the client — see `tests/example.py` for how staging/local/dev hosts are swapped in).

## Commands

```bash
pip install -e ".[dev]"           # install package + dev deps (pytest, responses)
pytest                            # run tests (tests/test_api.py is a stub; tests/example.py is a manual REPL-style scratchpad, not a pytest suite)
python -m build                   # produce sdist + wheel into dist/
```

There is no lint config and no formatter config. CI is GitHub Actions: `.github/workflows/ci.yml` runs `pytest` across Python 3.7–3.13 on push/PR to `master`; `.github/workflows/publish.yml` publishes to PyPI via OIDC Trusted Publishing when a GitHub Release is published. To release: bump `version` in `pyproject.toml`, merge, then cut a GitHub Release tagged `v<version>`.

`tests/example.py` is the de-facto manual integration harness — each block is gated by `if True/False:` and hits the real API with hard-coded credentials for staging/legacy-prod numbers. Flip the flags to exercise a flow; never commit `if True:` for blocks with secrets.

## Architecture

The whole client is one pattern repeated per resource. Internalize this and the rest of the code reads itself.

### The `bind_request` factory (`sendbee_api/bind.py`)

Every API method on the client is produced by `bind_request(api_path=..., model=..., method=..., query_parameters=..., ...)`. It returns a closure that, when called as an instance method, builds a `Request`, fires it, and returns either a `Response` (list endpoints) or a single model (POST/PUT/DELETE, or `force_single_model_response=True`).

Key behavior baked into the factory:
- `single_model_response` is auto-true for POST/PUT/DELETE.
- GET requests serialize query params into the URL; list values become comma-joined, dict values become `k:v,k:v`; booleans are coerced to `'1'`/`'0'` (see `constants.BoolConst`).
- POST/PUT/DELETE send `self.parameters['query']` as the JSON body — same dict, different transport.
- `default_parameters` are merged in first, then call-site kwargs override (used e.g. for `subscribe_contact` defaulting `block_automation`/`block_notifications` to `True`).
- A `timeout` kwarg on any call is extracted and applied to `requests` (default 20s); it never reaches the wire.
- If `client.fake_response_path` is set, the request is short-circuited and the file is read as the response body — this is the only built-in test seam.

### Resource clients are mixins composed onto `Client`

`Client` (= `SendbeeApi`) in `sendbee_api/client.py` inherits from `Contacts, Messages, Automation, Teams, RateLimit`. Each mixin lives under `sendbee_api/<resource>/client.py` and is just a class body of `name = bind_request(...)` assignments. To add a new endpoint:

1. Add the URL to the backend `public_api_v2/urls.py` and implement the view.
2. Add a `QueryParams` subclass in `sendbee_api/<resource>/query_params.py` enumerating accepted kwargs (`name = ('wire_name', 'description')` — `aenum.MultiValueEnum`, see below).
3. Add a `Model` subclass in `sendbee_api/<resource>/models.py` declaring response fields.
4. Add a `name = bind_request(api_path=..., model=..., query_parameters=..., method=...)` line to the resource's `client.py`.
5. If `Client` doesn't already inherit the mixin, add it to the MRO in `client.py`.

### Query parameters use `aenum.MultiValueEnum`

`QueryParams` (`sendbee_api/query_params.py`) subclasses are not plain enums — each member is `name = ('wire_name', 'human description')`. `bind_request` accepts a kwarg if it matches *either* the python attr name *or* the wire name. The description is used by `Client.print_params_for(fn_name)` to introspect a call's params from the REPL.

### Models declare fields with a leading underscore; client reads without it

The `Model` base in `sendbee_api/models.py` does some metaclass-flavored gymnastics: declaring `_name = TextField(index='name')` on the class causes the instance to expose `model.name` after `process()`. The leading underscore on the class attribute and the corresponding non-underscored instance attribute is the convention — keep it. Fields convert raw JSON values into typed Python via `Field._convert_field_item` (see `sendbee_api/fields.py` for `Text`, `Number`, `RealNumber`, `Boolean`, `Datetime`, `List`, and `ModelField` for nested models).

`ModelField` is how nested objects/arrays are mapped — e.g. `Contact._tags = ModelField(ContactTag, index='tags')` causes `contact.tags` to be a list of `ContactTag` model instances built by recursing into `process()`.

### Response, pagination, errors

`Response` (`sendbee_api/response.py`) wraps the raw body and lazily exposes `.models`, `.meta`, `.headers`, `.raw_data`, `.formatted_data`, `.warning`. Iterating a `Response` iterates `.models`. The server is expected to return `{"data": [...], "meta": {...}, "warning": "..."}`; the `Json` formatter (`sendbee_api/formatter.py`) unwraps `data` for models and `meta` for pagination.

Pagination: `response.has_next()` and `response.next_page()` drive manual loops; alternatively, requesting a page past the end raises `PaginationException` (raised inside `_process_response` when `current_page > 1` and `models` is empty). Both styles are documented in the README and are equally supported.

Errors: any HTTP ≥ 400 (unless the endpoint sets `ignore_error=True`) raises `SendbeeRequestApiException` with `.response` attached so callers can inspect headers (e.g. `Retry-After` on 429s). Non-fatal `warning` strings from the server are printed to stdout in yellow via `click.secho` — do not raise on them.

### Auth

`SendbeeAuth` (`sendbee_api/auth.py`) generates an HMAC-SHA256 token over the current UTC unix timestamp keyed by `api_secret`, base64-encoded as `"<ts>.<hex>"`. Every request carries `X-Api-Key` (the public key) and `X-Auth-Token` (this HMAC). `api.auth.check_auth_token(token)` is the same primitive in reverse and is what consumers should use to authenticate inbound webhooks from Sendbee — see the "Authenticate webhook request" section in README.md.

## Conventions worth knowing

- `force_single_model_response=True` is the way to make a GET return one model instead of a list (e.g. `get_conversation`, `chatbot_activity_status`).
- `ServerMessage` (in `sendbee_api/models.py`) is the canonical "the server just sent back `{message: ...}`" model — use it for DELETE endpoints and other ack-only responses.
- The `endpoints/` subpackage referenced from the backend is misspelled `convresations.py` (sic). The client's `conversations` package is spelled correctly; do not "fix" the backend filename casually, the URL imports depend on it.
- Debug mode (`SendbeeApi(..., debug=True)`) prints request/response/cURL via the `Debug` context manager (`sendbee_api/debug.py`) — invaluable when reproducing a server-side bug; pair with `tests/example.py`.
- The package depends on `ujson==2.0.1` (pinned), `aenum`, `click`, `requests`, `cryptography`, `dumpit`, and `curlify` — all declared in `pyproject.toml`'s `[project] dependencies`.
