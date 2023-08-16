---
hide:
  - navigation
  - toc
---

# Introduction
PromptGuard is a service that enables applications to leverage the power of language models without compromising user privacy. Designed for composability and ease of integration into existing applications and services, PromptGuard is consummable via a simple Python library as well as a [LangChain](https://python.langchain.com/docs/get_started/introduction.html) integration. Perhaps more importantly, PromptGuard leverages the power of [confidential computing](https://en.wikipedia.org/wiki/Confidential_computing) to ensure that even the PromptGuard service itself cannot access the data it is protecting.

Today's LLM application architectures often yield constructed prompts that may include retrieved context, conversation memory, and/or a user query, all of which may contain sensitive information. PromptGuard enables applications to protect this sensitive information by sanitizing prompts before they're sent to a language model. PromptGuard can then "de-sanitize" the model's response, ensuring that the application receives the same response it would have received had the prompt not been sanitized. You can think of PromptGuard as a privacy layer that wraps a language model, transparently sanitizing and de-sanitizing prompts and responses.

<div class="grid cards" markdown>

*   :material-rocket-launch: **Get Started**

    ---

    New to PromptGuard? Quickly get started here.
    
    [Learn more :octicons-arrow-right-24:](getting_started/quickstart.md){: .right}

*   :material-tools: **Technical Overview**

    ---

    Gain a better understanding of how PromptGuard protects sensitive data without seeing it.

    [Learn more :octicons-arrow-right-24:](getting_started/overview.md){: .right}

*   :material-account: **API Reference**

    ---

    See the API reference for the PromptGuard Python library.

    [Learn more :octicons-arrow-right-24:](reference/library_api.md){: .right}

</div>

## Get help
Can't find what you're looking for? Contact us at [promptguard@opaque.co](mailto:promptguard@opaque.co).
