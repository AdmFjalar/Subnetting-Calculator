from flask import Flask, render_template, url_for, request, redirect, flash
from Subnetter import *
import random
import colorsys

subnetColors = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yW]4OU*p41"&~vNUiVj&/{(/FJFL4P="Q%ZrVt+7$~"E8)_Zpr(I?su*acWH^WF'

@app.route('/')
def Index():
    # Define the data you want to pass to the template
    networkAddress = "192.168.0.0"
    cidr = 24

    subnetColors.clear()

    # Pass the data to the template
    return render_template("index.html", network_address=networkAddress, cidr=cidr)



# Flask route for handling POST requests to generate a URL
@app.route('/generate_url', methods=['POST'])
def GenerateURL():
    # Extracting data from the form submitted via POST
    baseIP = request.form['base_ip']
    baseCIDR = int(request.form['base_cidr'])
    hostsPerSubnet = request.form.get('hosts_per_subnet', [])

    # Validate the provided IP and CIDR
    if not ValidateIPAndCIDR(baseIP, baseCIDR):
        flash("Invalid IP and/or CIDR!", 'error')
        return redirect('/')

    # Convert the hostsPerSubnet string to a list of integers
    if hostsPerSubnet:
        hostsPerSubnet = [int(subnetHosts) for subnetHosts in hostsPerSubnet.split("-")]

    # Initialize hostsPerSubnet as an empty list if it's not provided
    if hostsPerSubnet == "":
        hostsPerSubnet = []

    # Extract the total number of hosts requested
    hosts = int(request.form.get('hosts', 0))

    # Calculate the maximum number of hosts for the given CIDR
    maxHosts = 2 ** (32 - baseCIDR)

    # Initialize a variable to track the hosts list for URL generation
    hostsList = "new"

    # Process the hosts list based on user input
    if not hosts and hostsPerSubnet:
        # If hosts are not provided but hostsPerSubnet is, use hostsPerSubnet as the list
        hostsList = "-".join([str(item) for item in hostsPerSubnet])
    elif hosts:
        # If hosts are provided, calculate and adjust the hostsPerSubnet list
        addressesLeft = maxHosts - sum(hostsPerSubnet)

        if addressesLeft > 0:
            # Ensure hosts is a power of 2 and fits within the available addresses
            hosts = 2 ** math.ceil(math.log2(hosts))
            if hosts > addressesLeft:
                hosts = 2 ** math.floor(math.log2(addressesLeft))

            # Add the calculated hosts to the hostsPerSubnet list
            hostsPerSubnet.append(hosts)

            # Check and sort the list in reverse order
            if not CheckSortedList(hostsPerSubnet):
                hostsPerSubnet.sort(reverse=True)
                flash("Re-ordered subnets to fit a larger subnet", 'warning')

        # Update the hostsList variable with the modified hostsPerSubnet list
        hostsList = "-".join([str(item) for item in hostsPerSubnet])

    # Generate the URL based on the provided parameters
    url = f"/subnet/{baseIP}/{baseCIDR}/{hostsList}"

    # Redirect the user to the generated URL
    return redirect(url)



# Flask route for displaying subnet information based on user input
@app.route('/subnet/<baseIP>/<baseCIDR>/<hosts>')
def ShowSubnet(baseIP, baseCIDR, hosts):
    # Check if the hosts parameter is set to "new" and handle it accordingly
    if hosts == "new":
        hosts = []
    else:
        # Get hosts list by splitting hosts parameter
        hosts = hosts.split("-")

    # Validate the provided IP and CIDR
    if not ValidateIPAndCIDR(baseIP, baseCIDR):
        flash("Invalid IP and/or CIDR!", 'error')
        return redirect('/')

    # Calculate the maximum number of hosts for the given CIDR
    maxHosts = 2 ** (32 - int(baseCIDR))

    # Initialize an empty list for recalculated hosts
    recalculatedHosts = []

    # Loop through provided hosts and recalculate them to the nearest power of 2
    for i in range(len(hosts)):
        recalculatedHosts.append(2 ** math.ceil(math.log2(int(hosts[i]))))

        # Add a random color for each subnet (if needed)
        if len(subnetColors) < len(hosts):
            subnetColors.append('#' + '%06x' % random.randint(0, 0xFFFFFF))

    # Call subnetter functions to generate subnets
    generatedSubnets = CalculateSubnets(baseIP, baseCIDR, recalculatedHosts)

    # Get the number of generated subnets
    numberOfSubnets = len(generatedSubnets)

    # Calculate the number of addresses left after allocating subnets
    addressesLeft = maxHosts - sum(recalculatedHosts)

    # Ensure that the number of addresses left is non-negative
    if addressesLeft < 0:
        # If negative, adjust the hosts list and redirect to a new URL
        while addressesLeft < 0:
            recalculatedHosts.pop()
            addressesLeft = maxHosts - sum(recalculatedHosts)
        hostsList = "-".join([str(item) for item in recalculatedHosts])
        url = f"/subnet/{baseIP}/{baseCIDR}/{hostsList}"
        return redirect(url)

    # Initialize CIDR available to the default value of 32
    cidrAvailable = 32

    # If there are still available addresses, calculate the CIDR from the remaining hosts
    if addressesLeft > 0:
        cidrAvailable = CIDRFromHosts(addressesLeft)
        # Adjust CIDR if the calculated value is greater than the actual addresses left
        if 2 ** cidrAvailable > addressesLeft:
            cidrAvailable = 32 - math.floor(math.log2(int(addressesLeft)))

    # Calculate base network object and extract base broadcast address
    baseNetwork = CalculateNetwork(baseIP, baseCIDR)
    baseBroadcast = baseNetwork.broadcast_address

    # Render the template with the calculated subnet information
    return render_template('subnet-results.html',
                           base_ip=baseIP,
                           base_cidr=baseCIDR,
                           generatedSubnets=generatedSubnets,
                           numberOfSubnets=numberOfSubnets,
                           addressesLeft=addressesLeft,
                           cidrAvailable=cidrAvailable,
                           subnetColors=subnetColors,
                           hostsPerSubnet=recalculatedHosts,
                           base_broadcast=baseBroadcast,
                           actual_hosts=hosts)



#Route to aboutapp child
@app.route('/aboutapp')
def AboutApp():
    return render_template("aboutapp.html")

#Route to aboutSubnet child
@app.route('/aboutsubnets')
def AboutSubnets():
    return render_template("aboutsubnets.html")


if __name__ == "__main__":
    app.run(debug=True)
