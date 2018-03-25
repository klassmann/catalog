# Udacity Catalog Project

## Table of Contents

- [About this project](#about)
- [Using with Vagrant](#using-vagrant)
- [Using with local environment](#using-local)
- [License](#license)


## About this project
This project was made for Udacity Full-Stack Web Developer nanodegree. The goal is provide a catalog application in Flask with CRUD, Authentication and Authorization with Google and other providers and a basic API endpoint for get the entire catalog of items.

<a name="using-vagrant"></a>
## Using with Vagrant

### Requirements
- Vagrant
- VirtualBox

### Setup Vagrant
Inside the project folder, use this command for setup the `vagrant` environment:
```bash
vagrant up
```
This command setup the vagrant and all the requirements for the project.

After the installing and the setup of the vagrant you need to enter in the vagrant environment:
```bash
vagrant ssh
```

And now you can run the application:
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

### Syncronize the database
```bash
./syncdatabase
```

### Run the application
```bash
./run
```

<a name="license"></a>
## License
You can't use this project as your project for Udacity, but you can use for study purposes if you want.


