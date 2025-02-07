# Confidential computing background
Computer security has traditionally been predicated on two tenets: the protection of data at rest and the protection of data in transit. The former is addressed by technologies such as full-disk encryption (FDE) the likes of [BitLocker](https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/), [FileVault](https://support.apple.com/guide/mac-help/protect-data-on-your-mac-with-filevault-mh11785/mac), and [LUKS](https://en.wikipedia.org/wiki/Linux_Unified_Key_Setup), while the latter is typically addressed by Transport Layer Security (TLS). These technologies have become ubiquitous in the last several decades and have greatly contributed to securing computer systems. They are, however, insufficient to fully ensure that only authorized parties have access to user data.

While data is being processed, it is stored in memory in the clear and it is transformed by the processor in full view of the system’s hardware, firmware, and operating system. This comprises tens of millions of lines of code written by a wide variety of vendors, some trustworthy and some less so. In addition, despite the best efforts of their developers, bugs and vulnerabilities are bound to creep into such large codebases, thereby rendering them susceptible to malware. This malware may in turn silently exfiltrate data or tamper with its processing to produce incorrect results.

Furthermore, system administrators have access, both remote and direct, to systems that handle confidential data. As a result, they can access or tamper with this data, either of their own volition, or by virtue of being compelled to do so by local authorities. Similarly, the service provider itself may misbehave or similarly be required to interfere.
To mitigate against these threats, a new tenet of computer security is needed: the protection of data during use.

## Confidential Computing
The term trusted computing base (TCB) refers to all the code and, by extension, all the entities that wrote that code, that are directly or transitively trusted by any given workload. In addition, the TCB of a workload encompasses all hardware that can peek into or alter that workload, such as devices with direct memory access (DMA) capability, as well as any person or organization that manages the infrastructure on which the workload runs and which could, if it so desired, gain access to or tamper with the workload, be it via remote administrative privileges or through direct physical access.

Therefore, any avenue of access through its TCB can potentially render a workload insecure. This includes malware, system administrators, and government entities whose jurisdiction the servers on which the workload executes find themselves in. As a result, for any workload that is deemed sensitive, it is desirable to render its TCB as small as it practically can be. Trusted execution environments (TEEs) provide a way to minimize and enforce a workload’s TCB.

TEEs provide a guarantee of confidentiality and integrity to both code and data. For a workload running inside a TEE, this means that no entity outside of the workload’s TCB may read from or write to its memory or otherwise tamper with its execution. In addition, TEEs provide a mechanism via which their trustworthiness and that of the workload running within them may be appraised. This mechanism is known as remote attestation and it allows a remote party to establish trust in a TEE as well as in the workload within it, and subsequently share secrets and other sensitive information with it.

In and out of themselves, TEEs are an abstract notion, and there exist multiple and wildly different implementations of them. Each implementation may be deemed a TEE irrespective of its internal architectural details if it conforms to the definition of a TEE. Some implementations include a larger TCB by design while others only carry the most minimal viable TCB.

The [Confidential Computing Consortium (CCC)](https://confidentialcomputing.io/) defines confidential computing as “the protection of data in use by performing computation in a hardware-based, attested Trusted Execution Environment” . The manner of execution of Opaque Gateway abides by this definition by leveraging AMD’s TEE implementation: AMD SEV-SNP.

## Remote Attestation
This section introduces nomenclature pertaining to remote attestation procedures. This nomenclature is useful in providing a shared language for the remainder of this document.

Trust is a choice an entity makes about another system, and trustworthiness is a quality about that system that can be used in deciding whether to trust it. Remote attestation is a process whereby an entity appraises the trustworthiness of a system and determines whether to trust it.

The system whose trustworthiness is appraised is known as the attester, the entity performing the appraisal is known as the verifier, and the entity that determines whether to trust the attester is known as the relying party.

The attester produces evidence containing a set of claims. Each claim is typically a key-value pair that describes some aspect of the attester that might be of interest to the verifier. Additionally, the evidence may be accompanied by a set of endorsements. An endorsement is a secure statement produced by an endorser that vouches for the integrity of the attester’s ability to collect claims and sign evidence. An endorser is typically a hardware manufacturer or software vendor whose endorsements help verifiers appraise the authenticity of some of the claims embedded in the evidence produced by the attester. The attester may provide its endorsements alongside the evidence or the verifier may obtain them on its own.

The verifier compares the values of the claims contained in the evidence against a set of reference values usually provided by a hardware manufacturer or software vendor. Reference values are typically referred to as good-known or nominal values in other documents. The verifier performs this comparison in addition to the appraisal of any endorsements according to an attestation policy. The attestation policy for evidence appraisal set by the verifier owner determines which claims and which endorsements the verifier appraises and how. As a result of this process, the verifier produces an attestation result that vouches for the attester.

The relying party obtains the attestation result from the verifier and applies to it a set of rules set by the relying party owner known as the appraisal policy for attestation results. This policy determines whether the attestation result satisfies the relying party and thus whether it is convinced that the attester is trustworthy.

Once the relying party establishes that the attester can be trusted, the relying party may establish a secure communications channel between it and the attester to share secrets with it.

Note that the nomenclature described does not prescribe an architecture. For instance, there is no requirement for the relying party and the verifier to be two separate entities or programs. There is likewise no restriction, for example, where a verifier cannot also be an attester.

### Roots of Trust
An entity in a trust hierarchy that is inherently trusted is said to be in the hierarchy’s root of trust. This is so because a root of trust cannot itself be attested to. This includes an entity that can assume the role of relying party during remote attestation but cannot also be an attester.

Consider a simple deployment model where an entity is both a relying party and verifier. This entity can establish trust with an attester, but whoever ultimately owns and operates the entity must necessarily trust it implicitly.

It follows that a component in the root of trust, be it hardware, firmware, or software, must provide a firm foundation from which to build security and trust.

## Attested TLS
Two peers who wish to communicate privately over an insecure channel such as the Internet must first establish a secret that they can use to encrypt and decrypt data. The most prevalent method of doing this is Transport Layer Security (TLS), formerly known as Secure Sockets Layer (SSL). TLS implements a handshake protocol based on asymmetric cryptography whereby two peers can agree on a secret encryption key without ever transmitting the key over the channel.

The two peers who wish to bootstrap a secure channel first each generate an asymmetric key. During the handshake, the peers exchange the public components of their corresponding asymmetric keys over the insecure channel. They then use each other’s public keys to compute an identical secret that they arrive at independently. The details of this computation vary depending on the key exchange method used and are beyond the scope of this document. An invariant is upheld by all cryptographic methods that guarantees that knowledge of the public keys does not result in an eavesdropper being able to also compute the secret.

Once the peers have computed the shared secret, they use it to configure a symmetric cipher that allows them to protect their data both from unauthorized access as well as from tampering while it is in transit.

In summary, TLS enables two peers to establish a secure communications tunnel over an initially insecure channel that provides them guarantees of both confidentiality and integrity.

### Authentication
TLS offers facilities to enable one or both peers to authenticate the other. With this functionality, each peer can independently ascertain the identity of the other during the handshake. In so doing, each can determine whether the other is who they think they are and thus decide whether to share any sensitive data.

Asymmetric cryptography is widely used for this type of authentication. More specifically, an asymmetric key pair can be regarded as a form of identity: if one entity knows the public key of another, the latter can prove their identity by providing proof of knowledge of the corresponding private component. In case an entity does not know the public key of another, it can attempt to ascertain its identity via a third-party known as a Certificate Authority (CA).

Certificate authorities are (usually) reputable entities that other entities choose to trust. There are many CAs that offer their services to the public and are directly or indirectly trusted by millions, forming a fabric of trust across the Internet. Other CAs are localized and specific, such as one internal to a company and trusted only by devices and services within an Intranet. A system of CAs, their corresponding identities, the identities for whom they vouch, and the entities who trust them is known as a Public Key Infrastructure (PKI). In a PKI, CAs are each identified by their own asymmetric key, the private part of which they carefully safeguard, and entities that trust them have a copy of the corresponding public components.

The role of a CA is to carefully evaluate evidence of identity produced by an entity, such as government-issued ID or company registration information. If the CA is satisfied, it produces a certificate for the entity’s public key. The certificate describes the entity, known as the subject; it names the CA, known as the issuer; it indicates what purposes the certificate may be used for; and it states the certificate’s period of validity. The certificate also carries a digest of the subject’s public key, a digest of the issuer’s public key, and a signature produced by the issuer over the contents of the certificate computed using the CA’s private key.

Using a PKI, an entity that wants to authenticate another but whose public key it does not recognize can request from the latter one or more chains of certificates for that key. If at least one of these chains is ultimately rooted in a CA that the authenticating entity trusts, it can rest assured of the identity of the other. A simpler way to state this is that A may not know B, but knows C who either directly vouches for B, or who vouches for a series of intermediaries which ultimately vouches for B.

A crucial and necessary aspect of the process of authentication in TLS is that the asymmetric key produced by the remote peer must be bound to the evidence of its identity. In other words, the public key that the remote peer sends through the insecure channel for the other peer to compute the shared secret with must be the same public key which the remote peer presents a certificate for and whose ultimate issuing authority the other peer trusts. Without this binding, the authentication serves no purpose as at least one of peers need not prove knowledge of the private key for which the certificate presented was issued and can thus instead be anybody.


### Remote Attestation
The process of authentication as described above in the context of client-server communication between a user and a service aids the user in establishing trust in the service provider. That is, a service provider launches one or more instances of a service and provides those instances with an asymmetric key and a corresponding certificate chain that identifies the provider as well as the hierarchy of entities that vouch for the provider’s identity. When a client conducts the TLS handshake with the service, the latter responds with these two pieces of information. With the asymmetric key and certificate chain in hand, the client can convince itself that the service is hosted by a known service provider.

This form of authentication makes no guarantees as to the trustworthiness of the service itself. If the service provider deployed malicious instances, if these instances have been compromised by malware, or if they are being actively monitored by the cloud service provider be it by malice or by force, the client has no way of finding out and aborting the handshake. The trust terminates in the service provider regardless of the trustworthiness of the service.

With confidential computing, the service provider is outside of the TCB. Thus, its identity is arguably irrelevant: it does not matter who hosts the service as long as the service itself and the hardware that it runs on can be proven to be trustworthy. Attested TLS (aTLS) binds the public key of the peer running in a TEE not to the identity of the service provider but to the attestation evidence produced by the TEE. In so doing, the authenticating peer (relying party) can ascertain that the secure communications channel being bootstrapped terminates within the confines of the peer being authenticated (attester). Additionally, if both sides of the TLS connection run in a TEE, attestation and key binding can be mutual. This may be used in scenarios where one or more service endpoints are backed by microservices that need to communicate with one another.

While the specifics of how key binding is achieved varies across TEE and aTLS implementations, the fundamental requirement remains: when a relying party wishes to establish an aTLS connection with an attester, the latter must include in the evidence that it produces a claim that identifies the public key and must submit it during the handshake. With that in place, the relying party, after successful appraisal of the evidence via a verifier, can ascertain that the public key sent by the attester for use in the computation of the shared key is the same as that claimed in the evidence. This in turn binds the channel’s encryption key to the trustworthiness of the attester.

### Topological Patterns
A TLS handshake begins with the client sending a ClientHello message to the server. Depending on the aTLS implementation, this message may include an explicit request for aTLS or the requirement may be assumed by both ends. The server in turn responds with a ServerHello message that can either include attestation evidence and possibly endorsements, or an attestation result readily produced by a verifier.

The Passport Model is defined by the server returning evidence and optionally endorsements to the client. In this model, the burden of appraising the evidence falls on the relying party, which must submit this information to a verifier. In contrast, the Background-Check Model is defined by the server itself submitting its evidence and optional endorsements to a verifier and returning to the client the corresponding attestation result produced by the verifier.

Regardless of which model is used, the client and server must agree on the model either ahead of time, during the handshake, or the client must be able to dynamically recognize and adapt to the server’s observed behavior.

## AMD SEV-SNP
In an effort to remove the hypervisor and cloud fabric from the TCB, AMD has added over the last several years several instruction set extensions to their processors. With the introduction of the Zen 3 architecture, AMD EPYC processors now provide the ability to instantiate a TEE in the form of a Confidential Virtual Machine (CVM).

The first extension that was added is Secure Memory Encryption (SME). SME was introduced in Zen 1 (Naples), allowing system software to mark individual pages of memory as private. In turn, the processor transparently encrypts and decrypts these pages as necessary using an ephemeral key known only to it that it generates during boot. A stricter version of SME called Transparent Secure Memory Encryption (TSME) was also added whereby the processor automatically encrypts all memory without intervention by system software. SME and TSME aid in thwarting a certain class of attacks where malicious sysadmins, hypervisor bugs, and physical access may leak user data.

SME was later extended in Zen 1 with Secure Encrypted Virtualization (SEV). This addition augments the behavior of SME with a different ephemeral encryption key per virtual machine. With SEV enabled, each virtual machine is assigned a different memory encryption key managed by the processor. Since the hypervisor and the virtual machines that it manages do not share the same encryption key, hypervisors are effectively rendered unable to read and extract virtual machine data.

SEV was subsequently extended with Encrypted State (SEV-ES) in Zen 2 (Rome). Whereas SEV protects VM memory, SEV-ES transparently encrypts and decrypts VM processor state. When SEV-ES is enabled, the hypervisor cannot, in addition to reading VM memory, access the VM’s registers when control is transferred from the VM to the hypervisor.

Finally, in Zen 3 (Milan), AMD introduced Secure Nested Paging (SEV-SNP). Whereas SEV and SEV-ES provide virtual machines with guarantees of confidentiality from the hypervisor, SEV-SNP provides guarantees of integrity, and additionally introduces support for remote attestation. Thus, the combination of SEV, SEV-ES, and SEV-SNP, collectively known as AMD SEV, allow for the creation and execution of TEE-compliant CVMs.


### Operational Overview
In the SEV-SNP threat model, the only components in the TCB are the processor, AMD’s Platform Security Processor (PSP), and the CVM itself. All other hardware, firmware, the hypervisor, the operating system, all device drivers, host-side user-mode software, as well as other VMs and CVMs along with their users and administrators, including the cloud service provider, are strictly outside of the TCB.

The core operating principle of SEV-SNP is that if a virtual machine writes data to a page in memory (a page is typically a 4KB chunk of byte-aligned memory), if and when the VM reads that page at any later time, it is guaranteed to read the same data that it previously wrote. If the data read differs from the data originally written, the processor alerts the VM to that effect. More specifically, SEV-SNP guards against replay attacks, data corruption, memory aliasing, and memory remapping by implementing additional access checks in hardware. The configuration of these checks is guarded by the hardware such that only authorized software may set up their behavior and only at the appropriate time of the lifecycle of a CVM. In addition, SEV-SNP introduces additional guardrails around interrupt delivery and hypervisor intercepts that cover other avenues by which a hypervisor may tamper with the integrity of a CVM.

It is important to understand that CVMs are instantiated out of an untrusted system state by untrusted software. It is the cloud fabric that decides on the parameters of the CVM and it is a potentially malicious hypervisor that loads code into the CVM before setting it in motion. For this reason, CVMs carry no secrets with them at the start of their lifecycle. Instead, SEV-SNP includes facilities for the remote attestation of CVMs. Only after careful appraisal of the evidence produced by SEV-SNP CVM can a user of the services provided by the CVM safely share secrets with it.


### Virtual Machine Startup
When a hypervisor is first requested to launch a virtual machine, one of its tasks is to populate the latter’s initial memory contents. These contents include both virtual machine and virtual device configuration as well as the code that the VM will execute immediately upon start. This code is typically hypervisor-specific firmware that allows the VM to set itself up, and to find and start the operating system.

Seeing as the hypervisor is untrusted, it could load into the CVM any code it desires. Similarly, since the cloud fabric and its sysadmins are also untrusted, they could tamper with the CVM’s contents before it has a chance to start. While the SEV-SNP hardware protects the integrity of the code once the CVM has launched, it is necessary to ensure during attestation that the code that initially seeded its execution is trustworthy.

To that end, the hypervisor interacts with the PSP throughout the launch flow of a CVM. At first, the hypervisor informs the PSP of its intention to launch a new CVM. In so doing, the PSP initializes a new state tracking structure for the CVM and protects it from the hypervisor. Then, for every page of memory that the hypervisor loads into the CVM, it informs the PSP. The SEV-SNP hardware only allows pages added in this way to be part of the CVM.

For each new page added, the PSP updates a running digest of the contents and metadata of every page loaded up to and including the last. This running digest consists of a series of hash extensions computed in the following manner:

`DIGEST_NEW := SHA-384(PAGE_INFO)`

where PAGE_INFO is a structure that holds the current running digest alongside a set of properties about the new page being added. These properties include a SHA384 digest of the contents of the new page, its read-write-execute permissions, and the guest physical address where it will be mapped in the CVM’s memory layout.

Once all pages are loaded, the hypervisor once again informs the PSP. At that point, the PSP performs final sanity checks on the CVM, transitions it into the running state, and protects it from further modification.

The final value of the running digest represents a cryptographic log, expressed as a single hash value, of the ordered sequence of steps that the hypervisor took while loading the virtual machine as well as of the contents, and properties of that content, that the hypervisor loaded into it. This value is known as the CVM’s launch digest, sometimes also referred to as its launch measurement, and is reflected during attestation.

Lastly, as part of the final message the hypervisor sends to the PSP, it may submit an arbitrary sequence of up to 32 bytes that the code running in the CVM can later retrieve. This array is known as host data, and is also included during attestation.

### Remote Attestation
Every processor that supports SEV-SNP carries a secret that is unique to it. In addition, each core in every processor ships with a given version of its microcode, and every PSP, with a given version of its firmware. Should an issue or security vulnerability be found after shipping, both the processor microcode and the PSP firmware can be upgraded at runtime provided the updates carry a signature the processor and PSP recognize, respectively.

The combination of the lowest microcode version across all processor cores and the version of the PSP firmware forms the TCB version. From a combination of the unique secret and the TCB version, the hardware derives an attestation key known as the Versioned Chip Endorsement Key (VCEK). For each VCEK, which is unique for each processor, AMD issues a certificate signed by the AMD SEV Signing Key (ASK). For the ASK in turn AMD issues a certificate signed by the AMD Root Key (ARK), one of which exists for every product (e.g., Milan, Rome, Naples, etc.). For the ARK, AMD issues a self-signed certificate and publishes it.

When a workload running in a CVM is challenged to produce evidence for attestation, it issues a request to the PSP to generate an attestation report. In a cloud setting, this request is routed from the workload in user-mode to the kernel-mode SEV guest driver, out to the hypervisor, and finally to the PSP of the physical server where the cloud fabric scheduled the workload.

The PSP attestation report contains a variety of fields including the CVM’s launch digest, a workload-provided field known as report data, and the value of host data. The entirety of the report is in turn signed by the VCEK.

The report data field contains any data that the workload wishes to include in the report. Typically, a workload uses this field to encode a combination of a nonce and a public key that helps ensure the freshness of the evidence and to establish a secure channel of communication with the workload, respectively.

During attestation, the verifier appraises the report by first verifying that the signature around it was produced by a VCEK that is rooted to a well-known, non-revoked ARK certificate. If this is true, the verifier knows that the report was generated by a genuine AMD PSP on a real, SEV-SNP platform. Thereafter, the verifier ensures that the TCB version is sufficiently recent as a means to ensure that the issuing platform does not have any known security vulnerabilities that could render the report untrustworthy. Thereafter, the verifier ensures that fields such as the launch digest, report data, host data, and potentially others depending on its evidence appraisal policy, are acceptable in accordance with its reference values.

To aid verifiers in validating VCEK signatures, AMD hosts a Key Distribution Service (KDS). The KDS is a Web service that retrieves VCEK certificates signed by the appropriate ASK for each unique processor and TCB version. Additionally, the KDS serves ASK and ARK certificates for each supported product as well as a corresponding Certificate Revocation List (CRL). With the KDS, verifiers can build full certificate chains that help ensure that signatures around attestation reports were generated by genuine SEV-SNP platforms.
