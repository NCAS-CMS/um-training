Post processing
===============

This is simply a very basic introduction to some of the more widely used useful tools for viewing, checking, and converting UM input and output data. The tools described below all run on the ARCHER2 login nodes.

xconv
-----

**i. View data**

On ARCHER2 go to the output directory of the global job that you ran previously (the one copied from u-cc654). Run ``xconv`` on the file ending with, for example, ``da19880901_04``. This file is an atmosphere start file - this type of file is used to restart the model from the time specified in the file header data.

In the same directory is a file whose name ends in ``.astart``; run a second instance of ``xconv`` on this file. This is the file used by the model to start its run - created by the reconfiguration program in this case.

The ``xconv`` window lists the fields in the file, the dimensions of those fields (upper left panel), the coordinates of the grid underlying the data, the time(s) of the data (upper right panel), some information about the type of file (lower left panel), and general data about the field (lower right panel.)

Both files have the same fields. Double click on a field to reveal its coordinate data. Check the time for this field (select the "t" checkbox in the upper right panel).

Plot both sets of data - click the :guilabel:`Plot Data` button.

View the data - this shows numerical data values and their coordinates and can be helpful for finding spurious data values.

**ii. Convert UM fields data to netCDF**

Select a single-level field (one for which nz=1), choose :guilabel:`Output format` to be :guilabel:`Netcdf`, enter an "Output file name", and select :guilabel:`Convert`. Information relevant to the file conversion will appear in the lower left panel.

Use ``xconv`` to view the netcdf file just created.

uminfo
------

You can view the header information for the fields in a UM file by using the utility ``uminfo`` - redirect the output to a file or pipe it to ``less``: :: 

  archer$ uminfo <one-of-your-fields-files> | less

The output from this command is best viewed in conjunction with the Unified Model Documentation Paper F3 which explains in depth the various header fields.

Mule
----

Mule consists of a Python API for reading and writing UM files and a set of UM utilities.  This section introduces you to some of the most useful UM utilities.  Full details of Mule can be found on the MOSRS: https://code.metoffice.gov.uk/doc/um/index.html

Before running the mule commands you will need to load the python environment on ARCHER2 by running: ::

  archer$ module load cray-python

**i. mule-pumf**

This provides another way of seeing header information, but also gives some information about the fields themselves. Its intended use is to aid in quick inspections of files for diagnostic purposes. 

Run ``mule-pumf`` on the start file - here's a couple of examples on one of Ros' files: :: 

 archer$ mule-pumf --print-columns 2 --headers-only \\
                        cc654.astart > ~/mule-pumf-header.out

 archer$ mule-pumf --print-columns 2 cc654.astart > ~/mule-pumf.out

* Can you see what the difference is in the output of these 2 commands?

Take a look at the man page (``mule-pumf -h``) and experiment with some of the other options

**ii. mule-summary**

This utility is used to print out a summary of the lookup headers which describe the fields from a UM file. Its intended use is to aid in quick inspections of files for diagnostic purposes.

Run ``mule-summary`` on the start file again.

**iii. mule-cumf**

This utility is used to compare two UM files and report on any differences found in either the headers or field data. Its intended use is to test results from different UM runs against each other to investigate possible changes. Note, differences in header information can arise even when field data is identical. Try out the following:

* Run ``mule-cumf`` on the two start files referred to above (in the *"View data"* section). You may wish to direct the output to a file.
* Run the same command but with the ``--summary`` option.  This, as the name suggests, prints a much shorter report of the differences.
* Run ``mule-cumf`` on a file and itself.
* View the help page with ``mule-cumf -h`` to find view all the available options. 

um-convpp
---------

We have mentioned in the presentations the PP file format - this is a sequential format (a fields file is random access) still much used in the community. PP data is stored as 32-bit, which provides a significant saving of space, but means that a conversion step is required from a fields file (64-bit). The utility to do this is called ``um-convpp``.  ``um-convpp`` converts directly from 64-bit files produced by the UM to 32-bit PP files.  You must, however, make sure you are using a version 10.4 or greater - you can check that you are using the right one by typing ``which um-convpp``. 

Set the stack size limit to unlimited, and add the path to ``um-convpp`` to your environment - you can also add this to your ``~/.profile`` so it is available everytime you log in. ::

  archer$ ulimit -s unlimited
  archer$ export PATH=$UMDIR/vn11.2/cce/utilities:$PATH

Run ``um-convpp`` on a fieldsfile (E.g `cc654a.pc19880901_00`) ::

  archer$ cd /home/n02/n02/ros/cylc-run/u-cc654/share/data/History_Data
  archer$ um-convpp cc654a.pc19880901_00 cc654a.pc19880901_00.pp

  archer$ ls -l cc654a.pc19880901*
  -rw-r--r-- 1 ros n02 64917504 Mar 15 11:56 ag761a.pc19880901_00
  -rw-r--r-- 1 ros n02 48581456 Mar 21 10:19 ag761a.pc19880901_00.pp

