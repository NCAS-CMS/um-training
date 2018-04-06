Working with Suites
===================

Suite Discovery and Management: rosie go
----------------------------------------

**Rosie go** is the suite manager GUI. It acts as a hub for all your suite work. From ``rosie go`` it is possible to search for suites, create, checkout, delete, edit, run suites and more.  We will only take a look at the main features here.  Full details on all the features of ``rosie go`` can be found in the user guide - http://metomi.github.io/rose/doc/rose-rug-rosie-go.html.

Launch ``rosie go`` by typing: ::

  puma$ rosie go

**i. Searching for suites**

By default, ``rosie go`` will show all the suites that you have checked out locally, so unless you have used Rose before you will have an empty results panel to begin with.  You can search for suites by typing a word/phrase into the search box and either click the search button or press ``<Enter>``.  The search looks for the entered word/phrase in **any** of a suite's properties.

* Enter **u-ag137** in the *Search* box and press ``<Enter>``

You should now see a long list of suites. All these suites are listed as they reference ``u-ag137`` in their suite information.

More advanced queries can be run by clicking the **+** button next to the search button.  Queries allow you to filter results based on the values of particular properties. You can combine filters to make complex queries.

* Select **idx** in the property box and **eq** in the operator box and then enter the value **u-ag137**. Click **Query**.

This time you should only see one suite listed in the results pane.

* Now run a query to list all suites **owned by rosalynhatcher containing ARCHER in their title**.

The searches you run within ``rosie go`` are recorded in your search history.

* View your history by clicking *"History -> Show search history"*.

The Search History panel should now be displayed on the left-hand side of ``rosie go`` listing your past searches.  You can order the results by type, parameters or whether you asked to see all revisions by clicking on the relevent column head. To re-run one of these searches simply click on it. 

* Try running your initial search for u-ag137 again.

Close the History Panel by clicking the close button at the top of the history panel.

**ii. Viewing suite information**

To obtain more information about a suite listed in the search results you can do one of two things; hold your mouse over the suite to display a tooltip containing more details or right click on the suite and click ``Info`` in the pop-up menu to display a dialog box containing further details.

* What project is suite u-ab878 associated with?

Suite search results can be ordered by property in either ascending or descending order. To do so, click on the column title for the property you wish to order by so an arrow is displayed next to it indicating the order in which the property is being sorted.

**iii. Checking out an existing suite**

Right-clicking on a suite displays a pop-up menu from which you can perform many functions on the suite; e.g. checkout, copy, delete, run, etc.  We will perform many of these actions in subsequent exercises but to begin with we will just checkout an existing suite to use in the *"Editing Suites"* exercises. To view a suite it must be checked out first.

* Right-click on suite **u-ag137** and select *Checkout Suite* from the pop-up menu. 

When you checkout a suite it is always placed in your ``~/roses`` directory.  In this state, the suite is simply a working copy - you can edit it and run it but any changes you make will only be held locally.  
 
.. note:: You can also checkout a suite by highlighting it and then clicking the *Checkout* button on the toolbar.  

**iv. Other useful features**

To see what suites you have checked out click the ``Show local suites`` button to the left of the search box (represented by the *home* icon).  You should have at least 1 suite listed.

* What do you think the *house* icon in the local column indicates?

Editing Suites: rose edit
-------------------------

The Rose config editor in combination with the meta-data file, which describes UM inputs, is the GUI for editing UM suites.  Building and running the UM under Rose requires, at least, two separate apps: an fcm_make_app to build the model executable and a UM app to configure the runtime namelists and environment variables.  Coupled models may require additional fcm_make apps, one for each executable to be built.

**i. Launch the config editor GUI**

Right click on suite u-ag137 and select ``Edit Suite``.  The ``rose edit`` GUI will start up.

On the left hand side is a navigation panel containing a tree listing the apps in the suite.  For this particular suite these are:

