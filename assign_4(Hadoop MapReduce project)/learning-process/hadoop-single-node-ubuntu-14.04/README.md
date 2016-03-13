#Hadoop 2.6 Installing on Ubuntu 14.04 (Single-Node Cluster)</h1>
##Hadoop 2.7.2 on Ubuntu 14.04.2
I followed this guide for Linux Mint Rosa with hadoop 2.7.2
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
	hduser@laptop:~$ wget http://a.mbbsindia.com/hadoop/common/hadoop-2.7.2/hadoop-2.7.2.tar.gz
	hduser@laptop:~$ tar xvzf hadoop-2.7.2.tar.gz
We want to move the Hadoop installation to the /usr/local/hadoop directory using the following command:

	hduser@laptop:~/hadoop-2.7.2$ sudo mv * /usr/local/hadoop
	[sudo] password for hduser: 
	hduser is not in the sudoers file.  This incident will be reported
	
Oops!... We got:

	"hduser is not in the sudoers file. This incident will be reported."

This error can be resolved by logging in as a root user, and then add hduser to sudo:

	hduser@laptop:~/hadoop-2.7.2$ su k
	Password: 

	k@laptop:/home/hduser$ sudo adduser hduser sudo
	[sudo] password for k: 
	Adding user `hduser' to group `sudo' ...
	Adding user hduser to group sudo
	Done.
Now, the **hduser** has root priviledge, we can move the Hadoop installation to the **/usr/local/hadoop** directory without any problem:

	k@laptop:/home/hduser$ sudo su hduser

	hduser@laptop:~/hadoop-2.7.2$ sudo mv * /usr/local/hadoop 
	hduser@laptop:~/hadoop-2.7.2$ sudo chown -R hduser:hadoop /usr/local/hadoop

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
	There are 2 choices for the alternative java (providing /usr/bin/java).

  	Selection    Path                                            Priority   Status
	------------------------------------------------------------
  	  0            /usr/lib/jvm/java-8-oracle/jre/bin/java          1074      auto mode
  	  1            /usr/lib/jvm/java-7-openjdk-amd64/jre/bin/java   1071      manual mode
	* 2            /usr/lib/jvm/java-8-oracle/jre/bin/java          1074      manual mode

	Press enter to keep the current choice[*], or type selection number: 0

Now we can append the following to the end of **~/.bashrc**:

	hduser@laptop:~$ vi ~/.bashrc

	#HADOOP VARIABLES START
	export JAVA_HOME=/usr/lib/jvm/java-8-oracle
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
	javac 1.8.0_74

	hduser@ubuntu-VirtualBox:~$ which javac
	/usr/bin/javac

	hduser@ubuntu-VirtualBox:~$ readlink -f /usr/bin/javac
	/usr/lib/jvm/java-8-oracle/bin/javac

###2. /usr/local/hadoop/etc/hadoop/hadoop-env.sh

We need to set **JAVA_HOME** by modifying **hadoop-env.sh** file.

	hduser@laptop:~$ vi /usr/local/hadoop/etc/hadoop/hadoop-env.sh

	export JAVA_HOME=/usr/lib/jvm/java-8-oracle

Adding the above statement in the hadoop-env.sh file ensures that the value of JAVA_HOME variable will be available to Hadoop whenever it is started up.

###3. /usr/local/hadoop/etc/hadoop/core-site.xml:

The **/usr/local/hadoop/etc/hadoop/core-site.xml** file contains configuration properties that Hadoop uses when starting up.
This file can be used to override the default settings that Hadoop starts with.

	hduser@laptop:~$ sudo mkdir -p /app/hadoop/tmp
	hduser@laptop:~$ sudo chown hduser:hadoop /app/hadoop/tmp

Open the file and enter the following in between the `<configuration></configuration>` tag:

	hduser@laptop:~$ vi /usr/local/hadoop/etc/hadoop/core-site.xml

	<configuration>
	 <property>
	  <name>hadoop.tmp.dir</name>
	  <value>/app/hadoop/tmp</value>
	  <description>A base for other temporary directories.</description>
	 </property>

	 <property>
	  <name>fs.default.name</name>
	  <value>hdfs://localhost:54310</value>
	  <description>The name of the default file system.  A URI whose scheme and authority determine the FileSystem implementation. The  uri's scheme determines the config property (fs.SCHEME.impl) naming the FileSystem implementation class.  The uri's authority is used to determine the host, port, etc. for a filesystem.</description>
	 </property>
	</configuration>

