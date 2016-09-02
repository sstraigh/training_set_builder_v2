#!/usr/bin/python

import math

def mass_lookup(atom_label):

  if (atom_label == "O"):
    return 15.9994
  if (atom_label == "H"):
    return 1.00794
  if (atom_label == "N"):
    return 14.0067
  if (atom_label == "Cl"):
    return 35.453
  if (atom_label == "F"):
    return 18.9984
  if (atom_label == "Br"):
    return 79.904
  if (atom_label == "I"):
    return 126.90447
  if (atom_label == "C"):
    return 12.0107
  return "N/A"

def get_masses(geometry_object):

  num_atoms = int(geometry_object[0])

  atomic_masses = []

  for i in xrange(0, num_atoms):
    atom_label = geometry_object[i+2].split()[0]
    atom_mass = mass_lookup(atom_label)
    atomic_masses.append(atom_mass)

  return atomic_masses

def cart_displacements(normal_modes, geometry_object, num_nm):

  '''
    Purpose is to convert the provided mass-weighted normal modes to 
    cartesian displacement vectors
  '''

  cartesian_displacements = []

  object_masses = get_masses(geometry_object)
  
  for n in xrange(0, num_nm):
    cart_disp_nm = []
    for i in xrange(0, len(object_masses)):
      for j in xrange(0, 3):
        cart_disp = normal_modes[(n*len(object_masses)*3) + (3*i + j)] / math.sqrt(object_masses[i]) 
        cart_disp_nm.append(cart_disp)

    # the following can *certainly* be optimized...

    norm = 0
    for i in xrange(0, len(cart_disp_nm)):
      norm += (cart_disp_nm[i] * cart_disp_nm[i])
    for i in xrange(0, len(cart_disp_nm)):
      cart_disp_nm[i] /= math.sqrt(norm)
   
    for i in xrange(0, len(cart_disp_nm)): 
      cartesian_displacements.append(cart_disp_nm[i])

  return cartesian_displacements

