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

input_text = "Some string with sensitive PII"
sanitized_response = pg.sanitize(text = input_text)
```
The `sanitized_response` contains both the `sanitized_text` as well as `secure_context` which must be passed to the followup call to `desanitize()`. 

```python
# Assume that sanitized_response.sanitized_text was passed into an LLM of your
# choice, and the final output is saved to 'llm_output"
desanitized_response = pg.desanitize(sanitized_text = llm_output, secure_context = sanitized_response.secure_context)

print(desanitized_response.desanitized_text)
```

## Using PromptGuard with LangChain

TODO: add link to LangChain docs

PromptGuard offers a [LangChain](https://python.langchain.com/docs/get_started/introduction.html) integration, enabling you to easily build privacy-preserving LLM applications.