# Quickstart

## Installation
To install OpaquePrompts, run:

```bash
pip install opaqueprompts
```

## Environment Setup
Accessing the OpaquePrompts API requires an API key, which you can get by creating an account [on the OpaquePrompts website](https://opaqueprompts.opaque.co). Once you have an account, you can find your API key on the [API Keys page](https://opaqueprompts.opaque.co/#/main/api/key).

Once you have your key, set it as an environment variable:

```bash
export OPAQUEPROMPTS_API_KEY="..."
```

## Using OpaquePrompts standalone
OpaquePrompts offers two main functions: `sanitize()` and `desanitize()`. `sanitize()` takes a string and returns a sanitized (i.e. encrypted and redacted) version of it, while `desanitize()` takes a sanitized string and returns the original string.

### Sanitization

```python
import opaqueprompts

input_text_with_pii = "John Smith called 213-456-7098 (the phone number of his friend Sarah Jane) and asked her to meet him in San Francisco."
sanitized_response = opaqueprompts.sanitize(input_texts = [input_text_with_pii])
```
The `sanitized_response` contains both the `sanitized_texts` as well as `secure_context` which must be passed to the followup call to `desanitize()`. 

```python
> print(sanitized_response)
SanitizeResponse(sanitized_texts=['PERSON_2 called PHONE_NUMBER_1 (the phone number of his friend PERSON_1) and asked her to meet him in LOCATION_1.'], secure_context='eyJzZWNyZXRfZW50cm9weSI6IjRocWZxb1VBUmJueWNYeU5JRjROa3VzNjdkSnZtY1ZPVFhYcnlPWDdmNzAxNVR4NVUraTM5c3VGRTJqS3oySjUzMkM4ckF6L0cyME5sWGloZ2hicWhzcFF6N2pVTUZIVVNvMVRGam1UU2tTcG5pR1Bob0s5RUR3N3JQZ2VkMklJNEhRTHh2dVZNUnJlY2h3WVhGbGhZYzhFOEI1VFJkWVl2Sm1QUG5Rbkp3WT0iLCJlbnRpdHlfbWFwIjp7IkxPQ0FUSU9OXzEiOiJibFpDVE1oMTR0OW1FQmZsejk5cWVlWVJSTjdyUzhkUTZRRVZOZHlKNkEwPSIsIlBFUlNPTl8xIjoiZDZiR3VjOEJVNUdPcG56cDJoV1FaUUIyaUtvRzA2U3dCdGlkSXo5WGxaUT0iLCJQRVJTT05fMiI6IkpKSyt6cmhtTENzWGVkTHhoNWxhTWFFSzlUVmw1bU55MkNGR3FZekRmZ3M9IiwiUEhPTkVfTlVNQkVSXzEiOiJhQU9GVmhoT0tqczVzT0Iwczh2dnZwNTBsVk9XcnNyODE3eEVVSnkrTzdRPSJ9fQ==')
```
As you can see, the `sanitized_texts` field contains the initial message, but with the PII removed. The `secure_context` is just an opaque set of bytes
which should get passed to the desanitize call as shown below.

### Desanitization

```python
# Assume that sanitized_response.sanitized_text was passed into an LLM of your
# choice, and the final output is saved to 'llm_output" such that
# llm_output = "PERSON_1 and PERSON_2 will be meeting in LOCATION_1"
desanitized_response = opaqueprompts.desanitize(sanitized_text = llm_output, secure_context = sanitized_response.secure_context)
```

The `desanitized_response` contains only one field `desanitized_text` which contains the desanitized version of `llm_output`.
 
```python
> print(desanitized_response)
DesanitizeResponse(desanitized_text='Sarah Jane and John Smith will be meeting in San Francisco')
```

## Using OpaquePrompts with LangChain

OpaquePrompts offers a [LangChain](https://python.langchain.com/docs/get_started/introduction.html) integration, enabling you to easily build privacy-preserving LLM applications. See the [OpaquePrompts page in the LangChain documentation](https://python.langchain.com/docs/integrations/llms/opaqueprompts) for more.

## Troubleshooting

### Version Mismatch

OpaquePrompts is currently in beta and is constantly being improved. As such we might sometimes make breaking changes and drop support for old versions of the Python package. If this happens, you should see an error message like this when making a `sanitize` or `desanitize` call:

```
Request sent using package version 0.1.0, but minimum supported version is 0.2.0. Please update the opaqueprompts package to a supported version.
```

If you see this, simply upgrade `opaqueprompts` with `pip install -U opaqueprompts` and then you should be able to continue using the package without issue.

### Missing Version Header

The logic to gracefully handle version mismatch was not added to the opaqueprompts package until version 0.1.0. As such if you are using an older version of opaqueprompts you may see the following error:

```
Client-Version header not set, please ensure this request was sent using opaqueprompts version >= 0.1.0
```

If you see this then make sure to update your opaqueprompts package to the latest version per the instructions in the "Version Mismatch" section.
