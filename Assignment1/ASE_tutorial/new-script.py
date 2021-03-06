#!/usr/bin/env python

import types
import numpy
import sys
import matplotlib
matplotlib.use("agg") # Change to "agg" to run on FRI
from pylab import *
import tsase
import ase

##### Setting up the atoms object with ASE and TSASE #########
##############################################################

#### Import the starting structure from a file ###############
p = tsase.io.read_con('diatomic.con')

#### Define the PES ##########################################
lj = tsase.calculators.lj(cutoff=3.5)
p.center(50.0)
p.set_calculator(lj)

#############################################################
## INSERT YOUR GRADIENT DESCENT METHOD BELOW ################


def magnitude(v):
    #print "mag: ", v
    mag = numpy.sqrt(numpy.vdot(v,v))
    return mag

def sum(a):
    #print "sum: ", a
    if type(a) is numpy.ndarray:
        ans = 0.0
        for y in a:
            ans += sum(y)
        return ans
    return abs(a)

def optimize(p, nArr, fArr, peArr):
    maxstep = 10000
    count = 0
    forces = p.get_forces()
    mag = magnitude(forces)
    while mag > 0.001 * p.get_number_of_atoms() and count < maxstep:
        count += 1
        pos = p.get_positions();
        mult = .00001
        #mult = 1
        forceSum = sum(forces)
        #print "sum is: ", forceSum
        # print "force sum: ", forceSum
        if (mult*p.get_number_of_atoms()*forceSum>2.0):
            print 'limit to 2 angstroms'
            mult = 2.0 / (p.get_number_of_atoms()*forceSum)
        y = 0
        while y < len(forces):
            i = 0
            while i < len(forces[y]):
                pos[y][i] += mult * forces[y][i]
                i+=1
            y+=1
        p.set_positions(pos)
        forces = p.get_forces()
        #p.set_positions(p.get_positions() + .0001 * p.get_forces())
        mag = magnitude(forces)
        #print "Steps: ", count
        nArr.append(count+1)
        fArr.append(mag)
        peArr.append(p.get_potential_energy())

n = 1
nArr = [1]
fArr = [magnitude(p.get_forces())]
peArr = [magnitude(p.get_potential_energy())]

#print type(p.get_forces())
optimize(p, nArr, fArr, peArr)

print 'Magnitudes:', fArr

print 'potential energy:', p.get_potential_energy()
print 'force:', p.get_forces()
print "Pos: ", p.get_positions()
print "Dist: ", p.get_all_distances()

#print [[1,2],[3,4]]+[[5,6],[7,8]]

############################################################
## KEEP THIS PART AT THE BOTTOM OF YOUR SCRIPT
p = tsase.io.write_con('optimized_diatomic.con',p,w='w') 

# The line above will write out a file called optimized_diatomic.con which is the optimized structure 


figure()
plot(nArr, fArr)
xlabel('Nth Step')
ylabel('Force Magnitude')
title('Forces over steps')
yscale('log')
savefig('LJ38f.png')

figure()
plot(nArr, peArr)
xlabel('Nth Step')
ylabel('Potential Energy')
title('Potential Energy over steps')
#yscale('log')
savefig('LJ38pe.png')

sys.exit()
