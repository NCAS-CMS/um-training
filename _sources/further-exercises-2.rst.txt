Further Exercises (2)
=====================

The exercises in this section are all optional.  We suggest you pick and choose the exercises that you feel are most relevant to the work you are/will be doing.

.. note:: Use your copy of suite u-ba799 for these exercises unless otherwise specified.

Post-Processing (archive and transfer of model data)
----------------------------------------------------

When your model runs it outputs data onto the Archer ``/work`` disk (``/projects`` on Monsoon/NEXCS). If you are running a long integration and/or at high resolution data will mount up very quickly and you will need to move it either to the ARCHER RDF or JASMIN.  The post-processing app (postproc) is used within cycling suites to automatically archive model data and can be optionally configured to transfer the data from the RDF to JASMIN data facility.  The app archives and deletes model output files, not only for the UM, but also NEMO and CICE in coupled configurations.

Let's try configuring your suite to archive to the RDF:

* Switch on post-processsing in window *suite conf -> Tasks*

The post-processing is configured under the **postproc** section:

* Select the "Archer archiving system" in window *Post Processing - common settings*.

A couple of new entries will have appeared in the index panel, *Archer Archiving* and *JASMIN Transfer*, identified with the blue dots.

You now need to specify where you want your archived data to be copied to:

* In the *Archer Archiving* panel set ``archive_root_dir`` to be **/nerc/n02/n02/<userid>**.  The *archive_name* (suite id) will be automatically appended to this.  

You will need to run the model for at least 1 day as archiving doesn't work for periods of less than 1 day.  Change the *"run length"* and *"cycling frequency"* to be 1 day.  This should complete in about 5 minutes so set the *"wallclock time"* to be 10 minutes. 

**Run** the suite.

Once the run has completed go to the archive directory for this cycle (e.g. ``/nerc/n02/n02/<userid>/<suiteid>/19880901T0000Z``) and you should see several files have been copied over (e.g ``ba902a.pc19880901_00.pp``).  Data is only archived when it is no longer required by the model for restarting or for calculating means (seasonal, annual, etc). This run is reinitialising the ``pc`` data stream every 4 hours and you should see that it has only archived data files up to 16:00hrs (ba902a.pc19880901_16.pp).  The last file containing data for hours 20-24 is still required by the model. Equally seasonal mean files would not be archived until the end of the year, after the annual mean has been created.

.. note:: The post-processing app can also be configured to transfer the archived data over to JASMIN.  Details on how to do this are available on the CMS website: http://cms.ncas.ac.uk/wiki/Docs/PostProcessingApp

Using IO Servers
----------------

Older versions of the UM did not have IO servers, which meant that all reading and writing of fields files went through a single processor (pe0).  When the model is producing lots of data and is running on many processors, this method of IO is very inefficient and costly - when pe0 is writing data, all the other processors have to wait around doing nothing but still consuming AUs.  Later UM versions, including UM 10.5, have IO servers which are processors dedicated to performing IO and which work asynchronously with processors doing the computation.

Here's just a taste of how to get this working in your suite.

Set the suite to run for 6 hours with an appropriate cycling frequency, then check that OpenMP is switched on (Hint: search for *openmp* in rose edit) as this is needed for the IO servers to work.

Navigate to *suite conf -> Domain Decomposition -> Atmosphere* and check the number of OpenMP threads is set to 2. Set the number of *"IO Server Processes"* to 8.

**Save** and then **Run** the suite.

You will see lots of IO server log files in ``~/cylc-run/<suitename>/work/<cycle>/atmos_main`` which can be ignored for the most part.

Try repeating the "Change dump frequency" experiment with the IO servers switched on - you should see much faster performance.

Writing NetCDF output from the UM
---------------------------------

Until UM vn10.9, only fields-file output was available from the UM - bespoke NetCDF output configurations did exist but not on the UM trunk. The suite used in most of these Section 7 exercises is vn11.0, hence supports both fields-file and NetCDF output data formats.

**i. Enable NetCDF**

Make sure that **IO Server Processes** is set to 0.

Navigate to *um -> namelist -> Model Input and Output -> NetCDF Output Options* and set ``l_netcdf`` to true. Several fields will appear which allow you to configure various NetCDF options.  For this exercise, leave them at their chosen values.

