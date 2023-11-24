from pyVim import connect
from pyVmomi import vim
import ssl

def connect_to_vcenter(vcenter_ip, username, password):
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        service_instance = connect.SmartConnect(
            host=vcenter_ip,
            user=username,
            pwd=password,
            sslContext=ssl_context
        )
        print("Connected to vCenter Server")
        return service_instance

    except Exception as e:
        print("Connection failed:", e)
        return None

def list_vms(service_instance):
    if service_instance:
        try:
            content = service_instance.RetrieveContent()
            vm_view = content.viewManager.CreateContainerView(
                content.rootFolder, [vim.VirtualMachine], True
            )
            vms = vm_view.view

            print("List of VMs:")
            for index, vm in enumerate(vms, start=1):
                print(f"{index}. VM Name: {vm.name}")

            return vms

        except Exception as e:
            print("Failed to list VMs:", e)
            return []

def get_vm_status(vm):
    if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
        return "Powered On"
    elif vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOff:
        return "Powered Off"
    elif vm.runtime.powerState == vim.VirtualMachinePowerState.suspended:
        return "Suspended"
    else:
        return "Unknown"

def display_vm_status(vms):
    print("\nVM Status:")
    for index, vm in enumerate(vms, start=1):
        print(f"{index}. VM Name: {vm.name}, Status: {get_vm_status(vm)}")

def start_vm(service_instance, vms):
    if service_instance:
        try:
            selected_vm = int(input("Enter the number of the VM to start: "))
            vm = vms[selected_vm - 1]
            print(f"Starting VM: {vm.name}")
            vm.PowerOn()

        except Exception as e:
            print(f"Failed to start VM:", e)

def stop_vm(service_instance, vms):
    if service_instance:
        try:
            selected_vm = int(input("Enter the number of the VM to stop: "))
            vm = vms[selected_vm - 1]
            print(f"Stopping VM: {vm.name}")
            vm.PowerOff()

        except Exception as e:
            print(f"Failed to stop VM:", e)

if __name__ == "__main__":
    vcenter_ip = '192.168.232.132'
    username = 'root'
    password = 'Sandip@1997'

    service_instance = connect_to_vcenter(vcenter_ip, username, password)

    if service_instance:
        vms = list_vms(service_instance)

        if vms:
            while True:
                print("\nOptions:")
                print("1. List VMs and Status")
                print("2. Start a VM")
                print("3. Stop a VM")
                print("4. Exit")

                choice = input("Enter your choice (1/2/3/4): ")

                if choice == '1':
                    display_vm_status(vms)
                elif choice == '2':
                    start_vm(service_instance, vms)
                elif choice == '3':
                    stop_vm(service_instance, vms)
                elif choice == '4':
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 4.")

        connect.Disconnect(service_instance)
        print("Disconnected from vCenter Server")
