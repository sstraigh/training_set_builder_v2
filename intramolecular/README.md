Training set builder comprises a sequence of scripts designed to
read the output of a molpro calculation (opt, frequencies), extract
the optimized geometry and normal modes, then use linear combinations
of the cartesion displacement vectors from these normal modes to
build a complete set of configurations which span the relavant
portions of the potential energy surface the permutationally 
invariant polynomials are designed to capture.

Training_set_builder.py contains the main routine. 
NM_tools.py contains the functions responsible for mathematical
  transformations on the normal mode vectors
Geometry_tools.py contains the configuration builder routines
  and the instructions for formatting the xyz printing of the
  configurations
molpro_tools.py contains the functions responsible for extracting
  data from the molpro calculation
