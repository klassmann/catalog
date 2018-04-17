# Udacity Catalog Project

## Table of Contents

- [About this project](#about)
- [Using with Vagrant](#using-vagrant)
- [Using with local environment](#using-local)
- [Important Notes and Common Issues](#common-issues)
- [License](#license)


<a name="about"></a>
## About this project
This project was made for Udacity Full-Stack Web Developer nanodegree. The goal is to provide a catalog application in Flask with CRUD, Authentication, and Authorization with Google, and a basic API endpoint to get the entire catalog of items.

## Features
- [x] Categories - CRUD
- [x] Item - CRUD
- [x] Google Authentication and Authorization
- [x] CSRF

<a name="using-vagrant"></a>
## Using with Vagrant

### Requirements
- [Vagrant](https://www.vagrantup.com/) (Tested with Vagrant 2.0.2)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (Tested with VirtualBox 5.2.4)

### Setup Vagrant environment
Inside the project folder, use this command for setup the `vagrant` environment:
```bash
vagrant up
```
This command setups the vagrant and all the requirements for the project, when you log in Vagrant, you will have the correct Python version and all the `requirements.txt` installed.

### Enter in Vagrant environment
After setup Vagrant environment, you can log in via SSH:
```bash
vagrant ssh
```

### Change for the correct directory
```bash
cd /vagrant
```

### Create the database
```bash
python database.py
```

### Run the application
```bash
./run
```

<a name="using-local"></a>
## Using with local environment

### Requirements
- [Python 3](https://www.python.org/downloads/)

### Start installing the `requirements.txt`

```bash
pip3 install -r requirements.txt
```

### Create the database
```bash
python3 database.py
```

### Run the application
```bash
./run
```


## Use the following URL for open the application
[http://locahost:5000](http://locahost:5000)


<a name="common-issues"></a>
## Important Notes and Common Issues
- If you are not using **Vagrant**, make sure of installing all the *requirements* in your environment.
- The database `database.py` need to be initialized before running the application `app.py`.
- The database is empty, so, you need to fill up it with your data.
- You have to open the address [http://locahost:5000](http://locahost:5000) in your browser because this is the only URL that Google Sign-In is authorized for run.


<a name="license"></a>
## License
You can't use this project as your project for Udacity, but you can use for study purposes if you want.


