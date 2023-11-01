import json
from app.crypto import CryptoKey
from app.hosts import Hosts, Groups
from app.database import Database
from os.path import expanduser

passpharse = None

db = Database(f'sqlite:///{expanduser("~")}/.config/myrdp/myrdp.sqlite')
db.update()
ck = CryptoKey()
ck.load(
    f'{expanduser("~")}/.config/myrdp/private.key',
    passphrase=passpharse
)
hosts = Hosts(db, ck)
groups = Groups(db, ck)

config = {'groups': [], 'hosts': []}

for group in hosts.getGroupsList():
    config['groups'].append(
        groups.getFormattedValues(group, ['name', 'default_user_name', 'default_password'])
    )

for host in hosts.getAllHostsNames():
    config['hosts'].append(hosts.getFormattedValues(
        host, ['group', 'name', 'address', 'user', 'password'])
    )


print(json.dumps(config, ensure_ascii=False, indent=2))
