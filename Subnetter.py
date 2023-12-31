import os
import ipaddress
import math

# Clear the console screen
def ClearConsole():
    os.system('cls')

# Calculate the maximum number of subnets for the given IP and CIDR
def CalculateAddressSpace(ip, cidr):
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
    while True:
        try:                # Gets user input and tries to convert to int
            ip = input("Enter the base IP address: ")
            cidr = int(input("Enter the CIDR notation (e.g., 24): "))
        except ValueError:  # If input cannot be converted to int, print error message and return
            print("Invalid input data type.")
        if ValidateIPAndCIDR(ip, cidr):
            break
    print("\n")

    maxSubnets = CalculateAddressSpace(ip, cidr)                      # Calculates the maximum number of subnets for the given IP and CIDR

    continueSubnetting=True
    hostsPerSubnet = []                                             # Initializes the list of hosts per subnet (MOVED FROM TRY)
    while continueSubnetting:                                                       #loops as long as doSubs=True 
        try:                                     
            for i in range(len(hostsPerSubnet), maxSubnets):                                 # Loops through the max number of subnets
                if (continueSubnetting==False):                                         # If continueSubnetting is false, break loop
                    break
                maxHosts = (2 ** (32 - cidr))                           # Calculates the maximum number of hosts for the given IP and CIDR
                addressesLeft = maxHosts - sum(hostsPerSubnet)          # Calculates the number of addresses left after subtracting the number of hosts for each subnet
                print("\n-------------------------------------------")
                print(f"----------------- SUBNET {i + 1} ----------------")
                print("-------------------------------------------")
                print(f"Total number of adresses left: {addressesLeft}")                                                            # Prints the number of addresses left in the range
                print(f"Maximum number of hosts supported for subnet {i+1}: {2**math.floor(math.log2(addressesLeft)) - 2}")         # Prints the maximum number of hosts supported for the subnet
                hostsPerSubnet.append(2**math.ceil(math.log2(int(input(f"Enter the number of hosts for this subnet: ")) + 2)))      # Gets user input and calculates the number of hosts for the subnet
                if (hostsPerSubnet[i] > addressesLeft):                                                                             # If the number of hosts entered is greater than the number of addresses left, print error message and default to the max number of hosts supported
                    print(f"\nToo many hosts entered, will now default to {2**math.floor(math.log2(addressesLeft)) - 2} hosts.\n")  # Prints the number of hosts that will be used for the subnet
                    hostsPerSubnet[i] = 2**math.floor(math.log2(addressesLeft))
                addressesLeft = maxHosts - sum(hostsPerSubnet)          # Calculates the number of addresses left after subtracting the number of hosts for each subnet
                if (addressesLeft <= 0):                                # If the number of addresses left is less than or equal to 0, print message and break loop
                    print("Max hosts reached.")
                    continueSubnetting=False                                        #Sets doSubs to false and ends loop
                    break
                hostsPerSubnet.sort(reverse=True)                       # Sorts the list of hosts per subnet in descending order
                set_bool=""
                while set_bool.lower()!='y' and set_bool.lower()!='n':  # Loops until user enters y or n
                    set_bool = input("Continue? Enter Y to continue or N to finish: ") # Asks user if they want to keep making subnets or finish
                    if set_bool.lower()=='y':
                        continueSubnetting=True                                                 # Continues loop
                    elif set_bool.lower()=='n':
                        continueSubnetting=False                                                # Ends loop
                    else:
                        print(f'\nInvalid input, please enter Y or N: ')
        except ValueError:
            print("Invalid input data type.")
            continueSubnetting=True
    subnets = CalculateSubnets(ip, cidr, hostsPerSubnet)    # Calculates the subnet masks for the given IP, CIDR, and hosts per subnet

    if subnets:                                                 # If subnetMasks is not empty, print the subnet details
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