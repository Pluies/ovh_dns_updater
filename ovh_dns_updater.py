import json
import os
import ovh
from kubernetes import client, config

# Sanity checks
for k in [
        'OVH_APPLICATION_KEY',
        'OVH_APPLICATION_SECRET',
        'OVH_CONSUMER_KEY',
        'DNS_ZONE',
        'DNS_SUBDOMAIN',
        ]:
    if k not in os.environ:
        raise KeyError('Required env var ' + k + ' not found in environment!')

# Config mapping
zone      = os.getenv('DNS_ZONE')
subdomain = os.getenv('DNS_SUBDOMAIN')
ttl       = os.getenv('DNS_TTL', 30)

# Configs can be set in Configuration class directly or using helper utility
config.load_incluster_config()

v1 = client.CoreV1Api()
ret = v1.list_node(watch=False)
external_ips = []
for node in ret.items:
    external_ips += [i.address
            for i in node.status.addresses
            if i.type == 'ExternalIP']

print("Current node ExternalIPs: %s" % external_ips)

client = ovh.Client(
    endpoint='ovh-eu',
    application_key=os.getenv('OVH_APPLICATION_KEY'),
    application_secret=os.getenv('OVH_APPLICATION_SECRET'),
    consumer_key=os.getenv('OVH_CONSUMER_KEY'),
)

# Get the existing records
records = [client.get('/domain/zone/%s/record/%s' % (zone, r))
        for r in client.get('/domain/zone/%s/record' % zone,
            subDomain=subdomain,
            fieldType='A')]

missing_external_ips = external_ips.copy()

# Now reconcile!
for r in records:
    # For each record... If matching a node, all good, otherwise delete
    if r['target'] in external_ips:
        print("Found existing record matching node:")
        print(json.dumps(r, sort_keys=True, indent=2))
        missing_external_ips.remove(r['target'])
    else:
        print("Found outdated record:")
        print(json.dumps(r, sort_keys=True, indent=2))
        print("Deleting...")
        client.delete('/domain/zone/%s/record/%s' % (zone, r['id']))

# Create new records for new nodes
for i in missing_external_ips:
    print("Adding record for IP: %s" % i)
    result = client.post('/domain/zone/%s/record' % zone,
            fieldType='A',
            subDomain=subdomain,
            target=i,
            ttl=ttl)
    print(json.dumps(result, sort_keys=True, indent=2))
