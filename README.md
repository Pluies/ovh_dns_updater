ovh_dns_updater
===============

Python script to be ran inside a Kubernetes cluster to grab nodes' IPs and update corresponding DNS records in OVH.

Configuration
-------------

This script expects the following env vars to be set:

- `OVH_APPLICATION_KEY`, `OVH_APPLICATION_SECRET`, `OVH_CONSUMER_KEY`:

OVH credentials as per [OVH token creation page](https://api.ovh.com/createToken/index.cgi?GET=/*&PUT=/*&POST=/*&DELETE=/*)

- `DNS_ZONE`, `DNS_SUBDOMAIN`:

Zone and subdomain, e.g. `DNS_ZONE=example.dom` `DNS_SUBDOMAIN=kubernetes` to update DNS records for [kubernetes.example.com](kubernetes.example.com)

Run
---

    python ./ovh_dns_updater.py
