# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  Vagrant::DEFAULT_SERVER_URL.replace('https://vagrantcloud.com')
  config.vm.box = "bento/ubuntu-16.04-i386"
  config.vm.box_version = "= 2.3.5"
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  # Work around disconnected virtual network cable.
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get -qqy update

    # Work around https://github.com/chef/bento/issues/661
    # apt-get -qqy upgrade
    DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade
    apt-get -qqy install make zip unzip
    apt-get -qqy install python3 python3-pip python3-virtualenv
    
    pip3 install --upgrade pip
    python3 -m virtualenv -p python3 env
    source env/bin/activate
    pip install -r /vagrant/requirements.txt
    echo "source env/bin/activate" >> .profile
    # pip3 install -r /vagrant/requirements.txt    
    
    vagrantTip="[35m[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant[m"
    echo -e $vagrantTip > /etc/motd
    echo "Done installing your virtual machine!"
  SHELL
end
