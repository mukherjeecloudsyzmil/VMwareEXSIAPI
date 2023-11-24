from pyVim import connect
from pyVmomi import vim  # Import the vim module

import ssl

# Disable SSL certificate verification
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

    # Retrieve content
    content = service_instance.RetrieveContent()

    # Get VMs
    vm_view = content.viewManager.CreateContainerView(
        content.rootFolder, [vim.VirtualMachine], True
    )
    vms = vm_view.view

    # List VMs
    print("List of VMs:")
    for vm in vms:
        print("VM Name:", vm.name)

    # Disconnect from vCenter Server
    connect.Disconnect(service_instance)
    print("Disconnected from vCenter Server")

except Exception as e:
    print("Connection failed:", e)