###4. /usr/local/hadoop/etc/hadoop/mapred-site.xml

By default, the **/usr/local/hadoop/etc/hadoop/** folder contains
**/usr/local/hadoop/etc/hadoop/mapred-site.xml.template**
file which has to be renamed/copied with the name **mapred-site.xml**:

	hduser@laptop:~$ cp /usr/local/hadoop/etc/hadoop/mapred-site.xml.template /usr/local/hadoop/etc/hadoop/mapred-site.xml

The **mapred-site.xml** file is used to specify which framework is being used for MapReduce. We need to enter the following content in between the `<configuration></configuration>` tag: 

	<configuration>
	 <property>
	  <name>mapred.job.tracker</name>
	  <value>localhost:54311</value>
	  <description>The host and port that the MapReduce job tracker runs at.  If "local", then jobs are run in-process as a single map and reduce task.
	  </description>
	 </property>
	</configuration>

###5. /usr/local/hadoop/etc/hadoop/hdfs-site.xml

The **/usr/local/hadoop/etc/hadoop/hdfs-site.xml** file needs to be configured for each host in the cluster that is being used.
It is used to specify the directories which will be used as the **namenode** and the **datanode** on that host.

Before editing this file, we need to create two directories which will contain the namenode and the datanode for this Hadoop installation.
This can be done using the following commands:

	hduser@laptop:~$ sudo mkdir -p /usr/local/hadoop_store/hdfs/namenode
	hduser@laptop:~$ sudo mkdir -p /usr/local/hadoop_store/hdfs/datanode
	hduser@laptop:~$ sudo chown -R hduser:hadoop /usr/local/hadoop_store

Open the file and enter the following content in between the `<configuration></configuration>` tag: 

	hduser@laptop:~$ vi /usr/local/hadoop/etc/hadoop/hdfs-site.xml

	<configuration>
	 <property>
	  <name>dfs.replication</name>
	  <value>1</value>
	  <description>Default block replication.The actual number of replications can be specified when the file is created.
	  The default is used if replication is not specified in create time.
	  </description>
	 </property>
	 
	 <property>
	   <name>dfs.namenode.name.dir</name>
	   <value>file:/usr/local/hadoop_store/hdfs/namenode</value>
	 </property>
	 
	 <property>
	   <name>dfs.datanode.data.dir</name>
	   <value>file:/usr/local/hadoop_store/hdfs/datanode</value>
	 </property>
	</configuration>

##Format the New Hadoop Filesystem

