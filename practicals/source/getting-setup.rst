Getting set up
==============

.. warning::
   You **MUST** have PUMA, ARCHER2 and MOSRS accounts setup before starting this section.
   
Setup connection to PUMA & ARCHER2
----------------------------------

To use the UM Introduction Tutorials you will first need to ensure you can connect from your local desktop to a both PUMA & ARCHER2.  There a multiple ways in which you can do this depending on your desktop platform:

* via `Terminal <terminal_>`_ on GNU/Linux & macOS
* via `MobaXTerm <mobaxterm_>`_ on Windows

SSH key files
^^^^^^^^^^^^^

Before you try and connect to PUMA or ARCHER2, you need to make sure that you have the ssh-keys for both platforms available on your computer.

.. _terminal:

Connecting via a Terminal (GNU/Linux & macOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It is possible to connect via a terminal with an X11 connection (`XQuartz <https://www.xquartz.org/>`_ is also required when using macOS)

Login to PUMA: ::

  ssh -Y -i /path/to/id_rsa_puma <puma-username>@puma.nerc.ac.uk

Login to ARCHER2: ::

  ssh -Y -i /path/to/id_rsa_archer <archer2-username>@login-4c.archer2.ac.uk

It is also possible to define a ``~/.ssh/config`` file entry for each with the necessary information, if desired. For example: ::

  Host login-4c.archer2.ac.uk
  User <archer2_username>
  IdentityFile ~/.ssh/id_rsa_archer
  ForwardX11 no
  ForwardX11Trusted no

so that you could then just connect using the command: ::
  
  ssh -Y login-4c.archer2.ac.uk

and similarly for PUMA.

.. _mobaxterm:

Connecting via MobaXTerm
^^^^^^^^^^^^^^^^^^^^^^^^

* From Chrome, go to page: https://mobaxterm.mobatek.net/download.html 
* Under “Home Edition” select “Download now”
* | On next page select **“MobaXterm Home Edition v21.4 (Portable edition)”**. 
  | This should download the package.
* Click the download icon in the bottom left hand corner. 
* | Double-click on the **MobaXterm_Personal_21.4** application file, and select “Extract all”. 
  | A new directory window will open up. 
* Double-click **MobaXterm_Personal_21.4** to launch the application.

Next time, navigate to “Downloads” to open the application.

Set up your ARCHER2 environment 
--------------------------------

Login to ARCHER2 from your local desktop, copy the following profile to your home directory. :: 

  archer2$ cp /work/y07/shared/umshared/um-training/rose-profile ~/.profile

Change the permissions on your ``/home`` and ``/work`` directories to enable the NCAS-CMS team to help with any queries: ::

  chmod -R g+rX /home/n02/n02/<your-username>
  chmod -R g+rX /work/n02/n02/<your-username>

Set up your PUMA environment
----------------------------

Login to PUMA from your local desktop.

Configure ``~/.profile``
^^^^^^^^^^^^^^^^^^^^^^^^
If this is the first time you have used your PUMA account, you will need to create a ``.profile``. Copy our standard one: :: 

  puma$ cd
  puma$ cp ~um/um-training/setup/.profile .

(If you already have a ``.profile``, make sure it includes the lines from the standard file.)

Configure access to MOSRS
^^^^^^^^^^^^^^^^^^^^^^^^^
Run the ``mosrs-setup`` script which will take you through the set up process to access the Met Office Science Repository Service (Remember your MOSRS username is one word; usually firstnamelastname, all in lowercase): ::

  puma$ ~um/um-training/mosrs-setup

Log out of PUMA and back in again (you will get a warning about not being able to find ``~/.ssh/ssh-setup`` this can be ignored and will be resolved in the next step). You should be prompted for your Met Office Science Repository Service password. A new window should then pop up (it may be hidden behind other windows) for ``Rosie`` asking for **Username for 'u' - 'https://code.metoffice.gov.uk/rosie/u'** . Enter your MOSRS username again.

.. note:: The cached password is configured to expire after 12 hours. Simply run the command ``mosrs-cache-password`` to re-cache it if this happens. Also if you know you won't need access to the repositories during a login session then just press return when asked for your MOSRS password.

Configure connection to ARCHER2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Due to ARCHER2 security and the UM workflow it is necessary to generate a special ssh-key that allows submission of UM suite from PUMA.

**i. Generate UM workflow ssh-key**

Run the following command to generate your ``id_rsa_archerum`` ssh key: ::

  puma$ ssh-keygen -t rsa -b 4096 -C "ARCHER2 UM Workflow" -f ~/.ssh/id_rsa_archerum

When prompted to **Enter passphrase**, this should be a fairly complicated and unguessable passphrase. You can use spaces in the passphrase if it helps you to remember it more readily. It is recommended that you don't use your password in case it is hacked.

Your ``id_rsa_archerum`` key will be automatically detected and sent to ARCHER2 to be installed.  This may take up to 48 hours, excluding weekends, to become activated and you will receive an email confirmation.

.. warning::
   * **DO NOT** use an empty passphrase.  This presents a security issue.
   * **DO NOT** regenerate your ``id_rsa_archerum`` key once you have a working one in place, unless absolutely necessary.

**ii. Update ssh config file**

In your PUMA ``~/.ssh/config`` file add the following section: ::

  Host login-4c.archer2.ac.uk
  User <archer2_username>
  IdentityFile ~/.ssh/id_rsa_archerum
  ForwardX11 no
  ForwardX11Trusted no

Where ``<archer2_username>`` should be replaced with your ARCHER2 username. If you don't have a ``~/.ssh/config`` file create one.

**iii. Set up ssh-agent**

Setting up an ``ssh-agent`` allows caching of your ``id_rsa_archerum`` key passphrase for a period of time. ::

  puma$ cp ~um/um-training/setup/ssh-setup ~/.ssh

Log out of PUMA and back in again to start up the ``ssh-agent`` process.

Add your ``id_rsa_archerum`` key to your ``ssh-agent`` by running: ::

  puma$ ssh-add ~/.ssh/id_rsa_archerum
  Enter passphrase for /home/<puma-username>/.ssh/id_rsa:
  [TYPE_YOUR_PASSPHRASE]

Enter your passphrase when prompted.  The ``ssh-agent`` will continue to run even when you log out of PUMA, however, it may stop from time to time, for example if PUMA is rebooted.  For instructions on what to do in this situation see :ref:`restarting-agent` in the Appendix.

**iv. Verify the setup is correct**

.. note:: Only proceed to this step once your ``id_rsa_archerum`` key has been installed on ARCHER2.

Log in to ARCHER2 with: ::

  puma$ ssh login-4c.archer2.ac.uk

You should not be prompted for your passphrase.  The response from ARCHER2 should be: ::

  puma$ ssh login-4c.archer2.ac.uk
  PTY allocation request failed on channel 0
  Comand rejected by policy. Not in authorised list 
  Connection to login-4c.archer2.ac.uk closed.

.. note:: It is not possible to start an interactive login session on ARCHER2 from PUMA.  For an interactive session you need to login from your local desktop or via your host institution.

You are now ready to try running a UM suite! 
