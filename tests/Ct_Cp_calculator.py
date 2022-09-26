# Ct and Cp calculator

## Input
# chord length of blade assumed costant with radius
from array import array
from cProfile import label
from calendar import c
from math import atan, cos, e, pi, sin, sqrt
from math import atan2
import matplotlib.pyplot as plt
import numpy as np

chord = 0.10
# pitch distance in meters
pitch = 1.0
# diameter of propeller in meters
dia = 1.6
# tip radius
R = dia / 2.0
# engine speed
RPM = 2100
# thickness to chord ratio for propelle section (costant with radius)
tonc = 0.12 * chord
# standard sea level atmosphere density
rho = 1.225
# RPM --> revs
n = RPM/60
# rps --> rads per second
omega = n * 2.0 * pi
# n blade propeller
B = 2
# use 10 blade segments (starting a 10%R to R)
xs = 0.1*R
xt = R
rstep = (xt-xs)/10
r1 = np.arange(xs,(xt+0.01),rstep)

# initializations
t = np.array([])
q = np.array([])
J = np.array([])
eff = np.array([])
V = np.array([])
Vax = np.array([])
## Calculation

# velocity step
for V in range(1,61):
    thrust = 0.0
    torque = 0.0
    for j in range(len(r1+1)):
        rad = r1[j]
        # calculate local blade element setting angle
        theta = atan(pitch/2/pi/rad)
        # calculate solidity
        sigma = 2 * chord / 2 / pi / rad
        # guess initial value of inflow and swirl factor
        a = 0.1
        b = 0.01
        # set logical variable to control iteration
        finished = False
        # set iteration count and check flag
        sum = 1
        while not finished:
            # axial velocity
            V0 = V * (1 +  a)
            # disk plane velocity
            V2 = omega * rad *(1 - b)
            # flow angle
            phi = atan2(float(V0), float(V2))
            # blade angle of attack
            alpha = theta - phi
            # lift coefficient
            cl = 6.2 * alpha
            # drag coefficient
            cd = 0.008 - 0.003 * cl + 0.01 * cl**2
            # local velocity at blade
            Vlocal = sqrt(V0**2 + V2**2)
            # thrust grading 
            DtDr = 0.5*rho*Vlocal**2*B*chord*(cl*cos(phi)-cd*sin(phi))
            # torque grading 
            DqDr = 0.5*rho*Vlocal**2*B*chord*rad*(cd*cos(phi)+cl*sin(phi))
            # momentum check on inflow and swirl factors
            tem1 = DtDr/(4*pi*rad*rho*V**2*(1+a))
            tem2 = DqDr/(4*pi*rad**3*rho*V*(1+a)*omega)
            # stabilise iteration 
            anew = 0.5*(a+tem1)
            bnew = 0.5*(b+tem2)
            
            # check for convergence
            if (abs(anew-a)<1e-5):
                if(abs(bnew-b)<1e-5):
                    finished == True
            
            a = anew
            b = bnew

            # increment iteration count
            sum = sum + 1
            # check to see if iteration stuck
            if (sum>500):
                finished = True

        thrust = thrust + DtDr * rstep
        torque = torque + DqDr * rstep
        finished = True

    t=np.append(t,thrust/(rho*n**2*dia**4))
    q=np.append(q,torque/(rho*n**2*dia**5))
    J=np.append(J, V/(n*dia)) 
eff=np.append(eff, J/2.0/pi*t/q)

Jmax=max(J) 
Tmax=max(t) 

plt.plot(J,t, label='Ct')
plt.plot(J,q,label='Cq')
plt.xlim(0, Jmax) 
plt.ylim(0, 1.1*Tmax)

plt.title('Thrust and Torque Coefficients')
plt.xlabel('Advance Ratio (J)')
plt.ylabel('Ct, Cq')
plt.legend()
plt.show()

plt.plot(J,eff)
plt.title('Propeller Efficiency')
plt.xlabel('Advance Ratio (J)')
plt.ylabel('Efficiency')
plt.xlim(0, Jmax) 
plt.ylim(0, 1)
plt.show()