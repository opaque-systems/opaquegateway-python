# Overview

## Technical overview

A technical overview on how Opaque Gateway build on top of [confidential computing](https://en.wikipedia.org/wiki/Confidential_computing) and [remote attestation](https://www.redhat.com/en/blog/attestation-confidential-computing) is coming soon.

### Attested communication with Opaque Gateway

All communication from a client to Opaque Gateway occurs over an attested TLS channel. In short, an attested TLS channel enables a client to 1) verify the identity of the server, 2) ensure that the server is running the correct software, and 3) establish an encrypted channel for communication. Attested TLS capabilities rely on the server running on confidential computing hardware. More on confidential computing, remote attestation, and attested TLS can be found [here](background.md).

## Supported entities

Opaque Gateway, for now, supports only the English language. The service identifies and sanitizes the following entity types:

| **Type**                                                                                                                        | **Notes**                           |
|---------------------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| Bank account numbers                                                                                                            |                                     |
| Credit card                                                                                                                     |                                     |
| Crypto wallet numbers                                                                                                           | Supports BTC wallets                |
| Dates                                                                                                                           |                                     |
| Driver's license numbers                                                                                                        | Supports US drivers' licenses       |
| Email addresses                                                                                                                 |                                     |
| Geographic locations                                                                                                            |                                     |
| [Individual Taxpayer Identification Numbers (ITINs)](https://www.irs.gov/individuals/individual-taxpayer-identification-number) |                                     |
| [International Bank Account Numbers (IBANs)](https://n26.com/en-eu/iban-number)                                            |                                     |
| IP addresses                                                                                                                    | Supports both IPv4 and IPv6         |
| Medical license numbers                                                                                                         |                                     |
| Names                                                                                                                           |                                     |
| Passport numbers                                                                                                                | Supports US passports               |
| Phone numbers                                                                                                                   |                                     |
| Social security numbers (SSNs)                                                                                                  | Supports US SSNs                    |
| URLs                                                                                                                            |                                     |

For custom entity types, contact us at `hello@opaque.co`.