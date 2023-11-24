import ssl
from pyVim import connect

# Disable SSL verification
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_NONE

# Define the connection parameters
vcenter_ip = '192.168.232.132'
username = 'root'
password = 'Sandip@1997'

# Connect to vCenter Server
try:
    service_instance = connect.SmartConnect(
        host=vcenter_ip,
        user=username,
        pwd=password,
        sslContext=ssl_context
    )
    print("Connected to vCenter Server")

    # Disconnect from vCenter Server
    connect.Disconnect(service_instance)
    print("Disconnected from vCenter Server")

except Exception as e:
    print("Connection failed:", e)
