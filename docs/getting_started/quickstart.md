# Quickstart

## Installation
To install PromptGuard, run:

```bash
pip install promptguard
```

## Environment Setup
Accessing the PromptGuard API requires an API key, which you can get by creating an account [here](https://promptguard.opaque.co). Once you have an account, you can find your API key on the [API Keys page](https://promptguard.opaque.co/api-keys).

Once you have your key, set it as an environment variable:

```bash
export PROMPTGUARD_API_KEY="..."
```

## Using PromptGuard
PromptGuard offers two main functions: `sanitize()` and `desanitize()`. `sanitize()` takes a string and returns a sanitized (i.e. encrypted and redacted) version of it, while `desanitize()` takes a sanitized string and returns the original string.

```python
```