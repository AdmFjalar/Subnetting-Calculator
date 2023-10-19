import os
import ipaddress
import math
import matplotlib.pyplot as plt

def ClearConsole():
    os.system('cls')

def CalculateMaxSubnets(ip, cidr):
    maxSubnets = 0
    if (ValidateIPAndCIDR(ip, cidr)):
        maxSubnets = 2 ** (32 - cidr)                                           # Calculates the maximum number of subnets for the given IP and CIDR notation
    return maxSubnets

def CalculateSubnets(ip, cidr, hostsPerSubnet):
    subnets = []
    if (ValidateIPAndCIDR(ip, cidr)):
        for i in range(len(hostsPerSubnet)):                                                                                                                            # Loops through the number of hosts per subnet
            if i == 0:
                subnets.append(ipaddress.IPv4Network(f'{ip}/{CIDRFromHosts(hostsPerSubnet[i])}', strict=False))                                       # Calculates the subnet mask for the given IP, CIDR, and hosts per subnet (first subnet)
            else:
                subnets.append(ipaddress.IPv4Network(f'{subnets[i-1].broadcast_address + 1}/{CIDRFromHosts(hostsPerSubnet[i])}', strict=False))   # Calculates the subnet mask for the given IP, CIDR, and hosts per subnet
    return subnets

def CIDRFromHosts(hosts):
    return 32 - math.ceil(math.log2(hosts))

def ValidateIPAndCIDR(ip, cidr):
    try:
        ipaddress.IPv4Network(f'{ip}/{cidr}', strict=False)                 # Creates a network from the given IP and CIDR notation (only used to check for invalid IP address or CIDR notation)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError):      # If the IP address or CIDR notation is invalid, print error message and return
        print("Invalid IP address or CIDR notation.\n")
        return False
    return True

def VisualizeSubnets(baseNetwork, subnets):
    fig, ax = plt.subplots()
    plt.show()

def Main():
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

    maxSubnets = CalculateMaxSubnets(ip, cidr)                      # Calculates the maximum number of subnets for the given IP and CIDR

#create a while loop here
    doSubs=True
    hostsPerSubnet = []                                             # Initializes the list of hosts per subnet (MOVED FROM TRY)
    while doSubs:                                                       #loops as long as doSubs=True 
        try:
                                                  
            for i in range(len(hostsPerSubnet), maxSubnets):                                 # Loops through the max number of subnets
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
                    doSubs=False                                        #Sets doSubs to false and ends loop
                    break
                set_bool=input("Continue? Enter Y to continue or N to finish: ") #asks user if they want to keep making subnets or finish
                if set_bool.lower()=='y':
                    doSubs=True                                                  #continues loop
                elif set_bool.lower()=='n':
                    doSubs=False                                                 #ends loop
                else:
                    print(f'\nInvalid input, please enter Y or N: ')
            hostsPerSubnet.sort(reverse=True)

        
        except ValueError:
            print("Invalid input data type.")                                #breaks Try and continues loop if data error
            doSubs=True
            
#end loop here

    subnets = CalculateSubnets(ip, cidr, hostsPerSubnet)    # Calculates the subnet masks for the given IP, CIDR, and hosts per subnet

    if subnets:                                                 # If subnetMasks is not empty, print the subnet details
        VisualizeSubnets(ipaddress.IPv4Network(f'{ip}/{cidr}', strict=False), subnets)
        print("\nCalculated Subnet Details:")
        for index, subnet in enumerate(subnets, start=1):
            print(f"Subnet {index}:\t{subnet.network_address}/{subnet.prefixlen}")
            print(f"\tSubnet Mask:\t\t{subnet.netmask}")
            print(f"\tNetwork Address:\t{subnet.network_address}")
            print(f"\tBroadcast Address:\t{subnet.broadcast_address}")
            print(f"\tHost Range:\t\t{subnet.network_address + 1} - {subnet.broadcast_address - 1}\n")
Main()  # Calls the main function