**ii. Set NetCDF Output Streams**

Expand the *NetCDF Output Streams* section. A single stream - **nc0** - already exists; select it to display its content. As a useful comaprison, expand the *Model Output Streams* section and with the middle mouse button select **pp0**. Observe that the only significant differences between **pp0** and **nc0** are the values of ``file_id`` and ``filename_base``.  Data compression options for **nc0** are revealed if ``l_compress`` is set to true. NetCDF deflation is a computationally expensive process best handled asynchronously to computation and as yet not fully implemented through the UM IO Server scheme (but under active development.) For many low- to medium-resolution models and, depending precisely on output profiles, high-resolution models also, use of UM-NetCDF without IO servers still provides significant benefits over fields-file output since using it avoids the need for subsequent file format conversion.

Right-click on **nc0** and select *Clone this section*. Edit the settings of the newly cloned section appropriately to make the new stream similar to **pp1** (ie. edit ``filename_base`` and all the reinitialisation variables). It is sensible to change the name of the new stream from "1" to something more meaningful, nc1 for example (right click on "1", select *Rename a section*, and change ...nc(1) to ...nc (nc1)).

**iii. Direct output to the nc streams**

Expand *STASH Requests and Profiles*, then expand *Usage Profiles*. Assign nc streams to usage profiles - in this suite, UPA and UPB are assigned to **pp0** and **pp1** respectively (where can you see this?). Edit these Usage profiles to refer to **nc0** and **nc1** respectively. Run the STASH Macros (if you need a reminder see Section 6), save the changes, and run the suite. Check that the NetCDF output is what you expected.

Try adding more nc streams to mimic the pp stream behaviour.

Running the coupled model
-------------------------

The coupled model consists of the UM Atmosphere model coupled to the NEMO ocean and CICE sea ice models.  The coupled configuration used for this exercise is N96 resolution for the atmosphere and a 1 degree ocean - you will see this written N96 ORCA1.

**i. Checkout and run the suite**

Checkout and open the suite **u-ak943**.  The first difference you should see is in the naming of the apps; there is a separate build app for the um and ocean, called *fcm_make_um* and *fcm_make_ocean* respectively. The model configuration is under *coupled* rather than *um*.

Make the usual changes required to run the suite (i.e. set username, account code, queue)

Check that the suite is set to build both the UM and ocean, as well as run the reconfiguration and model.

**Run** the suite.

**ii. Exploring the suite**

Whilst the suite is compiling and running which will take around 45 minutes, take some time to look around the suite.

* How many nodes is the atmosphere running on?
* How many nodes is the ocean running on?

Changing the processor decomposition for the ocean is not as simple as just changing the EW/NS processes.  You also need to:

1. Recalculate the CICE number of columns per block EW and rows per block NS. (Normally the model is set up so that NEMO and CICE use the same decomposition). Looking at the current settings we calculate as follows:

  Num of cols per block EW = Num of cols EW / Num of processes EW (E.g. 360 / 9 = 40)

  Num of rows per block NS = Num of rows NS / Num of processes NS (E.g. 330 / 8 = 42) 

2. Recompile the ocean executable. Note the executable comprises both the ocean (NEMO) and sea-ice (CICE) code. 

Now looked at the ``coupled`` settings.   

* Can you see where the NEMO model settings appear? 

Look under *Run settings (namrun)*. The variables ``nn_stock`` and ``nn_write`` control the frequency of output files. 

* How often are NEMO restart files written? (Hint the NEMO timestep length is set as variable ``rn_rdt``).

Now browse the CICE settings.

* Can you find what the CICE restart frequency is set to? 

NEMO and CICE are developed separately from the UM, and you should have seen that they work in very different ways. See the websites for documentation: 

* http://oceans11.lanl.gov/trac/CICE 
* http://www.nemo-ocean.eu/

**iii. Output files**

**Log files** 

NEMO logging information is written to:

 ``~/cylc-run/<suitename>/work/<cycle>/coupled/ocean.output``

CICE logging information is written to: 

 ``~/cylc-run/<suitename>/work/<cycle>/coupled/ice_diag.d``

If the model fails some error messages may also be written to the file ``~/cylc-run/<suitename>/work/<cycle>/coupled/debug.root.01`` or ``debug.root.02``