Now, the Hadoop file system needs to be formatted so that we can start to use it. The format command should be issued with write permission since it creates **current** directory
under **/usr/local/hadoop_store/hdfs/namenode** folder:

	hduser@laptop:~$ hdfs namenode -format
	16/03/13 09:56:54 INFO namenode.NameNode: STARTUP_MSG: 
	/************************************************************
	STARTUP_MSG: Starting NameNode
	STARTUP_MSG:   host = enlighterCOM/127.0.1.1
	STARTUP_MSG:   args = [-format]
	STARTUP_MSG:   version = 2.7.2
	STARTUP_MSG:   classpath = /usr/local/hadoop/etc/hadoop:/usr/local/hadoop/share/hadoop/common/lib/commons-beanutils-1.7.0.jar:/usr/local/hadoop/share/hadoop/common/lib/java-xmlbuilder-0.4.jar:/usr/local/hadoop/share/hadoop/common/lib/jets3t-0.9.0.jar:/usr/local/hadoop/share/hadoop/common/lib/stax-api-1.0-2.jar:/usr/local/hadoop/share/hadoop/common/lib/htrace-core-3.1.0-incubating.jar:/usr/local/hadoop/share/hadoop/common/lib/log4j-1.2.17.jar:/usr/local/hadoop/share/hadoop/common/lib/jsch-0.1.42.jar:/usr/local/hadoop/share/hadoop/common/lib/paranamer-2.3.jar:/usr/local/hadoop/share/hadoop/common/lib/xmlenc-0.52.jar:/usr/local/hadoop/share/hadoop/common/lib/snappy-java-1.0.4.1.jar:/usr/local/hadoop/share/hadoop/common/lib/gson-2.2.4.jar:/usr/local/hadoop/share/hadoop/common/lib/slf4j-api-1.7.10.jar:/usr/local/hadoop/share/hadoop/common/lib/junit-4.11.jar:/usr/local/hadoop/share/hadoop/common/lib/jersey-json-1.9.jar:/usr/local/hadoop/share/hadoop/common/lib/guava-11.0.2.jar:/usr/local/hadoop/share/hadoop/common/lib/apacheds-i18n-2.0.0-M15.jar:/usr/local/hadoop/share/hadoop/common/lib/jersey-server-1.9.jar:/usr/local/hadoop/share/hadoop/common/lib/jaxb-impl-2.2.3-1.jar:/usr/local/hadoop/share/hadoop/common/lib/jetty-6.1.26.jar:/usr/local/hadoop/share/hadoop/common/lib/api-util-1.0.0-M20.jar:/usr/local/hadoop/share/hadoop/common/lib/zookeeper-3.4.6.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-math3-3.1.1.jar:/usr/local/hadoop/share/hadoop/common/lib/asm-3.2.jar:/usr/local/hadoop/share/hadoop/common/lib/jaxb-api-2.2.2.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-httpclient-3.1.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-configuration-1.6.jar:/usr/local/hadoop/share/hadoop/common/lib/curator-framework-2.7.1.jar:/usr/local/hadoop/share/hadoop/common/lib/jetty-util-6.1.26.jar:/usr/local/hadoop/share/hadoop/common/lib/jersey-core-1.9.jar:/usr/local/hadoop/share/hadoop/common/lib/jsr305-3.0.0.jar:/usr/local/hadoop/share/hadoop/common/lib/xz-1.0.jar:/usr/local/hadoop/share/hadoop/common/lib/api-asn1-api-1.0.0-M20.jar:/usr/local/hadoop/share/hadoop/common/lib/jackson-jaxrs-1.9.13.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-lang-2.6.jar:/usr/local/hadoop/share/hadoop/common/lib/hadoop-annotations-2.7.2.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-logging-1.1.3.jar:/usr/local/hadoop/share/hadoop/common/lib/activation-1.1.jar:/usr/local/hadoop/share/hadoop/common/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/common/lib/hamcrest-core-1.3.jar:/usr/local/hadoop/share/hadoop/common/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-net-3.1.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-cli-1.2.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-digester-1.8.jar:/usr/local/hadoop/share/hadoop/common/lib/jackson-xc-1.9.13.jar:/usr/local/hadoop/share/hadoop/common/lib/jettison-1.1.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-codec-1.4.jar:/usr/local/hadoop/share/hadoop/common/lib/httpclient-4.2.5.jar:/usr/local/hadoop/share/hadoop/common/lib/servlet-api-2.5.jar:/usr/local/hadoop/share/hadoop/common/lib/mockito-all-1.8.5.jar:/usr/local/hadoop/share/hadoop/common/lib/curator-client-2.7.1.jar:/usr/local/hadoop/share/hadoop/common/lib/curator-recipes-2.7.1.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-collections-3.2.2.jar:/usr/local/hadoop/share/hadoop/common/lib/jsp-api-2.1.jar:/usr/local/hadoop/share/hadoop/common/lib/avro-1.7.4.jar:/usr/local/hadoop/share/hadoop/common/lib/hadoop-auth-2.7.2.jar:/usr/local/hadoop/share/hadoop/common/lib/httpcore-4.2.5.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-compress-1.4.1.jar:/usr/local/hadoop/share/hadoop/common/lib/netty-3.6.2.Final.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-io-2.4.jar:/usr/local/hadoop/share/hadoop/common/lib/commons-beanutils-core-1.8.0.jar:/usr/local/hadoop/share/hadoop/common/lib/apacheds-kerberos-codec-2.0.0-M15.jar:/usr/local/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.10.jar:/usr/local/hadoop/share/hadoop/common/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/common/hadoop-nfs-2.7.2.jar:/usr/local/hadoop/share/hadoop/common/hadoop-common-2.7.2-tests.jar:/usr/local/hadoop/share/hadoop/common/hadoop-common-2.7.2.jar:/usr/local/hadoop/share/hadoop/hdfs:/usr/local/hadoop/share/hadoop/hdfs/lib/xercesImpl-2.9.1.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/htrace-core-3.1.0-incubating.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/log4j-1.2.17.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/xml-apis-1.3.04.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/xmlenc-0.52.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/commons-daemon-1.0.13.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/leveldbjni-all-1.8.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/guava-11.0.2.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/jersey-server-1.9.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/jetty-6.1.26.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/asm-3.2.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/jetty-util-6.1.26.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/jersey-core-1.9.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/jsr305-3.0.0.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/commons-lang-2.6.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/commons-logging-1.1.3.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/commons-cli-1.2.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/commons-codec-1.4.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/servlet-api-2.5.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/netty-all-4.0.23.Final.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/netty-3.6.2.Final.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/commons-io-2.4.jar:/usr/local/hadoop/share/hadoop/hdfs/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/hdfs/hadoop-hdfs-2.7.2-tests.jar:/usr/local/hadoop/share/hadoop/hdfs/hadoop-hdfs-nfs-2.7.2.jar:/usr/local/hadoop/share/hadoop/hdfs/hadoop-hdfs-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/lib/stax-api-1.0-2.jar:/usr/local/hadoop/share/hadoop/yarn/lib/log4j-1.2.17.jar:/usr/local/hadoop/share/hadoop/yarn/lib/zookeeper-3.4.6-tests.jar:/usr/local/hadoop/share/hadoop/yarn/lib/leveldbjni-all-1.8.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jersey-json-1.9.jar:/usr/local/hadoop/share/hadoop/yarn/lib/guava-11.0.2.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jersey-server-1.9.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jaxb-impl-2.2.3-1.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jetty-6.1.26.jar:/usr/local/hadoop/share/hadoop/yarn/lib/zookeeper-3.4.6.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jersey-client-1.9.jar:/usr/local/hadoop/share/hadoop/yarn/lib/javax.inject-1.jar:/usr/local/hadoop/share/hadoop/yarn/lib/asm-3.2.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jaxb-api-2.2.2.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jetty-util-6.1.26.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jersey-core-1.9.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jsr305-3.0.0.jar:/usr/local/hadoop/share/hadoop/yarn/lib/xz-1.0.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jackson-jaxrs-1.9.13.jar:/usr/local/hadoop/share/hadoop/yarn/lib/commons-lang-2.6.jar:/usr/local/hadoop/share/hadoop/yarn/lib/commons-logging-1.1.3.jar:/usr/local/hadoop/share/hadoop/yarn/lib/activation-1.1.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/yarn/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop/share/hadoop/yarn/lib/commons-cli-1.2.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jackson-xc-1.9.13.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jettison-1.1.jar:/usr/local/hadoop/share/hadoop/yarn/lib/commons-codec-1.4.jar:/usr/local/hadoop/share/hadoop/yarn/lib/guice-servlet-3.0.jar:/usr/local/hadoop/share/hadoop/yarn/lib/servlet-api-2.5.jar:/usr/local/hadoop/share/hadoop/yarn/lib/commons-collections-3.2.2.jar:/usr/local/hadoop/share/hadoop/yarn/lib/aopalliance-1.0.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jersey-guice-1.9.jar:/usr/local/hadoop/share/hadoop/yarn/lib/commons-compress-1.4.1.jar:/usr/local/hadoop/share/hadoop/yarn/lib/netty-3.6.2.Final.jar:/usr/local/hadoop/share/hadoop/yarn/lib/commons-io-2.4.jar:/usr/local/hadoop/share/hadoop/yarn/lib/guice-3.0.jar:/usr/local/hadoop/share/hadoop/yarn/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-server-tests-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-applications-distributedshell-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-server-applicationhistoryservice-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-server-sharedcachemanager-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-server-web-proxy-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-client-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-server-common-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-applications-unmanaged-am-launcher-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-registry-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-api-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-server-nodemanager-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-common-2.7.2.jar:/usr/local/hadoop/share/hadoop/yarn/hadoop-yarn-server-resourcemanager-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/log4j-1.2.17.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/paranamer-2.3.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/snappy-java-1.0.4.1.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/leveldbjni-all-1.8.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/junit-4.11.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/jersey-server-1.9.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/javax.inject-1.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/asm-3.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/jersey-core-1.9.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/xz-1.0.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/hadoop-annotations-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/jackson-core-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/hamcrest-core-1.3.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/protobuf-java-2.5.0.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/guice-servlet-3.0.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/aopalliance-1.0.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/avro-1.7.4.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/jersey-guice-1.9.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/commons-compress-1.4.1.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/netty-3.6.2.Final.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/commons-io-2.4.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/guice-3.0.jar:/usr/local/hadoop/share/hadoop/mapreduce/lib/jackson-mapper-asl-1.9.13.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-hs-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-core-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-shuffle-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-app-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-hs-plugins-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-2.7.2-tests.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-2.7.2.jar:/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-common-2.7.2.jar:/contrib/capacity-scheduler/*.jar
	STARTUP_MSG:   build = https://git-wip-us.apache.org/repos/asf/hadoop.git -r b165c4fe8a74265c792ce23f546c64604acf0e41; compiled by 'jenkins' on 2016-01-26T00:08Z
	STARTUP_MSG:   java = 1.8.0_74
	************************************************************/
	16/03/13 09:56:55 INFO namenode.NameNode: registered UNIX signal handlers for [TERM, HUP, INT]
	16/03/13 09:56:55 INFO namenode.NameNode: createNameNode [-format]
	16/03/13 09:56:56 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
	Formatting using clusterid: CID-18591cd3-b413-4689-9dac-862316b9a114
	16/03/13 09:56:56 INFO namenode.FSNamesystem: No KeyProvider found.
	16/03/13 09:56:56 INFO namenode.FSNamesystem: fsLock is fair:true
	16/03/13 09:56:57 INFO blockmanagement.DatanodeManager: dfs.block.invalidate.limit=1000
	16/03/13 09:56:57 INFO blockmanagement.DatanodeManager: dfs.namenode.datanode.registration.ip-hostname-check=true
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: dfs.namenode.startup.delay.block.deletion.sec is set to 000:00:00:00.000
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: The block deletion will start around 2016 Mar 13 09:56:57
	16/03/13 09:56:57 INFO util.GSet: Computing capacity for map BlocksMap
	16/03/13 09:56:57 INFO util.GSet: VM type       = 64-bit
	16/03/13 09:56:57 INFO util.GSet: 2.0% max memory 889 MB = 17.8 MB
	16/03/13 09:56:57 INFO util.GSet: capacity      = 2^21 = 2097152 entries
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: dfs.block.access.token.enable=false
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: defaultReplication         = 1
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: maxReplication             = 512
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: minReplication             = 1
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: maxReplicationStreams      = 2
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: replicationRecheckInterval = 3000
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: encryptDataTransfer        = false
	16/03/13 09:56:57 INFO blockmanagement.BlockManager: maxNumBlocksToLog          = 1000
	16/03/13 09:56:57 INFO namenode.FSNamesystem: fsOwner             = hduser (auth:SIMPLE)
	16/03/13 09:56:57 INFO namenode.FSNamesystem: supergroup          = supergroup
	16/03/13 09:56:57 INFO namenode.FSNamesystem: isPermissionEnabled = true
	16/03/13 09:56:57 INFO namenode.FSNamesystem: HA Enabled: false
	16/03/13 09:56:57 INFO namenode.FSNamesystem: Append Enabled: true
	16/03/13 09:56:58 INFO util.GSet: Computing capacity for map INodeMap
	16/03/13 09:56:58 INFO util.GSet: VM type       = 64-bit
	16/03/13 09:56:58 INFO util.GSet: 1.0% max memory 889 MB = 8.9 MB
	16/03/13 09:56:58 INFO util.GSet: capacity      = 2^20 = 1048576 entries
	16/03/13 09:56:58 INFO namenode.FSDirectory: ACLs enabled? false
	16/03/13 09:56:58 INFO namenode.FSDirectory: XAttrs enabled? true
	16/03/13 09:56:58 INFO namenode.FSDirectory: Maximum size of an xattr: 16384
	16/03/13 09:56:58 INFO namenode.NameNode: Caching file names occuring more than 10 times
	16/03/13 09:56:58 INFO util.GSet: Computing capacity for map cachedBlocks
	16/03/13 09:56:58 INFO util.GSet: VM type       = 64-bit
	16/03/13 09:56:58 INFO util.GSet: 0.25% max memory 889 MB = 2.2 MB
	16/03/13 09:56:58 INFO util.GSet: capacity      = 2^18 = 262144 entries
	16/03/13 09:56:58 INFO namenode.FSNamesystem: dfs.namenode.safemode.threshold-pct = 0.9990000128746033
	16/03/13 09:56:58 INFO namenode.FSNamesystem: dfs.namenode.safemode.min.datanodes = 0
	16/03/13 09:56:58 INFO namenode.FSNamesystem: dfs.namenode.safemode.extension     = 30000
	16/03/13 09:56:58 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.window.num.buckets = 10
	16/03/13 09:56:58 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.num.users = 10
	16/03/13 09:56:58 INFO metrics.TopMetrics: NNTop conf: dfs.namenode.top.windows.minutes = 1,5,25
	16/03/13 09:56:58 INFO namenode.FSNamesystem: Retry cache on namenode is enabled
	16/03/13 09:56:58 INFO namenode.FSNamesystem: Retry cache will use 0.03 of total heap and retry cache entry expiry time is 600000 millis
	16/03/13 09:56:58 INFO util.GSet: Computing capacity for map NameNodeRetryCache
	16/03/13 09:56:58 INFO util.GSet: VM type       = 64-bit
	16/03/13 09:56:58 INFO util.GSet: 0.029999999329447746% max memory 889 MB = 273.1 KB
	16/03/13 09:56:58 INFO util.GSet: capacity      = 2^15 = 32768 entries
	Re-format filesystem in Storage Directory /usr/local/hadoop_store/hdfs/namenode ? (Y or N) y
	16/03/13 09:57:03 INFO namenode.FSImage: Allocated new BlockPoolId: BP-550570491-127.0.1.1-1457843223078
	16/03/13 09:57:03 INFO common.Storage: Storage directory /usr/local/hadoop_store/hdfs/namenode has been successfully formatted.
	16/03/13 09:57:03 INFO namenode.NNStorageRetentionManager: Going to retain 1 images with txid >= 0
	16/03/13 09:57:03 INFO util.ExitUtil: Exiting with status 0
	16/03/13 09:57:03 INFO namenode.NameNode: SHUTDOWN_MSG: 
	/************************************************************
	SHUTDOWN_MSG: Shutting down NameNode at enlighterCOM/127.0.1.1
	************************************************************/

