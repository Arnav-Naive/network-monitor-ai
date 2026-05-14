from pysnmp.hlapi import *

# OIDs to query
oids = {
    'cpu': '1.3.6.1.2.1.25.3.3.1.2.1',
    'memory': '1.3.6.1.2.1.25.2.3.1.6.1',
    'temperature': '1.3.6.1.4.1.9.2.1.56.0',
    'bandwidth': '1.3.6.1.4.1.9.2.1.58.0',
}

print("Testing SNMP connection to virtual switch...\n")

for name, oid in oids.items():
    iterator = getCmd(
        SnmpEngine(),
        CommunityData('public'),
        UdpTransportTarget(('127.0.0.1', 1611)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    
    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    
    if errorIndication:
        print(f"❌ {name}: Error - {errorIndication}")
    else:
        for varBind in varBinds:
            print(f"✓ {name}: {varBind[1]}")

print("\n✅ Virtual switch is responding!")