Note the reduction in file size. Now use xconv to examine the contents of the PP file.

cfa
---

There is an increasing use of python in the community and we have, and
continue to develop, python tools to do much of the data processing
previously done using IDL or MATLAB and are working to extend that
functionality. ``cfa`` is a python utility which offers a host of
features - we'll use it to convert UM fields file or PP data to
CF-compliant data in NetCDF format. You first need to set the
environment to run ``cfa``: ::

 archer$ export PATH=/home/n02/n02/dch/cf/bin:$PATH
 archer$ cfa -i -o cc654a.pc19880901_00.nc cc654a.pc19880901_00.pp
 
Try viewing the NetCDF file with xconv.


``cfa`` can also view CF fields. It can be run on PP or NetCDF
files, to provide a text representation of the CF fields contained in
the input files. Try it on a PP file and its NetCDF equivalent,
e.g. ::

  archer$ cfa -vm cc654a.pc19880901_00.pp | less
  Field: long_name:HEAVYSIDE FN ON P LEV/UV GRID (ncvar%UM_m01s30i301_vn1100)
  ---------------------------------------------------------------------------
  Data           : long_name:HEAVYSIDE FN ON P LEV/UV GRID(time(5), air_pressure(17), latitude(145), longitude(192)) 
  Cell methods   : time: point
  Axes           : time(5) = [1988-09-01T00:00:00Z, ..., 1988-09-01T03:59:59Z] 360_day
                 : air_pressure(17) = [1000.0, ..., 10.0] hPa
                 : latitude(145) = [-90.0, ..., 90.0] degrees_north
                 : longitude(192) = [0.0, ..., 358.125] degrees_east

  Field: long_name:VORTICITY 850 (ncvar%UM_m01s30i455_vn1100)
  -----------------------------------------------------------
  Data           : long_name:VORTICITY 850(time(5), latitude(145), longitude(192)) 
  Cell methods   : time: point
  Axes           : air_pressure(1) = [-1.0] hPa
                 : time(5) = [1988-09-01T00:00:00Z, ..., 1988-09-01T03:59:59Z] 360_day
                 : latitude(145) = [-90.0, ..., 90.0] degrees_north
                 : longitude(192) = [0.0, ..., 358.125] degrees_east

CF-python CF-plot
-----------------

Many tools exist for analysing data from NWP and climate models and there are many contributing factors for the proliferation of these analysis utilities, for example, the disparity of data formats used by the authors of the models, and/or the availability of the underlying sofware. There is a strong push towards developing and using python as the underlying language and CF-netCDF as the data format. CMS is home to tools in the CF-netCDF stable - here's an example of the use of these tools to perform some quite complex data manipulations. The user is insulated from virtually all of the details of the methods allowing them to concentrate on scientific analysis rather than programming intricacies.

* Set up the environment and start python. ::

   
   archer$ export PATH=/home/n02/n02/dch/cf/bin:$PATH
   archer$ python
   >>>

We'll be looking at CRU observed precipitation data.

* Import the cf-python library ::

  >>> import cf

* Read in data files ::

  >>> f = cf.read('~dch/UM_Training/cru/*.nc')[0]

* Inspect the file contents with different amounts of detail ::

  >>> f
  >>> print(f)
  >>> f.dump()
  
Note that the two files in the cru directory are aggregated into one
field.

* Read in another field produced by a GCM, this has a different
  latitude/longitude grid to regrid the CRU data to ::

  >>> g = cf.read('~dch/UM_Training/N96_DJF_precip_means.nc')[0]
  >>> print(g)

* Regrid the field of observed data, ``f`` to the grid of the model
  field (g) ::

  >>> f = f.regrids(g, method='linear')
  >>> print(f)

* Average the regridded field with respect to time ::

  >>> f = f.collapse('T: mean')
  >>> print(f)

Note that the time axis is now of length 1.

* Subspace the regridded field to a European region ::

  >>> f = f.subspace(X=cf.wi(-10, 40), Y=cf.wi(35, 70))
  >>> print(f)

Note that the latitude and longitude axes are now shorter in length.

* Import the cfplot visualisation library ::

  >>> import cfplot

* Make a default contour plot of the regridded observed data, ``f`` ::

   >>> cfplot.con(f)

* Make a "blockfill" plot of the regridded observed data, ``f`` ::

   >>> cfplot.con(f, blockfill=True)

* Make a default contour plot of the model data, ``g`` ::

   >>> cfplot.con(g)
   
* Make a "blockfill" plot of the model data, ``g``, over the
  same region ::

   >>> g = g.subspace(X=cf.wi(-10, 40), Y=cf.wi(35, 70))
   >>> cfplot.con(g, blockfill=True)
   
* Write out the new field f to disk ::

  >>> cf.write(f, 'cru_precip_european_mean_regridded.nc')

This has just given you a taster of CF-Python & CF-Plot, if you would like to try out some more exercises please take a look at https://github.com/NCAS-CMS/cf-training

