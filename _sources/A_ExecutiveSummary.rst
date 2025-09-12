.. _ExecutiveSummary:

Executive Summary
=================

There are sector specific requirements that call for organizations
to monitor network activity, protect sensitive data, and demonstrate 
security controls.  Enterprises leverage network traffic visibility 
in their security operations centers to prevent, detect, and respond 
to cybersecurity threats. Enterprises moving to newer network security 
protocol standards such as TLS 1.3 will face challenges for maintaining 
network traffic visibility. 

Modern protocol designers have changed protocols to strengthen security 
properties that protect the secrecy of historical network traffic. This 
is possible even if the servers' long-term secret keys are compromised —
a property known as forward secrecy. However, forward secrecy has created 
significant challenges for the network visibility strategies used by enterprises.

The National Cybersecurity Center of Excellence (NCCoE), in collaboration 
with technology providers and enterprise customers, initiated a project 
demonstrating options for maintaining visibility within an enterprise adopting 
these new security protocols. The demonstrations are suitable for voluntary 
adoption across a wide range of enterprise architectures. They are scalable, 
actionable, and application protocol-agnostic, as well as usable in real-time 
following post-packet capture.

Enterprises using the Transport Layer Security (TLS) 1.2 protocol without forward 
secrecy deploy tools and architectural solutions that provide visibility into 
enterprise traffic within their network. Enterprises have regulatory and compliance 
requirements to maintain visibility into received network traffic to enable the 
organization's security monitoring, analysis, and management policies. An enterprise 
will not be able to use its deployed tools and architectural solutions that provide 
visibility into enterprise TLS 1.2 traffic to have visibility into TLS 1.3 traffic. 
This publication includes demonstrated approaches for enterprises to adopt TLS 1.3 
to allow enterprises to benefit from the security functionality of TLS 1.3 while 
maintaining the visibility into received network traffic.

This publication describes the motivation, approach, architecture, build implementation, 
demonstration scenarios, results, and risk and compliance management characteristics 
for the demonstrated proofs of concept. The top-level overview provides links to 
technical details that are contained in online NIST pages. The linked files provide 
detailed technical information for each demonstration that TLS visibility implementers 
can adopt in their own environments. The demonstrations in this publication to maintain 
visibility are not intended as a recommended default or even for common use but to 
assist in those areas where, as OMB M 22-09 states: "...as agencies segment their networks, 
move away from intranets, and permit access to enterprise services from any network, 
inspecting traffic in these environments will become less practical and less valuable 
over time. In other places, deep traffic inspection may be more valuable and can create 
less of an increase in attack surface."
