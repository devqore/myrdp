# virtual machine to build releases

Vagrant.configure("2") do |config|
    config.vm.box = "generic/ubuntu1604"
    config.vm.synced_folder ".", "/vagrant", type: 'nfs', nfs_udp: false, nfs_version: 4

    config.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "playbook.yml"
        ansible.limit = "all,localhost"
        ansible.verbose = true
    end
end