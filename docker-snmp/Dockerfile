FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y snmpd && \
    rm -rf /var/lib/apt/lists/*

COPY scripts/*.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

COPY snmpd.conf /etc/snmp/snmpd.conf

EXPOSE 161/udp

CMD ["snmpd", "-f", "-Lo", "-C", "-c", "/etc/snmp/snmpd.conf"]