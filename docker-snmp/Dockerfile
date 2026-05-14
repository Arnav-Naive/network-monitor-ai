FROM ubuntu:22.04

# Install SNMP daemon
RUN apt-get update && \
    apt-get install -y snmpd && \
    rm -rf /var/lib/apt/lists/*

# Copy metric scripts
COPY scripts/*.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/*.sh

# Configure SNMP
COPY snmpd.conf /etc/snmp/snmpd.conf

# Expose SNMP port
EXPOSE 161/udp

# Start SNMP daemon
CMD ["snmpd", "-f", "-Lo", "-C", "-c", "/etc/snmp/snmpd.conf"]