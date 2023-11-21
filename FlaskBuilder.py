from flask import Flask, render_template, url_for, request, redirect, flash
from Subnetter import *
import random
import colorsys

subnetColors = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yW]4OU*p41"&~vNUiVj&/{(/FJFL4P="Q%ZrVt+7$~"E8)_Zpr(I?su*acWH^WF'

@app.route('/')
def HomeFunc():
    # Define the data you want to pass to the template
    network_address = "192.168.0.0"
    cidr = 24

    subnetColors.clear()

    # Pass the data to the template
    return render_template("index.html", network_address=network_address, cidr=cidr)

@app.route('/about')
def AboutFunc():
    return render_template("About")

@app.route('/generate_url', methods=['POST'])
def generate_url():
    base_ip = request.form['base_ip']   
    base_cidr = int(request.form['base_cidr'])
    hostsPerSubnet = request.form.get('hosts_per_subnet', [])

    if (ValidateIPAndCIDR(base_ip, base_cidr) == False):
        flash("Invalid IP and/or CIDR!", 'error')
        return redirect('/')

    if hostsPerSubnet:
        hostsPerSubnet = [ int(subnetHosts) for subnetHosts in hostsPerSubnet.split("-")]
    if hostsPerSubnet == "":
        hostsPerSubnet = []
    hosts = int(request.form.get('hosts', 0))

    maxHosts = (2 ** (32 - base_cidr))      
    
    hostsList = "new"
    if not hosts and hostsPerSubnet:
        hostsList = "-".join([str(item) for item in hostsPerSubnet])
    elif hosts:
        addressesLeft = maxHosts - sum(hostsPerSubnet)

        if addressesLeft > 0:    
            hosts = 2**math.ceil(math.log2(hosts))
            if hosts > addressesLeft:
                hosts = 2**math.floor(math.log2(addressesLeft))
            hostsPerSubnet.append(hosts)
            hostsPerSubnet.sort(reverse=True)
        hostsList = "-".join([str(item) for item in hostsPerSubnet])

    url = f"/subnet/{base_ip}/{base_cidr}/{hostsList}"
    
    return redirect(url)

@app.route('/subnet/<base_ip>/<base_cidr>/<hosts>')
def show_subnet(base_ip, base_cidr, hosts):
    if hosts == "new":
        hosts = []
    else:
        # Get hosts list by splitting hosts_list 
        hosts = hosts.split("-")
   
    if (ValidateIPAndCIDR(base_ip, base_cidr) == False):
        flash("Invalid IP and/or CIDR!", 'error')
        return redirect('/')

    maxHosts = (2 ** (32 - int(base_cidr)))

    recalculatedHosts = []

    for i in range(len(hosts)):
        recalculatedHosts.append(2**math.ceil(math.log2(int(hosts[i]))))
        if (len(subnetColors) < len(hosts)):     
            subnetColors.append('#' + '%06x' % random.randint(0, 0xFFFFFF))
    if (CheckSortedList(recalculatedHosts) == False):
        recalculatedHosts.sort(reverse=True)
    
    # Call subnetter functions to generate subnets    
    generatedSubnets = CalculateSubnets(base_ip, base_cidr, recalculatedHosts)
   
    numberOfSubnets = len(generatedSubnets)

    addressesLeft = maxHosts - sum(recalculatedHosts)
    
    cidrAvailable = 32

    if (addressesLeft > 0):
        cidrAvailable = CIDRFromHosts(addressesLeft)
        if (2**cidrAvailable > addressesLeft):
            cidrAvailable = 32 - math.floor(math.log2(int(addressesLeft)))

    # calculate base network object and extract base broadcast
    baseNetwork=CalculateRootNetwork(base_ip, base_cidr)
    base_broadcast=baseNetwork.broadcast_address

    # Return results template

    return render_template('subnet-results.html',
                          base_ip=base_ip,   
                          base_cidr=base_cidr,
                          generatedSubnets=generatedSubnets,
                          numberOfSubnets=numberOfSubnets,
                          addressesLeft=addressesLeft,
                          cidrAvailable=cidrAvailable,
                          subnetColors=subnetColors,
                          hostsPerSubnet=recalculatedHosts,
                          base_broadcast=base_broadcast,
                          actual_hosts=hosts)

#Route to subnet-input child
@app.route('/subnet/<base_ip>/<base_cidr>/<hosts>/input')
def show_input():
    return render_template('subnet-input-extend.html')

#Route to the subnet-output child
@app.route('/subnet/<base_ip>/<base_cidr>/<hosts>/output')
def show_output(base_ip,base_cidr,hostsPerSubnet):
    # Call subnetter functions to generate subnets    
    generatedSubnets = CalculateSubnets(base_ip, base_cidr, hostsPerSubnet)
   
    numberOfSubnets = len(generatedSubnets)
    return render_template('subnet-output-extend.html',
                    generatedSubnets=generatedSubnets,
                    numberOfSubnets=numberOfSubnets)

if __name__ == "__main__":
    app.run(debug=True)
