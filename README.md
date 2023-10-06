# Subnetting Calculator
## Course project
### CS202.2 Research Proposal
This is part of CS202.2 Research Proposal, which will be used as a proof of concept and codebase for CS203.2 Team Prototype and Report.

The script is a subnetting calculator which takes a base network adress and mask, and divides it into smaller subnets. The user can input different sized subnets and these will then be organized by size and validated (including against the range to make sure the subnets do not stray outside of the supplied range).

## Guide
### Base network
#### Enter your base network address
This should be in the format of x.x.x.x (i.e., 10.0.0.0, 172.16.0.0, etc)
#### Enter your base network mask
This should be in CIDR format, x (i.e., 24, 25, 16, etc)
### Subnets
#### Number of hosts
Enter the number of hosts you want for the corresponding subnet (up to the max supported number of hosts which is displayed for each subnet).