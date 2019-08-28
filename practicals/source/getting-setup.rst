Getting set up
==============

Install and Launch MobaXterm
----------------------------

Unfortunately we can no longer pre-install MobaXterm for you due to licencing restrictions, so you will first need to download and install MobaXterm:

* Login to the windows machine with your University of Reading credentials
* | From Chrome, go to page: https://mobaxterm.mobatek.net/download.html 
  | Google “mobaxterm download” and this should be the first entry (check the URL). 
* Under “Home Edition” select “Download now”
* | On next page select **“MobaXterm Home Edition v11.1 (Portable edition)”**. 
  | This should download the package. 
* Click the download icon in the bottom left hand corner. 
* | Double-click on the **MobaXterm_Personal_11.1** application file, and select “Extract all”. 
  | A new directory window will open up. 
* Double-click **MobaXterm_Personal_11.1** to launch the application.

Next time, navigate to “Downloads” to open the application.

Login to PUMA 
-------------

::

  xterm$ ssh -Y <puma-username>@puma.nerc.ac.uk

Set up your PUMA environment and access to MOSRS
------------------------------------------------

**i. Configure ~/.profile**

If this is the first time you have used your PUMA account, you will need to create a ``.profile``. Copy our standard one: :: 

  puma$ cd
  puma$ cp ~um/um-training/setup/.profile .

(If you already have a ``.profile``, make sure it includes the lines from the standard file.)

**ii. Configuring access to MOSRS**

Run the ``mosrs-setup`` script which will take you through the set up process to access the Met Office Science Repository Service (Remember your MOSRS username is one word; usually firstnamelastname, all in lowercase): ::

  puma$ ~um/um-training/mosrs-setup

Log out of PUMA and back in again (you will get a warning about not being able to find ``~/.ssh/ssh-setup`` this can be ignored and will be resolved in the next step). You should be prompted for your Met Office Science Repository Service password. A new window should then pop up (it may be hidden behind other windows) for ``Rosie`` asking for **Username for 'u' - 'https://code.metoffice.gov.uk/rosie/u'** . Enter your MOSRS username again.

.. note:: The cached password is configured to expire after 12 hours. Simply run the command ``mosrs-cache-password`` to re-cache it if this happens. Also if you know you won't need access to the repositories during a login session then just press return when asked for your MOSRS password.

Make sure you can login to your ARCHER training account
-------------------------------------------------------

An ARCHER username will be provided on the day of the course. Ask the CMS team if you're unsure. The password for these accounts is listed in a file on PUMA: ``~um/um-training/login.txt``. 

From PUMA: :: 

  puma$ ssh <archer-username>@login.archer.ac.uk

.. note:: It's best to copy and paste the password from the file rather than type it by hand.  

Set up your ARCHER environment 
------------------------------

Once you have successfully logged into ARCHER, copy the following profile to your home directory. :: 

  archer$ cp /work/y07/y07/umshared/um-training/rose-profile ~/.profile

Exit ARCHER
-----------

Log out of ARCHER. This should take you back to puma. 

:: 

  archer$ exit

.. _ssh-setup:

Set up an ssh connection from PUMA to ARCHER
--------------------------------------------

.. note:: If you already have ssh keys and agent set up on PUMA, follow the instructions on :ref:`using-existing-agent` in the Appendix, then skip to Section 1.8.

**i. Generate authentication key on PUMA and install it on ARCHER.** 

Run the ``install-ssh-keys`` script.  This will take you through ssh-key creation and copy the key over to ARCHER.
:: 

  puma$ source ~um/um-training/install-ssh-keys <archer-username>@login.archer.ac.uk

When prompted to **Enter passphrase**, this should be a fairly complicated and unguessable passphrase. You can use spaces in the passphrase if it helps you to remember it more readily. It is recommended that you don't use your password in case it is hacked. 

.. warning:: **DO NOT** use an empty passphrase as this presents a security issue.

After generating your ssh-key, the script will copy it over to ARCHER.  

When prompted for **Password**, enter your ARCHER password.


**ii. Verify the authentication works.** 

:: 

  puma$ ssh <archer-username>@login.archer.ac.uk
  Enter passphrase for key '/home/<puma-username>/.ssh/id_dsa': 
  [TYPE_YOUR_PASSPHRASE]

If you don't get asked for your Passphrase (i.e. RSA key), then something has gone wrong. In this case, make sure the public key, was successfully copied over to ARCHER by logging into ARCHER and opening the file ``~/.ssh/authorized_keys``. It should contain something similar to: ::

   ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAt1JmHYgsuf0UWVLqNqnDSaUUP2xJ+Um0H5WnUt
   /i2mxhlBrwOtvVWRjnzo5EcylZJs/Cg5JVe4UR6toqNXbZG1RXscLQnQoPAvzFoWLzfP7Q3lrz
   eC1SkM2FWfWC38ga3Svs6fm63/I7WmJy+4D8BWWaXj/9yM1OskFj6yfWItr150rwwNauOQbWJh
   l7I/KkfhVPBvZ9vHiAK4cjUMQ9fFS1dij3GSBmOfu2RuMgNNg9y1MLSzEk2242F4tOg7paTk7w
   wUZ+ZLqRBtT2aREnjIGI7KvACBZD1y40tXXPIZw9m2Dl0dK7mFQ2/YFWh2/NAmkFMXzDOmkg0b
   iq1m+QKw==
   ros@puma

If it doesn't, and no errors were reported from the ``install-ssh-keys`` script, please ask for assistance.

Once you have this part working, log out of ARCHER. 

**iii. Start up ssh-agent.**

Run the following command and type your passphrase: :: 

  puma$ ssh-add
  Enter passphrase for /home/<puma-username>/.ssh/id_rsa: 
  [TYPE_YOUR_PASSPHRASE]

The ssh agent should keep running even when you log out of puma, however you may need to restart it from time to time. For instructions on how to do this see :ref:`restarting-agent` in the Appendix. 
	
Check this all works by ssh-ing to ARCHER 
-----------------------------------------

From PUMA type: ::

  puma$ ssh <archer-username>@login.archer.ac.uk

If you get to ARCHER without a password or passphrase, then you're done.


You are now ready to try running a UM suite! 
