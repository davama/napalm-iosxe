# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "rtr" do |iosxe|
    iosxe.vm.box = "csr1k"

    iosxe.vm.network :forwarded_port, guest: 830, host: "2223", id: 'ssh'
    iosxe.vm.network :forwarded_port, guest: 80, host: "2224", id: 'ssh'
    iosxe.vm.network :forwarded_port, guest: 443, host: "2225", id: 'ssh'
    iosxe.vm.network :forwarded_port, guest: 22, host: "2222", id: 'ssh'

    iosxe.vm.network "private_network", virtualbox__intnet: "link_1", ip: "10.0.1.21", auto_config: false
    iosxe.vm.network "private_network", virtualbox__intnet: "link_2", ip: "10.0.1.22", auto_config: false
    iosxe.vm.network "private_network", virtualbox__intnet: "link_3", ip: "10.0.1.23", auto_config: false
    iosxe.vm.network "private_network", virtualbox__intnet: "link_4", ip: "10.0.1.24", auto_config: false
  end

end
