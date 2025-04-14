.. _ExecutiveSummary:

Executive Summary
=================

Enterprises need visibility into the data transiting their
networks—particularly their enterprise data centers to implement
critical cybersecurity, operational, and regulatory controls (e.g.,
intrusion detection and response, malware detection, troubleshooting, and
fraud monitoring). Implementing network security protocols in enterprise
data centers to ensure data integrity and confidentiality has posed
challenges for maintaining the necessary network visibility required by
these controls. To maintain visibility, enterprise architectures
typically use passive or active monitoring devices to facilitate
comprehensive inspection, collection, and analysis of internal network
traffic. In the past, decryption of network traffic by passive
decryption devices involved providing copies of servers' long-term
cryptographic keys purely for monitoring and inspection purposes. In
these cases, long-term cryptographic keys allow the decryption of past,
present, and future network traffic for the lifetime of a key.

Modern protocol designers have changed protocols to strengthen security
properties that protect the secrecy of historical traffic. This is
possible even if the servers' long-term secret keys are compromised—a
property known as *forward secrecy*. However, forward secrecy has
created significant challenges for the network visibility strategies
used by enterprises.

The National Cybersecurity Center of Excellence (NCCoE) , in
collaboration with technology providers and enterprise customers,
initiated a project demonstrating options for maintaining visibility
within an enterprise in the face of the challenges presented by these
new security protocols. The example solutions demonstrated are suitable
for voluntary adoption across a wide range of user environments. They
are scalable, actionable, and application protocol-agnostic, as well as
usable in real-time following post-packet capture. The solutions
demonstrate approaches for enterprises to adopt Transport Layer Security
(TLS) 1.3, reap the benefits from the improved security functionality,
while maintaining the visibility that they have come to expect.

Enterprises using the TLS 1.2 protocol without forward secrecy (which
was how TLS 1.2 was originally specified), deploy tools and
architectural solutions that provide visibility into enterprise traffic
within their network. Enterprise visibility into received network
traffic should remain intact to enforce the organization's security
monitoring, analysis, and management policies. Monitoring and analysis
tools that conform to their security policies are dependent on
visibility solutions that enable an enterprise-authorized party to
decrypt past, present, and future network traffic. The solutions
demonstrate approaches for enterprises to adopt TLS 1.3, reap the
benefits from the improved security functionality, while maintaining the
visibility that they have come to expect.

This publication describes the motivation, approach, architecture, build implementation,
demonstration scenarios, results, and risk and compliance management characteristics for
the demonstrated proofs of concept. The top-level overview provides links to technical
details that are contained in GitHub files. The linked files provide detailed technical
information for each build that technology implementers can emulate in their own environments.
This implementation demonstration is not intended as a recommended default or even for common
use but to assist in those areas where, as OMB M 22-09 states: "...as agencies segment their
networks, move away from intranets, and permit access to enterprise services from any network,
inspecting traffic in these environments will become less practical and less valuable over time.
In other places, deep traffic inspection may be more valuable and can create less of an increase
in attack surface."