Note that **hdfs namenode -format** command should be executed once before we start using Hadoop.
If this command is executed again after Hadoop has been used, it'll destroy all the data on the Hadoop file system.

##Starting Hadoop
Now it's time to start the newly installed single node cluster.
We can use **start-all.sh** or (**start-dfs.sh** and **start-yarn.sh**)

	k@laptop:~$ cd /usr/local/hadoop/sbin

	k@laptop:/usr/local/hadoop/sbin$ ls
	distribute-exclude.sh    start-all.cmd        stop-balancer.sh
	hadoop-daemon.sh         start-all.sh         stop-dfs.cmd
	hadoop-daemons.sh        start-balancer.sh    stop-dfs.sh
	hdfs-config.cmd          start-dfs.cmd        stop-secure-dns.sh
	hdfs-config.sh           start-dfs.sh         stop-yarn.cmd
	httpfs.sh                start-secure-dns.sh  stop-yarn.sh
	kms.sh                   start-yarn.cmd       yarn-daemon.sh
	mr-jobhistory-daemon.sh  start-yarn.sh        yarn-daemons.sh
	refresh-namenodes.sh     stop-all.cmd
	slaves.sh                stop-all.sh

	k@laptop:/usr/local/hadoop/sbin$ sudo su hduser

	hduser@laptop:/usr/local/hadoop/sbin$ start-all.sh
	hduser@laptop:~$ start-all.sh
	This script is Deprecated. Instead use start-dfs.sh and start-yarn.sh
	16/03/13 09:58:47 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
	Starting namenodes on [localhost]
	localhost: starting namenode, logging to /usr/local/hadoop/logs/hadoop-hduser-namenode-enlighterCOM.out
	localhost: starting datanode, logging to /usr/local/hadoop/logs/hadoop-hduser-datanode-enlighterCOM.out
	Starting secondary namenodes [0.0.0.0]
	0.0.0.0: starting secondarynamenode, logging to /usr/local/hadoop/logs/hadoop-hduser-secondarynamenode-enlighterCOM.out
	16/03/13 09:59:05 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
	starting yarn daemons
	starting resourcemanager, logging to /usr/local/hadoop/logs/yarn-hduser-resourcemanager-enlighterCOM.out
	localhost: starting nodemanager, logging to /usr/local/hadoop/logs/yarn-hduser-nodemanager-enlighterCOM.out

