# Quickstart

## Installation
To install PromptGuard, run:

```bash
pip install promptguard
```

## Environment Setup
Accessing the PromptGuard API requires an API key, which you can get by creating an account [on the PromptGuard website](https://promptguard.opaque.co). Once you have an account, you can find your API key on the [API Keys page](https://promptguard.opaque.co/api-keys).

Once you have your key, set it as an environment variable:

```bash
export PROMPTGUARD_API_KEY="..."
```

## Using PromptGuard standalone
PromptGuard offers two main functions: `sanitize()` and `desanitize()`. `sanitize()` takes a string and returns a sanitized (i.e. encrypted and redacted) version of it, while `desanitize()` takes a sanitized string and returns the original string.

```python
import promptguard as pg

input_text_with_pii = "John Smith called 213-456-7098 (the phone number of his friend Sarah Jane) and asked her to meet him in San Francisco."
sanitized_response = pg.sanitize(text = input_text_with_pii)
```
The `sanitized_response` contains both the `sanitized_text` as well as `secure_context` which must be passed to the followup call to `desanitize()`. 

```python
> print(sanitized_response)
SanitizeResponse(sanitized_text='PERSON_2 called PHONE_NUMBER_1 (the phone number of his friend PERSON_1) and asked her to meet him in LOCATION_1.', secure_context='eyJzZWNyZXRfZW50cm9weSI6IjRocWZxb1VBUmJueWNYeU5JRjROa3VzNjdkSnZtY1ZPVFhYcnlPWDdmNzAxNVR4NVUraTM5c3VGRTJqS3oySjUzMkM4ckF6L0cyME5sWGloZ2hicWhzcFF6N2pVTUZIVVNvMVRGam1UU2tTcG5pR1Bob0s5RUR3N3JQZ2VkMklJNEhRTHh2dVZNUnJlY2h3WVhGbGhZYzhFOEI1VFJkWVl2Sm1QUG5Rbkp3WT0iLCJlbnRpdHlfbWFwIjp7IkxPQ0FUSU9OXzEiOiJibFpDVE1oMTR0OW1FQmZsejk5cWVlWVJSTjdyUzhkUTZRRVZOZHlKNkEwPSIsIlBFUlNPTl8xIjoiZDZiR3VjOEJVNUdPcG56cDJoV1FaUUIyaUtvRzA2U3dCdGlkSXo5WGxaUT0iLCJQRVJTT05fMiI6IkpKSyt6cmhtTENzWGVkTHhoNWxhTWFFSzlUVmw1bU55MkNGR3FZekRmZ3M9IiwiUEhPTkVfTlVNQkVSXzEiOiJhQU9GVmhoT0tqczVzT0Iwczh2dnZwNTBsVk9XcnNyODE3eEVVSnkrTzdRPSJ9fQ==')
```
As you can see, the `sanitized_text` field contains the initial message, but with the PII removed. The `secure_context` is just an opaque set of bytes
which should get passed to the desanitize call as shown below.

```python
# Assume that sanitized_response.sanitized_text was passed into an LLM of your
# choice, and the final output is saved to 'llm_output" such that
# llm_output = "PERSON_1 and PERSON_2 will be meeting in LOCATION_1"
desanitized_response = pg.desanitize(sanitized_text = llm_output, secure_context = sanitized_response.secure_context)
```

The `desanitized_response` contains only one field `desanitized_text` which contains the desanitized version of `llm_output`.
 
```python
> print(desanitized_response)
DesanitizeResponse(desanitized_text='Sarah Jane and John Smith will be meeting in San Francisco')
```

## Using PromptGuard with LangChain

TODO: add link to LangChain docs

PromptGuard offers a [LangChain](https://python.langchain.com/docs/get_started/introduction.html) integration, enabling you to easily build privacy-preserving LLM applications.