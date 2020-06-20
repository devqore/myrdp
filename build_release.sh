#!/usr/bin/env bash
vagrant up --provider=libvirt --provision
vagrant ssh -c "cd /vagrant && /vagrant/freeze.sh"
vagrant halt
