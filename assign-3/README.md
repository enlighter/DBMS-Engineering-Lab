# Instructions for setting up a Django environment with Mariadb database backend


## Prerequisites

To get started, you will need a clean Ubuntu 14.04 server instance 
with a non-root user set up.  The non-root user must be configured with `sudo` privileges.  Learn how to set this up by following our [initial server setup guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-14-04).

When you are ready to continue, read on.

<div data-unique="install-the-components-from-the-ubuntu-repositories" name="install-the-components-from-the-ubuntu-repositories"></div>

## Install the Components from the Ubuntu Repositories

Our first step will be install all of the pieces that we need from the repositories.  We will install `pip`,
 the Python package manager, in order to install and manage our Python 
components.  We will also install the database software and the 
associated libraries required to interact with them.

We will cover both MySQL and MariaDB below, so choose the section associated with the DBMS you'd like to use.

### MariaDB

If you prefer MariaDB, you can follow the instructions below to 
install it and perform the necessary initial configuration.  Install the
 packages from the repositories by typing:

    sudo apt-get update
    sudo apt-get install python-pip python-dev mariadb-server libmariadbclient-dev libssl-dev

You will be asked to select and confirm a password for the administrative MariaDB account.

You can then run through a simple security script by running:

    sudo mysql_secure_installation

You'll be asked for the administrative password you set for MariaDB 
during installation.  Afterwards, you'll be asked a series of questions.
  Besides the first question, asking you to choose another 
administrative password, select yes for each question.

With the installation and initial database configuration out of the 
way, we can move on to create our database and database user.

<div data-unique="create-a-database-and-database-user" name="create-a-database-and-database-user"></div>

## Create a Database and Database User

The remainder of this guide can be followed as-is regardless of whether you installed MySQL or MariaDB.

We can start by logging into an interactive session with our database
 software by typing the following (the command is the same regardless of
 which database software you are using):

    mysql -u root -p

You will be prompted for the administrative password you selected during installation.  Afterwards, you will be given a prompt.

First, we will create a database for our Django project.  Each 
project should have its own isolated database for security reasons.  We 
will call our database `<span class="highlight">myproject</span>`
 in this guide, but it's always better to select something more 
descriptive.  We'll set the default type for the database to UTF-8, 
which is what Django expects:

    CREATE DATABASE <span class="highlight">myproject</span> CHARACTER SET UTF8;

Remember to end all commands at an SQL prompt with a semicolon.

Next, we will create a database user which we will use to connect to 
and interact with the database.  Set the password to something strong 
and secure:

    CREATE USER <span class="highlight">myprojectuser</span>@localhost IDENTIFIED BY '<span class="highlight">password</span>';

Now, all we need to do is give our database user access rights to the database we created:

    GRANT ALL PRIVILEGES ON <span class="highlight">myproject</span>.* TO <span class="highlight">myprojectuser</span>@localhost;

Flush the changes so that they will be available during the current session:

    FLUSH PRIVILEGES;

Exit the SQL prompt to get back to your regular shell session:

    exit

## Install Django within a Virtual Environment

Now that our database is set up, we can install Django.  For better 
flexibility, we will install Django and all of its dependencies within a
 Python virtual environment.

You can get the `virtualenv` package that allows you to create these environments by typing:

    sudo pip install virtualenv

Make a directory to hold your Django project.  Move into the directory afterwards:

    mkdir ~/<span class="highlight">myproject</span>
    cd ~/<span class="highlight">myproject</span>

We can create a virtual environment to store our Django project's Python requirements by typing:

    virtualenv <span class="highlight">myprojectenv</span>

This will install a local copy of Python and `pip` into a directory called `<span class="highlight">myprojectenv</span>` within your project directory.

Before we install applications within the virtual environment, we need to activate it. You can do so by typing:

    source <span class="highlight">myprojectenv</span>/bin/activate

Your prompt will change to indicate that you are now operating within the virtual environment. It will look something like this `(<span class="highlight">myprojectenv</span>)<span class="highlight">user</span>@<span class="highlight">host</span>:~/<span class="highlight">myproject</span>$`.

Once your virtual environment is active, you can install Django with `pip`.  We will also install the `mysqlclient` package that will allow us to use the database we configured:

    pip install django mysqlclient

We can now start a Django project within our `myproject` 
directory.  This will create a child directory of the same name to hold 
the code itself, and will create a management script within the current 
directory.  Make sure to add the dot at the end of the command so that 
this is set up correctly:

    django-admin.py startproject <span class="highlight">myproject</span> .<div data-unique="configure-the-django-database-settings" name="configure-the-django-database-settings"></div>

## Configure the Django Database Settings

Now that we have a project, we need to configure it to use the database we created.

Open the main Django project settings file located within the child project directory:

    nano ~/<span class="highlight">myproject</span>/<span class="highlight">myproject</span>/settings.py

Towards the bottom of the file, you will see a `DATABASES` section that looks like this:

    . . .

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    . . .

This is currently configured to use SQLite as a database.  We need to
 change this so that our MySQL/MariaDB database is used instead.

First, change the engine so that it points to the `mysql` backend instead of the `sqlite3` backend.  For the `NAME`, use the name of your database (`<span class="highlight">myproject</span>`
 in our example).  We also need to add login credentials.  We need the 
username, password, and host to connect to.  We'll add and leave blank 
the port option so that the default is selected:

    . . .

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.<span class="highlight">mysql</span>',
            'NAME': '<span class="highlight">myproject</span>',
            'USER': '<span class="highlight">myprojectuser</span>',
            'PASSWORD': '<span class="highlight">password</span>',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    . . .

When you are finished, save and close the file.

<div data-unique="migrate-the-database-and-test-your-project" name="migrate-the-database-and-test-your-project"></div>

## Migrate the Database and Test your Project

Now that the Django settings are configured, we can migrate our data structures to our database and test out the server.

We can begin by creating and applying migrations to our database.  
Since we don't have any actual data yet, this will simply set up the 
initial database structure:

    cd ~/<span class="highlight">myproject</span>
    python manage.py makemigrations
    python manage.py migrate

After creating the database structure, we can create an administrative account by typing:

    python manage.py createsuperuser

You will be asked to select a username, provide an email address, and choose and confirm a password for the account.

Once you have an admin account set up, you can test that your 
database is performing correctly by starting up the Django development 
server:

    python manage.py runserver 0.0.0.0:8000

In your web browser, visit your server's domain name or IP address followed by `:8000` to reach default Django root page:

    http://server_domain_or_IP:8000
    localhost:8000 in our case

You should see the default index page:

Append `/admin` to the end of the URL and you should be able to access the login screen to the admin interface:

Enter the username and password you just created using the `createsuperuser` command.  You will then be taken to the admin interface:

When you're done investigating, you can stop the development server by hitting CTRL-C in your terminal window.

By accessing the admin interface, we have confirmed that our database
 has stored our user account information and that it can be 
appropriately accessed.
