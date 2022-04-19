## Description
The program illustrates the gas engine cycle and calculates its efficiency coefficient and information of all specified processes.

Input:
There will be shown a window of the app.
By providing:
- number of degrees of freedom
- Information of the cycle graph - for every point state:
	-  its coordinates in (p in pascals, V in m^3) 
	- type of process that point's starting:
		- l - straight line
		- c - hyperbolic curve
		- a - adiabatic curve

The program will show information about all specified processes (an energy change), efficiency of the cycle.

## Depedencies
- matplotlib 3.3.4
- PyQt5
- scipy
- numpy 1.20.1

Can be transformed into executable with fbs compiler.
