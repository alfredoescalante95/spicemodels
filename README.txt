---------------------------     spicemodels     -------------------------------

This python packages transforms from wavefront .OBJ files to Spice .BDS (DSK, 
Digital Shape model Kernel). In order to use the package just import it and 
use one of the functions:
	
	- spicemodels.obj2dsk()
	- spicemodels.dsk2obj()
	
The required inputs will be asked in the console. Please be careful 
introducing the required kernels and files with its corresponding path. 
	
-------------------   obj2dsk example   ------------------------

This is an example run in python console with BepiColombo:

	>>> import spicemodels
	>>> spicemodels.obj2dsk()
	Introduce .OBJ file to process: bepi_mcs.obj
	Introduce x displacement (int): 0
	Introduce y displacement (int): 0
	Introduce z displacement (int): 0
	number of vertex:  562623
	number of facets:  263617
	vertex-facet input file created for DSK generation
	Processing of OBJ file successful!!
	creating setup file for DSK generation
	Introduce path for Leapseconds kernel: naif0012.tls
	Introduce path for Frames kernel: bc_mpo_v18.tf
	Introduce path for generated DSK: bepi.bds
	Introduce the following parameters:
	- Surface name: 1
	- Center name: MPO
	- Body reference frame: MPO_SPACECRAFT
	- Units of distance of OBJ file: CENTIMETERS
	- Naif Surface Name: BEPI_1
	- Naif Surface Code: 1
	- Naif Surface Body (float): -121
	setup file created successfully!!
	creating DSK file
	Please, to finish introduce: setup.txt
	
	MKDSK Program; Ver. 2.0.0, 28-FEB-2017; Toolkit Ver. N0066
	
	SETUP FILE NAME> setup.txt
	Reading plate model input file...
	...Done reading plate model input file.
	
	Generating Spatial Index...
	Segregating and closing DSK file...
	DSK file was created.
	
	All done.
	
	Return code 0
	Process finished.
	
-------------------   dsk2obj example   ------------------------

This is an example run in python console with BepiColombo:

	>>> import spicemodels
	>>> spicemodels.dsk2obj()
	Introduce input file name: bepi.bds
	Introduce output file name: bepi.obj
	Factor to dimension the displayed model: 1000
	
	Input DSK:        bepi.bds
	Output text file: bepi.obj
	Output format:    obj
	
	
	Processing segment 1
	Segment is type 2
	Number of vertices: 299006
	Number of plates:   263617
	Reading vertices...
		Reading plates...
		Writing output file bepi.obj
		Writing vertices...
		Writing plates...
		Finished writing output file bepi.obj
		
		
		