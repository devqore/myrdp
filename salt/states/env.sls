packages:
  pkg.installed:
    {% if grains['os'] == 'Ubuntu' %}
    - names:
      - binutils
      - python3-pyqt4
      - python3-virtualenv
      - python3-dev
      - virtualenv
      - kde-style-breeze-qt4  # additional style
    {% elif grains['os'] == 'Arch' %}
    - names:
      - python3-pyqt4
    {% endif %}

/opt/python3-venvs/myrdp:
  virtualenv.managed:
    - system_site_packages: False
    - requirements: /home/vagrant/myrdp/requirements-freeze.txt
    - python: /usr/bin/python3

pyqt4:
  module.run:
    - name: file.copy
    {% if grains['os'] == 'Ubuntu' %}
    - src: /usr/lib/python3/dist-packages/PyQt4
    {% elif grains['os'] == 'Arch' %}
    - src: /usr/lib/python3/site-packages/PyQt4
    {% endif %}
    - dst: /opt/python3-venvs/myrdp/lib/python3.5/site-packages/PyQt4
    - recurse: True
    - remove_existing: True

sip:
  cmd.run:
    {% if grains['os'] == 'Ubuntu' %}
    - name: cp /usr/lib/python3/dist-packages/sip* /opt/python3-venvs/myrdp/lib/python3.5/site-packages
    {% elif grains['os'] == 'Arch' %}
    - name: cp /usr/lib/python3/site-packages/sip* /opt/python3-venvs/myrdp/lib/python3/site-packages
    {% endif %}
