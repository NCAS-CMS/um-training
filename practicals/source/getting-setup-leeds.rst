Getting set up (7th-9th February, Leeds)
========================================

.. warning::
   You **MUST** have PUMA, ARCHER2 and MOSRS accounts setup before starting this section.
   
.. note::
   These instructions are for use on the UM Training Course held on 7-9th February 2023.  If you are using them for self-study please contact NCAS-CMS for instructions.
   
Setup connection to PUMA & ARCHER2
----------------------------------

To use the UM Introduction Tutorials you will first need to ensure you can connect from the local desktop to both PUMA & ARCHER2.  

SSH key files
^^^^^^^^^^^^^

Before you try and connect to PUMA or ARCHER2, you need to make sure that you have the ssh-keys for both platforms available on the local desktop.

Hopefully you remembered to bring your ssh-keys with you on a USB stick. Please talk to a course tutor if you have forgotten them.

Copy your ssh-keys from the USB stick to the ``~/.ssh`` directory.

Connecting via a Terminal (GNU/Linux & macOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Connect via a terminal with an X11 connection (`XQuartz <https://www.xquartz.org/>`_ is also required when using macOS)

Login to PUMA: ::

  ssh -Y -i ~/.ssh/id_rsa_puma <puma-username>@192.171.169.138
  
We suggest adding an entry to the ``~/.ssh/config`` file so you don't need to keep typing in the IP address. For example: ::

  Host puma
  Hostname 192.171.169.138
  User <puma_username>
  IdentityFile ~/.ssh/id_rsa_puma
  ForwardX11 yes
  ForwardX11Trusted yes
   
so that you can then connect using the command: ::

  ssh puma

In a new terminal window, login to ARCHER2: ::

  ssh -Y -i ~/.ssh/id_rsa_archer <archer2-username>@login.archer2.ac.uk

Again you could define a ``~/.ssh/config`` file entry for each with the necessary information, if desired. For example: ::

  Host login.archer2.ac.uk
  User <archer2_username>
  IdentityFile ~/.ssh/id_rsa_archer
  ForwardX11 yes
  ForwardX11Trusted yes

so that you could then just connect using the command: ::
  
  ssh login.archer2.ac.uk

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

Log out of PUMA and back in again (you will get a warning about not being able to find ``~/.ssh/ssh-setup`` this can be ignored and will be resolved in the next step). You should first be prompted for your **Met Office Science Repository Service password**.  Enter your password. Then you will be prompted for **Username for 'u' - 'https://code.metoffice.gov.uk/rosie/u'** . Enter your MOSRS username.

.. A new window should then pop up (it may be hidden behind other windows) for ``Rosie`` asking for **Username for 'u' - 'https://code.metoffice.gov.uk/rosie/u'** . Enter your MOSRS username again.

.. note:: The cached password is configured to expire after 12 hours. Simply run the command ``mosrs-cache-password`` to re-cache it if this happens. Also if you know you won't need access to the repositories during a login session then just press return when asked for your MOSRS password.

Configure connection to ARCHER2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Due to ARCHER2 security and the UM workflow it is necessary to use a special ssh-key that allows submission of UM suite from PUMA.
Prior to the course you generated a UM workflow ssh-key called ``~/.ssh/id_rsa_archerum``.

**i. Update ssh config file**

In your PUMA ``~/.ssh/config`` file add the following section: ::

  Host login.archer2.ac.uk
  User <archer2_username>
  IdentityFile ~/.ssh/id_rsa_archerum
  ForwardX11 no
  ForwardX11Trusted no

Where ``<archer2_username>`` should be replaced with your ARCHER2 username. If you don't have a ``~/.ssh/config`` file create one.

.. _ssh-setup:

**ii. Set up ssh-agent**

Setting up an ``ssh-agent`` allows caching of your ``id_rsa_archerum`` key passphrase for a period of time. ::

  puma$ cp ~um/um-training/setup/ssh-setup ~/.ssh

Log out of PUMA and back in again to start up the ``ssh-agent`` process.

Add your ``id_rsa_archerum`` key to your ``ssh-agent`` by running: ::

  puma$ ssh-add ~/.ssh/id_rsa_archerum
  Enter passphrase for /home/<puma-username>/.ssh/id_rsa:
  [TYPE_YOUR_PASSPHRASE]

Enter your passphrase when prompted.  The ``ssh-agent`` will continue to run even when you log out of PUMA, however, it may stop from time to time, for example if PUMA is rebooted.  For instructions on what to do in this situation see :ref:`restarting-agent` in the Appendix.

**iii. Verify the setup is correct**

Log in to ARCHER2 with: ::

  puma$ ssh login.archer2.ac.uk

You should not be prompted for your passphrase.  The response from ARCHER2 should be: ::

  puma$ ssh login.archer2.ac.uk
  PTY allocation request failed on channel 0
  Comand rejected by policy. Not in authorised list 
  Connection to login.archer2.ac.uk closed.

.. note:: It is not possible to start an interactive login session on ARCHER2 from PUMA.  For an interactive session you need to login from your local desktop.

You are now ready to try running a UM suite! 
