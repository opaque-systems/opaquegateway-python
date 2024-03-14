---
hide:
  - navigation
  - toc
---

# Introduction
Opaque Gateway is a service that enables applications to leverage the power of language models without compromising user privacy. Designed for composability and ease of integration into existing applications and services, Opaque Gateway is consumable via [a simple Python library](getting_started/quickstart.md#installation) as well as through [LangChain](https://python.langchain.com/docs/integrations/llms/opaqueprompts). Perhaps more importantly, Opaque Gateway leverages the power of [confidential computing](https://en.wikipedia.org/wiki/Confidential_computing) to ensure that even the Opaque Gateway service itself cannot access the data it is protecting.

Today's LLM application architectures often yield constructed prompts that may include retrieved context, conversation memory, and/or a user query, all of which may contain sensitive information. Opaque Gateway enables applications to protect this sensitive information by sanitizing prompts before they're sent to a language model. Opaque Gateway can then "de-sanitize" the model's response, ensuring that the application receives the same response it would have received had the prompt not been sanitized. You can think of Opaque Gateway as a privacy layer that wraps a language model, transparently sanitizing and de-sanitizing prompts and responses.

<div class="grid cards" markdown>

*   :material-rocket-launch: **Get Started**

    ---

    New to Opaque Gateway? Quickly get started here.
    
    [Learn more :octicons-arrow-right-24:](getting_started/quickstart.md){: .right}

*   :material-tools: **Technical Overview**

    ---

    Gain a better understanding of how Opaque Gateway protects sensitive data without seeing it.

    [Learn more :octicons-arrow-right-24:](getting_started/overview.md){: .right}

*   :material-code-tags: **API Reference**

    ---

    See the API reference for the Opaque Gateway Python library.

    [Learn more :octicons-arrow-right-24:](reference/library_api.md){: .right}

</div>

## Get help
Can't find what you're looking for? Contact us at [opaquegateway@opaque.co](mailto:opaquegateway@opaque.co).
