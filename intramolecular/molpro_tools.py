#!/usr/bin/python

def find_molpro_mode(mode_index, filename, num_normal_modes):
  '''
    Returns the ith normal mode of the system
  '''

  nm_flag = 0

  # molpro prints normal modes in blocks of 5, so we must keep track of which
  # block the normal mode we want is in

  nm_block_index = int(mode_index / 5)

  ith_normal_mode = []
  with open(filename, 'r') as f:
    for line in f:

      if (nm_block_index == (nm_flag - 1)):
        if (line.split() and line.split()[0][0] == "G"):
          ith_normal_mode.append(line.split()[(mode_index % 5) + 1])

      # Start looking for the normal mode coordinates in block nm_flag+1 if true
      if (line.split() and line.split()[0] == "Wavenumbers"):
        nm_flag = nm_flag + 1
          
  return ith_normal_mode

def find_molpro_nm(filename, num_nm):
  '''
   return the normal modes from the molpro output
  '''
  normal_mode_matrix = []

  for i in xrange(0, num_nm):
    next_mode = find_molpro_mode(i, filename, num_nm)
    for value in next_mode:
      normal_mode_matrix.append(float(value))

  return normal_mode_matrix

def find_molpro_eq_geometry(filename):
  '''
    return the optimized geometry from molpro calculation
  '''
  geo_flag = 0
  geometry_object = []
  line_counter = 0

  file_contents = open(filename).readlines()

  for line in file_contents:

    if (geo_flag == 1):
      if (line_counter == 1): 
        num_atoms = int(line.split()[0])

      if (line_counter > 0 and line_counter <= (2 + num_atoms)): 
        geometry_object.append(line)

      line_counter = line_counter + 1

    if (line.split() and line.split()[0] == "Current"):
      geo_flag = 1

  return geometry_object

def find_num_normal_modes(filename):

  num_normal_modes = 0
  nm_flag = 0
  nr_flag = 0

  file_contents = open(filename).readlines()

  for line in file_contents:
    if (line == '\n'):
      nm_flag = 0
      nr_flag = 0
    if (nm_flag == 1 and int(line.split()[0]) and float(line.split()[1])):
      num_normal_modes += 1
    if (line.split() and line.split()[0] == "Vibration"):
      nr_flag = 1
    if (nr_flag == 1 and line.split()[0] == "Nr"):
      nm_flag = 1

  return num_normal_modes

def read_molpro_output(filename):
  
  '''
    Purpose is to read the molpro output file and read in the equilibrium
    geometry and mass-weighted normal mode vectors
  '''

  equilibrium_geometry = find_molpro_eq_geometry(filename)
  num_modes = find_num_normal_modes(filename)
  mass_weighted_normal_modes = find_molpro_nm(filename, num_modes)

  return equilibrium_geometry, mass_weighted_normal_modes, num_modes

