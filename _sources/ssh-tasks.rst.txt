Appendix B: SSH FAQs
====================

This Sections provides instructions for some common ssh tasks. If you have any problems, contact a member of the CMS team. 

.. note: Take care not to confuse your ARCHER2 *password* and ssh-key *passphrase*.
 
.. _using-existing-agent:

Using an existing ssh agent
---------------------------

If you already have an ssh-agent set up on PUMA2, you can use this one to connect to your ARCHER2 training account. Conversely, after the course you may wish to use the keys you set up for own Archer account. 

You can copy your ssh key over to Archer using the ``ssh-copy-id`` script. 

First you need to find the name of the public key in your ``.ssh`` directory. :: 

  puma2$ cd ~/.ssh
  puma2$ ls 
  environment.puma2.archer2.ac.uk  id_rsa  id_rsa.pub	known_hosts  ssh-setup

The public key ends with ``.pub`` and will usually be called ``id_rsa.pub`` or ``id_dsa.pub``. 

Now run the script to copy the key to your ARCHER2 account, making sure to use the correct name for your key: :: 

  puma2$ ssh-copy-id -i ~/.ssh/id_rsa.pub <archer-username>@login.archer2.ac.uk

You will be prompted for your Archer password. 

If successful, you should now be able to login to Archer without a password. If you are prompted for a passphrase you need to re-start your agent - see below. 

.. _restarting-agent:

Restarting your ssh agent 
-------------------------

Normally your ssh agent persists even when you log out of puma2. However, from time to time it can vanish. 

If you are prompted for your passphrase, this means the ssh agent has stopped for some reason. The agent *should* have been re-initialised when you logged into PUMA2, but you will need to re-associate your ssh keys to the agent.  

To do so, run: :: 

  puma2$ ssh-add

If successful this will prompt for your passphrase: :: 
   
  Enter passphrase for /home/<puma2-username>/.ssh/id_rsa_archerum: 

Sometimes this step will fail with the following error: :: 

  Could not open a connection to your authentication agent.

In this case, the agent is not running. Usually this is beacuse of an environment file. Delete the following: :: 

  puma2$ rm ~/.ssh/environment.puma2.archer2.ac.uk

Then log out of puma2 and back in again. You should hopefully see a message similar to: :: 

  Initialising new SSH agent...

And you should now be able to run ssh-add successfully. 

.. _regenerating-keys:

Regenerating your ssh keys
--------------------------

If you have forgotten your passphrase you will need to regenerate your ssh keys. Before doing so, you will need to tidy up the old keys otherwise the ssh agent can get itself confused. 

Go to your ``.ssh`` directory, and look at the files: :: 

  puma2$ cd ~/.ssh
  puma2$ ls
  environment.puma2.archer2.ac.uk  id_rsa  id_rsa.pub	known_hosts  ssh-setup

Delete the public and private keys. These will normally be named ``id_rsa`` and ``id_rsa.pub``, or ``id_dsa`` and ``id_dsa.pub``. 

You should also delete the ``environment.puma2.archer2.ac.uk`` file: :: 

  puma2$ rm id_rsa id_rsa.pub environment.puma2.archer2.ac.uk 

Next check if you have an agent running: :: 

  puma2$ ps -flu <puma2-username> | grep ssh-agent

If you have an agent running, one or more lines like the following will be returned: :: 
     
  15658 ?        00:00:00 ssh-agent

The number in the first column is the process-id, pass this to the ``kill`` command to stop the process, for example: :: 
  
  puma2$ kill -9 15658

You can now start again, following the :ref:`ssh set up instructions <ssh-setup>`. 
