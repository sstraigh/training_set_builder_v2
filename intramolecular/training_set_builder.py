#!/usr/bin/python

import nm_tools
import molpro_tools
import geometric_tools
import numpy as np
import sys

'''
  Purpose: Generate a sequence of xyz configurations for a given molecule
  
  Input: Molpro output from normal modes/optimization calculation 
         Also maximum number of combined vectors, num_points to scan along each nm

  Output: Single xyz trajectory file containing linear combinations of the
          normal modes
'''


if (len(sys.argv) < 4):
  print "Usage: ./training_set_builder.py Num_Vects Molpro_ouput Num_points > STDOUT"
  sys.exit()

# Read in number of points sampled along each normal mode

num_points = int(sys.argv[3])

# Read in number of normal modes to couple

num_coupled_nm = int(sys.argv[1])

# extract optimized geometry and mass weighted normal modes from
# molpro file

eq_geometry, mass_weighted_nm, num_nm = molpro_tools.read_molpro_output(sys.argv[2])

cart_displacements = mass_weighted_nm
#cart_displacements = nm_tools.cart_displacements(mass_weighted_nm, eq_geometry, num_nm)

training_set = geometric_tools.generate_configurations(num_coupled_nm, cart_displacements, \
                                                       eq_geometry, num_points, num_nm)

# print training set to STDOUT

count = 0
for configuration in training_set:
  count = count + 1
  print eq_geometry[0].split()[0] # this is the number of atoms
  print "configuration #: ", count
  geometric_tools.print_config(configuration, eq_geometry)
