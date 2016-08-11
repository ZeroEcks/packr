# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
VAGRANT_IP = "192.168.33.11"

Vagrant.require_version ">= 1.8.2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "bento/ubuntu-14.04"
  config.vm.network :private_network, ip: VAGRANT_IP
  config.ssh.insert_key = false
  config.vm.synced_folder ".", "/home/vagrant/packr", type: "nfs"

  # install Ansible within the VM and run our dev playbook
  config.vm.provision "ansible_local" do |ansible|
    ansible.install = true
    ansible.provisioning_path = "/home/vagrant/packr/ansible"
    ansible.playbook = "dev.yml"
  end

  # add localhost to Ansible inventory
  config.vm.provision "shell", inline: "echo 'localhost\n' >> /etc/ansible/hosts > /dev/null"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.name = "packr"
    vb.memory = "1024"
    vb.cpus = 2
  end
end

