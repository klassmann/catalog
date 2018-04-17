# Udacity Catalog Project

## Table of Contents

- [About this project](#about)
- [Using with Vagrant](#using-vagrant)
- [Using with local environment](#using-local)
- [License](#license)


## About this project
This project was made for Udacity Full-Stack Web Developer nanodegree. The goal is provide a catalog application in Flask with CRUD, Authentication and Authorization with Google, and a basic API endpoint for get the entire catalog of items.

<a name="using-vagrant"></a>
## Using with Vagrant

### Requirements
- Vagrant
- VirtualBox

### Setup Vagrant environment
Inside the project folder, use this command for setup the `vagrant` environment:
```bash
vagrant up
```
This command setup the vagrant and all the requirements for the project, when you log in Vagrant you have the correct Python version and all the `requirements.txt` installed.

### Enter in Vagrant machine
After setuping Vagrant machine, you can log in via SSH:
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
- Python 3

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

## Important Notes and Common Issues
- You are not using **Vagrant**, make sure of installing all the *requirements* in your environment.
- The database is empty, so, you need to fill up it with your own data.
- The database (database.py) need to be initialized before running the application (app.py).
- You need to open the address http://locahost:5000 in your browser, because this is the only URL that Google Sign-In is authorized for.


<a name="license"></a>
## License
You can't use this project as your project for Udacity, but you can use for study purposes if you want.


