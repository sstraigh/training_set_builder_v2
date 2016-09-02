#!/usr/bin/python

import itertools
import numpy as np

def print_config(xyz_data, geometry_object):
  '''
    Routine to print a formatted xyz file output from a list
    containing xyz floating point information

    Requires reference geometry to determine appropriate
    atomic labels
  '''
  
  num_atoms = len(xyz_data) / 3
  for i in xrange(0, num_atoms):
    position_string = '%-3s' % geometry_object[2 + i].split()[0]
    for j in xrange(0, 3):
      position_string += '%20.15f' % xyz_data[i*3 + j]
    print position_string

  return

def generate_configurations(num_combined_nm, cart_displacements, eq_geometry, num_points, num_nm):

  num_atoms = int(eq_geometry[0])

  # xyz_config holds the equilibrium xyz geometry of 3N coordinates
  xyz_config = []
  for i in xrange(0, num_atoms):
    for j in xrange(0,3):
      xyz_config.append(float(eq_geometry[2 + i].split()[1 + j]))

  # initialize container storing labels of possible basis vectors
  # used to create linear combinations of cartesian displacements
  # to sample the nm space

  nm_indices = []
  for i in xrange(0, num_nm):
    nm_indices.append(i)

  # basis_vects is a list containing every unique combination of normal modes
  # up to the user-specified order defining the distortion of the eq geometry

  basis_vects = list(itertools.combinations(nm_indices, num_combined_nm))

  # coefficient list contains all possible distortions of the nm's chosen as
  # a basis vector for this system

  coefficient_list = []
  num_distortions = np.power(num_points, num_combined_nm)

  for i in xrange(0, num_distortions):
    # each possible distortion is a different combination of the incremental
    # changes along each basis vector
    coeffs = np.zeros(num_combined_nm)
    for j in xrange(0, num_combined_nm):
      index = (i / np.power(num_points, j)) % num_points
      coeffs[j] = 0.3 * ((index - (num_points / 2.0)) / (num_points / 2.0))
    coefficient_list.append(coeffs)

  # for every basis set combo, run all coefficient possibilities, generate
  # distorted structure

  config_list = []

  for basis_combo in basis_vects:
    for coeff_combo in coefficient_list:
      distortion_vector = np.zeros(len(xyz_config)).tolist()
      for i in xrange(0, num_combined_nm):
        for j in xrange(0, len(xyz_config)):
          distortion_vector[j] += cart_displacements[basis_combo[i]*num_atoms*3 + j] * coeff_combo[i]

      distorted_config = np.zeros(len(xyz_config)).tolist()
      for i in xrange(0, len(xyz_config)):
        distorted_config[i] = (xyz_config[i] + distortion_vector[i])

      config_list.append(distorted_config)

  return config_list
