# Resolver SDK Python Guide

`resolver-sdk` is a Python client for communicating with the Resolver by Kroll API. It supplies API-key authentication, retry handling, resource helpers, selected typed models, in-memory list caching, and job polling.

This guide is for developers starting from scratch. Replace values in angle brackets with values from your Resolver environment. Do not commit API keys.

## Requirements

- Python 3.11 or later
- A Resolver API base URL and an API key with suitable permissions

## Install with pip

Install from this checkout:

```bash
python -m pip install .
```

For editable development work:

```bash
python -m pip install -e .
```

Verify the installation:

```bash
python -c "from resolver_sdk import ResolverClient; print('Resolver SDK is ready')"
```

## Configure credentials

Store credentials in environment variables rather than source code:

```bash
# macOS or Linux
export RESOLVER_BASE_URL="<https://your-resolver-environment.example>"
export RESOLVER_API_KEY="<your-api-key>"

# PowerShell
$env:RESOLVER_BASE_URL = "<https://your-resolver-environment.example>"
$env:RESOLVER_API_KEY = "<your-api-key>"
```

The SDK sends the key in the `x-api-key` header. A trailing slash on the base URL is removed automatically.

## First request

Start with a read-only list call:

```python
import os
from resolver_sdk import ResolverClient

client = ResolverClient(
    base_url=os.environ["RESOLVER_BASE_URL"],
    api_key=os.environ["RESOLVER_API_KEY"],
)

forms = client.forms.get_all_forms()
print(f"Found {len(forms)} forms")
print(f"HTTP calls made: {client.get_api_calls()}")
```

Success confirms the URL, API key, network path, and permissions for this endpoint.

## Resource helpers

| Resource | Useful starting methods |
| --- | --- |
| `client.forms` | `get_all_forms`, `get_linked_forms`, `get_form_reports`, `get_form_formula`, `get_form_roles` |
| `client.applications` | `get_all_applications`, `get_activities`, `get_actions`, `get_views` |
| `client.reports` | `get_all_reports`, `get_report_components` |
| `client.objects` | `get_all_objects`, `get_object`, `check_object_exists`, `object_count`, `add_object`, `update_object`, `delete_object` |
| `client.roles` | `get_all_roles`, `get_role`, `get_users_and_groups_in_role` |
| `client.lifecycle` | `get_all_lifecycles`, `get_states_and_transitions`, `get_trigger_transitions` |
| `client.formulas` | `recalculate_for_all_objs`, `delete_formula` |
| `client.user_groups` | `get_users_in_group` |
| `client.utility` | `get_job_details`, `wait_for_job` |

Identifiers, payload fields, and permissions depend on your Resolver environment. Confirm them before performing writes.

## Common examples

List applications and activities. Verify `id` in your own API response before relying on it:

```python
applications = client.applications.get_all_applications()
for application in applications:
    application_id = application["id"]
    activities = client.applications.get_activities(application_id)
    print(application_id, len(activities))
```

Read an object with metadata:

```python
object_detail = client.objects.get_object(
    obj_id=<OBJECT_ID>,
    include_field_metadata=True,
    include_formula_metadata=True,
)
print(object_detail)
```

Create an object. This payload is illustrative only:

```python
payload = {
    "objectTypeId": <OBJECT_TYPE_ID>,
    "fields": [{"fieldId": <FIELD_ID>, "value": "<VALUE>"}],
}
created = client.objects.add_object(payload)
print(created)
```

Use raw request helpers only when there is no resource helper:

```python
response = client.safe_get("<API_PATH>", params={"<QUERY_NAME>": "<VALUE>"})
```

`safe_post`, `safe_put`, and `safe_delete` work similarly. Endpoint paths should begin with `/`.

## Caching and jobs

The forms, applications, reports, lifecycles, and roles list methods cache their results on the client. Request current data with `refresh=True`:

```python
forms = client.forms.get_all_forms()
fresh_forms = client.forms.get_all_forms(refresh=True)
```

Some operations return Resolver job IDs. Wait for a job directly when needed:

```python
job = client.utility.wait_for_job(job_id=<JOB_ID>, poll_interval=2, timeout=300)
print(job)
```

Polling backs off gradually, to a maximum 30-second interval. A `TimeoutError` is raised after the specified timeout.

## Errors and retries

By default, requests time out after 30 seconds. The transport retries connection failures, timeouts, and 5xx errors up to three attempts; it does not retry 4xx errors.

```python
from resolver_sdk.exceptions import (
    ResolverUnauthorizedError,
    ResolverRateLimitError,
    ResolverServerError,
    ResolverTransportError,
)

try:
    count = client.objects.object_count(obj_type_id=<OBJECT_TYPE_ID>)
except ResolverUnauthorizedError:
    print("Check the API key and its permissions.")
except ResolverRateLimitError:
    print("Slow down and retry later.")
except ResolverServerError:
    print("Resolver returned a server error after retries.")
except ResolverTransportError:
    print("The network request could not be completed.")
```

Customize defaults with a transport:

```python
from resolver_sdk import ResolverClient
from resolver_sdk.transport import ResolverTransport

transport = ResolverTransport(
    "<https://your-resolver-environment.example>", "<your-api-key>",
    timeout=60, retries=5, backoff=1,
)
client = ResolverClient("<unused>", "<unused>", transport=transport)
```

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `ResolverUnauthorizedError` | API key, target environment, and key permissions. |
| `ResolverForbiddenError` | The key is valid but lacks access to this resource or action. |
| `ResolverNotFoundError` | Base URL, endpoint path, and resource ID. |
| Model validation error | Compare the Resolver response with the expected typed model. |
| Repeated server/network errors | Resolver availability, proxy/firewall settings, then timeout/retry settings. |
| Stale list results | Call the list method with `refresh=True`. |

## Safe usage checklist

- Start in non-production where possible.
- Never log, commit, or share an API key.
- Begin with read-only calls.
- Validate Resolver-specific IDs and payload fields before writing.
- Treat `delete_*` methods as destructive.
- Use `client.get_api_calls()` to observe request volume.

## Next steps

Browse `src/resolver_sdk/resources` for implemented helpers and `src/resolver_sdk/schemas` for typed models. Build a small read-only script, validate real response shapes, then introduce write operations deliberately.