* *suite conf* - General suite configuration options
* *fcm_make_pp* - Extract and build the post-processing scripts
* *fcm_make_um* - Extract and build the UM source code
* *housekeeping* - Tidies up log files, old work and data directories
* *install_ancil* - Install ancillary files
* *postproc* - Post-processing settings
* *rose_ana* - Rose built in app; used here for comparison of dump files
* *rose_arch* - Rose built in app; used here for archiving of log files
* *um* - The UM atmosphere and reconfiguration settings

**ii. Explore the GUI**

Click on the triangle to the left of *suite conf* to expand that section.  Click on *Build and run switches*.  A panel will appear on the right-hand side containing options for controlling what tasks will be run for this suite.  You can see that it will build the UM and reconfiguration executables, run the reconfiguration and then run the model.

.. note:: We generally use a **common notation** to help users navigate through the GUI and to help us help you with questions. Getting to "UM Science Settings" would be indicated like this: *um->namelist->UM Science Settings*.  This notation will be used throughout the rest of this document.

The input namelists for the um are contained in the *um->namelist* section.  Let's take a look at the science namelist for Microphysics (Large Scale Precipiation), run_precip under "UM Science Settings".

For each UM namelist item there is a short description to help you understand what that variable is.  Click on the cog next to a namelist variable and select *Help* to view more detailed information.  The help information can give you some useful pointers but be aware that it has been written with Met Office setup in mind. 

Range and type checking of variables is done as soon as the user enters a new value.  Try changing the value of *timestep_mp_in* to 0. This will cause an error flag to appear, hover over the error for more information and click the *undo* button several times to revert to the original value.

Some larger science sections have been been divided into subsections, take a look at "Section 05 - Convection" for an example of this. To open a section in a new tab click with the middle mouse button, expand the section by clicking the page triangles. Rose edit has a search box which can be used to search item names. Try searching for the variable *astart* where the input dump is specified, you will be taken directly to the Dumping and Meaning panel.

Trigger ignored settings are hidden by default and only appear to the user when the appropriate options are selected. Open the Gravity Wave Drag panel, if you change *i_gwd_vn* from 5 to 4 the options available change. Click the save button to apply these changes to your app. Let's take a look at what effect this has had to the ``rose-app.conf`` file, run ``fcm diff`` in the suite directory.

  ::

    puma$ cd ~/roses/u-ag137
    puma$ fcm diff -g

You should see that several namelist items have had *!!* added to the start of the line. This tells Rose to ignore these items when processing the app file into Fortran namelists. Should you wish to see all variables on a panel select "View All Ignored Variables" and "View Latent Variables" from the "View" menu.

Switch back to the Rose edit window and click the **undo** button to revert the changes and then **save** the suite again. To view all changes made to the suite in the current session click on the **Undo/Redo Viewer** in the *Edit* menu.

**iii. Error checking of UM inputs**

In addition to the type and range checking of namelist items and environment variables, more thorough checks can be made using Rose macros and the fail-if/warn-if metadata.

First let's check if the suite contains any options which trigger the fail-if and warn-if checks in the UM metadata. Select "Check fail-if, warn-if" from the "Metadata" menu. As this suite is setup correctly "FailureRuleChecker: No problems found" should appear at the bottom right of the window.

Now let's try and introduce both a warning and a failure. We're going to change the boundary layer option "alpha_cd". Either navigate to *"Section 03 - Boundary Layer -> Implicit solver options"* or type "alpha_cd" into the search bar. Click on the plus sign to add an array element to alpha_cd and type 1.5 into the new box. Next navigate to *"Reconfiguration and Ancillary Control -> Output dump grid sizes and levels"* and increase the number of ozone levels to 86. Now run the fail-if, warn-if checker again.

* What is the error?
* What is the warning?

Use the undo button to put the settings back to how we found them and run the checker again. It is strongly recommended that whenever namelists and environment variables are modified that the fail-if, warn-if checker is applied before running the suite.

