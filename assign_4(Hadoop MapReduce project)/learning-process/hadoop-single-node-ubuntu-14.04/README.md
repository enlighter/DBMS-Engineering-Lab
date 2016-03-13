<h1>Hadoop 2.6 Installing on Ubuntu 14.04 (Single-Node Cluster)</h1>
<h3>Hadoop on Ubuntu 14.04</h3>
<h3>Install Java verison 7 or 8 on your ubuntu</h3>
<h3>Adding a dedicated Hadoop user</h3>

    k@laptop:~$ sudo addgroup hadoop
	Adding group `hadoop' (GID 1002) ...
	Done.

	k@laptop:~$ sudo adduser --ingroup hadoop hduser
	Adding user 'hduser' ...
	Adding new user 'hduser' (1001) with group `hadoop' ...
	Creating home directory `/home/hduser' ...
	Copying files from `/etc/skel' ...
	Enter new UNIX password: 
	Retype new UNIX password: 
	passwd: password updated successfully
	Changing the user information for hduser
	Enter the new value, or press ENTER for the default
		Full Name []: 
		Room Number []: 
		Work Phone []: 
		Home Phone []: 
		Other []: 
	Is the information correct? [Y/n] Y

<h3>Installing SSH</h3>
**ssh** has two main components:

 1. **ssh** : The command we use to connect to remote machines - the client
 2. **sshd** : The daemon that is running on the server and allows clients to connect to the server 

The **ssh** is pre-enabled on Linux, but in order to start **sshd** daemon, we need to install **ssh** first. Use this command to do that :

    k@laptop:~$ sudo apt-get install ssh

This will install ssh on our machine. If we get something similar to the following, we can think it is setup properly:

    k@laptop:~$ which ssh
	/usr/bin/ssh
	
	k@laptop:~$ which sshd
	/usr/sbin/sshd

<h3>Create and Setup SSH Certificates</h3>
Hadoop requires SSH access to manage its nodes, i.e. remote machines plus our local machine. For our single-node setup of Hadoop, we therefore need to configure SSH access to localhost.

So, we need to have SSH up and running on our machine and configured it to allow SSH public key authentication.

Hadoop uses SSH (to access its nodes) which would normally require the user to enter a password. However, this requirement can be eliminated by creating and setting up SSH certificates using the following commands. If asked for a filename just leave it blank and press the enter key to continue. 

    k@laptop:~$ su hduser
    Password: 
    k@laptop:~$ ssh-keygen -t rsa -P ""
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/hduser/.ssh/id_rsa): 
    Created directory '/home/hduser/.ssh'.
    Your identification has been saved in /home/hduser/.ssh/id_rsa.
    Your public key has been saved in /home/hduser/.ssh/id_rsa.pub.
    The key fingerprint is:
    50:6b:f3:fc:0f:32:bf:30:79:c2:41:71:26:cc:7d:e3 hduser@laptop
    The key's randomart image is:
	+--[ RSA 2048]----+
	|        .oo.o    |
	|       . .o=. o  |
	|      . + .  o . |
	|       o =    E  |
	|        S +      |
	|         . +     |
	|          O +    |
	|           O o   |
	|            o..  |
	+-----------------+


	hduser@laptop:/home/k$ cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys

The second command adds the newly created key to the list of authorized keys so that Hadoop can use ssh without prompting for a password.

We can check if ssh works:

	hduser@laptop:/home/k$ ssh localhost
	The authenticity of host 'localhost (127.0.0.1)' can't be established.
	ECDSA key fingerprint is e1:8b:a0:a5:75:ef:f4:b4:5e:a9:ed:be:64:be:5c:2f.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.
	Welcome to Ubuntu 14.04.1 LTS (GNU/Linux 3.13.0-40-generic x86_64)
	...

<h3>Install Hadoop</h3>
