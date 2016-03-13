#Hadoop 2.6 Installing on Ubuntu 14.04 (Single-Node Cluster)</h1>
##Hadoop on Ubuntu 14.04
###Install Java verison 7 or 8 on your ubuntu
##Adding a dedicated Hadoop user

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

##Installing SSH
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

##Create and Setup SSH Certificates
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

##Install Hadoop
	hduser@laptop:~$ wget http://mirrors.sonic.net/apache/hadoop/common/hadoop-2.6.0/hadoop-2.6.0.tar.gz
	hduser@laptop:~$ tar xvzf hadoop-2.6.0.tar.g
We want to move the Hadoop installation to the /usr/local/hadoop directory using the following command:

	hduser@laptop:~/hadoop-2.6.0$ sudo mv * /usr/local/hadoop
	[sudo] password for hduser: 
	hduser is not in the sudoers file.  This incident will be reported
	
Oops!... We got:

	"hduser is not in the sudoers file. This incident will be reported."

This error can be resolved by logging in as a root user, and then add hduser to sudo:

	hduser@laptop:~/hadoop-2.6.0$ su k
	Password: 

	k@laptop:/home/hduser$ sudo adduser hduser sudo
	[sudo] password for k: 
	Adding user `hduser' to group `sudo' ...
	Adding user hduser to group sudo
	Done.
Now, the hduser has root priviledge, we can move the Hadoop installation to the **/usr/local/hadoop** directory without any problem:

	k@laptop:/home/hduser$ sudo su hduser

	hduser@laptop:~/hadoop-2.6.0$ sudo mv * /usr/local/hadoop 
	hduser@laptop:~/hadoop-2.6.0$ sudo chown -R hduser:hadoop /usr/local/hadoop

##Setup Configuration Files
The following files will have to be modified to complete the Hadoop setup:

 1.  ~/.bashrc
 2. /usr/local/hadoop/etc/hadoop/hadoop-env.sh
 3. /usr/local/hadoop/etc/hadoop/core-site.xml
 4. /usr/local/hadoop/etc/hadoop/mapred-site.xml.template
 5. /usr/local/hadoop/etc/hadoop/hdfs-site.xml

###1. ~/.bashrc:
Before editing the **.bashrc** file in our home directory, we need to find the path where Java has been installed to set the **JAVA_HOME** environment variable using the following command:

	hduser@laptop update-alternatives --config java
	There is only one alternative in link group java (providing /usr/bin/java): /usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java
	Nothing to configure.
Now we can append the following to the end of **~/.bashrc**:

	hduser@laptop:~$ vi ~/.bashrc

	#HADOOP VARIABLES START
	export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
	export HADOOP_INSTALL=/usr/local/hadoop
	export PATH=$PATH:$HADOOP_INSTALL/bin
	export PATH=$PATH:$HADOOP_INSTALL/sbin
	export HADOOP_MAPRED_HOME=$HADOOP_INSTALL
	export HADOOP_COMMON_HOME=$HADOOP_INSTALL
	export HADOOP_HDFS_HOME=$HADOOP_INSTALL
	export YARN_HOME=$HADOOP_INSTALL
	export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_INSTALL/lib/native
	export HADOOP_OPTS="-Djava.library.path=$HADOOP_INSTALL/lib"
	#HADOOP VARIABLES END

	hduser@laptop:~$ source ~/.bashrc
note that the JAVA_HOME should be set as the path just before the '.../bin/':

	hduser@ubuntu-VirtualBox:~$ javac -version
	javac 1.7.0_75

	hduser@ubuntu-VirtualBox:~$ which javac
	/usr/bin/javac

	hduser@ubuntu-VirtualBox:~$ readlink -f /usr/bin/javac
	/usr/lib/jvm/java-7-openjdk-amd64/bin/javac