When something goes wrong with the coupled model it can be tricky to work out what has gone wrong. NEMO errors may not appear at the end of the file but will be flagged with the string ``E R R O R``. 

**Restart files** 

Restart files go to the subdirectories ``NEMOhist`` and ``CICEhist`` in the standard data directory ``~/cylc-run/<suitename>/share/data/History_Data``.

**Diagnostic files**

Diagnostic files are left in the ``~/cylc-run/<suitename>/work/<cycle>/coupled/`` directory. 

CICE files start with ``<suitename>i``. Once your suite has run you should see the following CICE file: :: 

  archer$ ls ak943i*
  ak943i.10d.1978-09-10.nc

NEMO diagnostic files are named ``<suitename>o*grid_[TUVW]*``. To see what files are produced, run: :: 

  archer$ ls ak943o*grid*

In this case each processor writes to a separate file. To concatenate these into a global file use the ``rebuild_nemo`` tool, e.g.: :: 

  archer$ rebuild_nemo ak943o_10d_19780901_19780910_grid_W_19780901-19780910 72

Higher resolution NEMO suites may use the XIOS IO server. In this case, global files may be written directly, or each server process may write its own file. 
  
.. note:: The coupled atmos-ocean model setup is complex so we recommend you find a suite already setup for your needs.  If you find you do need to modify a coupled suite setup please contact NCAS-CMS for advice. 

Running the Nesting Suite
-------------------------

The Nesting Suite drives a series of nested limited area models (LAM)
from a global model.  It allows the user to specify the domains and it
then automatically creates the required ancillary files and lateral
boundary condition files.

**i. Checkout and run the suite**

Checkout and open the suite **u-ba621**. There are a number of tasks for
creating ancillary files (*ancil_** and *ants_**).  The global model set
up is in *glm_um* and the LAMs are in *um*.  The task *um-createbc* creates
the lateral boundary condition files.

Under *suite conf -> jinja2:suite.rc* are the main panels for
controlling the Nesting Suite. Make the usual changes required to run
the suite (i.e. set username, account code, queue). The training
nesting suite has pre-built executables so you don't have to spend
time building it.  **Run** the suite.

This particular suite has a global model and one limited area model.
It should complete in about 45 - 60 minutes.

**ii. Exploring the Suite**

The Driving Model set up panel allows the user to specify the
resolution of the global model and the number of nested regions.

The *Nested Region 1* set up panel specifies the latitude and longitude
of the centre of the first nested region.  All the other limited area
models have the same centre.

A useful way to get this information is to use Google Maps.  Find the
place you want as a centre and then press ``control-left mouse`` and a
little window with the latitude and longitude appears.

 * Can you find out where the first LAM is located?  Hint: look at the orography file output during the ancillary creation.

The *resolution 1* set up panel specifies the grid and the run length.

The *Config 1* set up panel specifies the science configuration to be
run.  Each LAM can have multiple science configurations.

**iii.  Initial Data**

The initial data for the global model is in ``share/cycle/<cycle time>/glm/ics``

The initial data for the first LAM is in ``share/cycle/<cycle time>/Regn1/resn_1/RA1M/ics``

The RA1M is the name you gave to the first science configuration.

The LBCs for the first LAM are in ``share/cycle/<cycle time>/Regn1/resn_1/RA1M/lbcs``.

**iv. The ancillary files**

These are in ``share/data/ancils/Regn1/resn_1``


**v.  The output files**

The global model output is in ``share/cycle/<cycle time>/glm/um``. This also
contains contains the data for creating the LBC files (umglaa_cb*) for the first LAM.

Diagnostic files can be found under ``work/<cycle time>`` in an application directory.  For
example, the region1 forecast diagnostics is in ``work/<cycle time>/Regn1_resn_1_RA1M_um_fcst_000``.
This will include the pe_output files.

The output for the first LAM is in ``share/cycle/<cycle time>/Regn1/resn_1/RA1M/um``.


**vi. Further Information**

This has been a very brief overview of the functionality of the
Nesting Suite. The Nesting Suite is developed and maintained by Stuart
Webster at the Met Office.  He has a web page all about the Nesting
Suite at https://code.metoffice.gov.uk/trac/rmed/wiki/suites/nesting.
This includes a more detailed tutorial.