We can check if it's really up and running:

	hduser@laptop ~ $ jps
	20512 NodeManager
	20404 ResourceManager
	20821 Jps
	19930 NameNode
	20235 SecondaryNameNode

The output means that we now have a functional instance of Hadoop running on our VPS (Virtual private server).

Another way to check is using **netstat**:

	hduser@laptop:~$ netstat -plten | grep java
	(Not all processes could be identified, non-owned process info will not be shown, you would have to be root to see it all.)
	tcp        0      0 127.0.0.1:54310         0.0.0.0:*               LISTEN      1001       942049      19930/java      
	tcp        0      0 0.0.0.0:50090           0.0.0.0:*               LISTEN      1001       951307      20235/java      
	tcp        0      0 0.0.0.0:50070           0.0.0.0:*               LISTEN      1001       942032      19930/java      
	tcp6       0      0 :::8031                 :::*                    LISTEN      1001       951474      20404/java      
	tcp6       0      0 :::8032                 :::*                    LISTEN      1001       951488      20404/java      
	tcp6       0      0 :::8033                 :::*                    LISTEN      1001       952317      20404/java      
	tcp6       0      0 :::8040                 :::*                    LISTEN      1001       950970      20512/java      
	tcp6       0      0 :::8042                 :::*                    LISTEN      1001       954614      20512/java      
	tcp6       0      0 :::41427                :::*                    LISTEN      1001       952297      20512/java      
	tcp6       0      0 :::8088                 :::*                    LISTEN      1001       953476      20404/java      
	tcp6       0      0 :::8030                 :::*                    LISTEN      1001       951484      20404/java

