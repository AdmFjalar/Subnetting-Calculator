import os
import ipaddress
import math

# Clear the console screen
def ClearConsole():
    os.system('cls')

# Calculate the maximum number of subnets for the given IP and CIDR
def CalculateMaxSubnets(ip, cidr):
    if ValidateIPAndCIDR(ip, cidr):
        return 2 ** (32 - cidr)

# Calculate the subnet masks for the given IP, CIDR, and hosts per subnet
def CalculateSubnets(ip, cidr, hostsPerSubnet):
    if ValidateIPAndCIDR(ip, cidr):
        subnets = []
        for i, hosts in enumerate(hostsPerSubnet):
            subnet_ip = ip if i == 0 else str(subnets[i - 1].broadcast_address + 1)
            subnet = CalculateNetwork(subnet_ip, CIDRFromHosts(hosts))
            subnets.append(subnet)
        return subnets

# Calculate the network based on the given IP and CIDR
def CalculateNetwork(ip, cidr):
    return ipaddress.IPv4Network(f'{ip}/{cidr}', strict=False)

# Calculate CIDR notation based on the number of hosts
def CIDRFromHosts(hosts):
    return 32 - math.ceil(math.log2(int(hosts)))

# Validate the given IP address and CIDR notation
def ValidateIPAndCIDR(ip, cidr):
    try:
        CalculateNetwork(ip, cidr)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        print("Invalid IP address or CIDR notation.\n")
        return False
    return True

# Check if a list is sorted
def CheckSortedList(listToCheck):
    isSorted = True
    l = len(listToCheck)
    for i in range(l - 1):
        if listToCheck[i] < listToCheck[i + 1]:
            isSorted = False
    return isSorted

# Used if wanting to subnet in the console rather than the web UI.
def RunInConsole():
    ClearConsole()
    ip, cidr = GetUserInput()

    maxSubnets = CalculateMaxSubnets(ip, cidr)

    hostsPerSubnet = GetHostsPerSubnet(maxSubnets, cidr)
    subnets = CalculateSubnets(ip, cidr, hostsPerSubnet)

    if subnets:
        print("\nCalculated Subnet Details:")
        for index, subnet in enumerate(subnets, start=1):
            print(f"Subnet {index}:\t{subnet.network_address}/{subnet.prefixlen}")
            print(f"\tSubnet Mask:\t\t{subnet.netmask}")
            print(f"\tNetwork Address:\t{subnet.network_address}")
            print(f"\tBroadcast Address:\t{subnet.broadcast_address}")
            print(f"\tHost Range:\t\t{subnet.network_address + 1} - {subnet.broadcast_address - 1}\n")

# Entry point of the script
# if __name__ == "__main__":
#     RunInConsole()