##Stopping Hadoop
	$ pwd
	/usr/local/hadoop/sbin

	$ ls
	distribute-exclude.sh  httpfs.sh                start-all.sh         start-yarn.cmd    stop-dfs.cmd        yarn-daemon.sh
	hadoop-daemon.sh       mr-jobhistory-daemon.sh  start-balancer.sh    start-yarn.sh     stop-dfs.sh         yarn-daemons.sh
	hadoop-daemons.sh      refresh-namenodes.sh     start-dfs.cmd        stop-all.cmd      stop-secure-dns.sh
	hdfs-config.cmd        slaves.sh                start-dfs.sh         stop-all.sh       stop-yarn.cmd
	hdfs-config.sh         start-all.cmd            start-secure-dns.sh  stop-balancer.sh  stop-yarn.sh

We run **stop-all.sh** or (**stop-dfs.sh** and **stop-yarn.sh**) to stop all the daemons running on our machine:

	hduser@laptop:/usr/local/hadoop/sbin$ pwd
	/usr/local/hadoop/sbin
	hduser@laptop:/usr/local/hadoop/sbin$ ls
	distribute-exclude.sh  httpfs.sh                start-all.cmd      start-secure-dns.sh  stop-balancer.sh    stop-yarn.sh
	hadoop-daemon.sh       kms.sh                   start-all.sh       start-yarn.cmd       stop-dfs.cmd        yarn-daemon.sh
	hadoop-daemons.sh      mr-jobhistory-daemon.sh  start-balancer.sh  start-yarn.sh        stop-dfs.sh         yarn-daemons.sh
	hdfs-config.cmd        refresh-namenodes.sh     start-dfs.cmd      stop-all.cmd         stop-secure-dns.sh
	hdfs-config.sh         slaves.sh                start-dfs.sh       stop-all.sh          stop-yarn.cmd
	hduser@laptop:/usr/local/hadoop/sbin$ 
	hduser@laptop:/usr/local/hadoop/sbin$ stop-all.sh
	This script is Deprecated. Instead use stop-dfs.sh and stop-yarn.sh
	15/04/18 15:46:31 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
	Stopping namenodes on [localhost]
	localhost: stopping namenode
	localhost: stopping datanode
	Stopping secondary namenodes [0.0.0.0]
	0.0.0.0: no secondarynamenode to stop
	15/04/18 15:46:59 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
	stopping yarn daemons
	stopping resourcemanager
	localhost: stopping nodemanager
	no proxyserver to stop

##Hadoop Web Interfaces
Let's start the Hadoop again and see its Web UI:

	hduser@laptop:/usr/local/hadoop/sbin$ start-all.sh


**http://localhost:50070/ - web UI of the NameNode daemon**

![Hadoop Web UI](http://www.bogotobogo.com/Hadoop/images/Install/Hadoop_50070.png)


Courtesy : bogotobogo.com