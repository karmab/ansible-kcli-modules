#!/usr/bin/python
# coding=utf-8

from ansible.module_utils.basic import AnsibleModule
from kvirt.config import Kconfig


DOCUMENTATION = '''
module: kcli_vm
short_description: Handles libvirt vms using kcli
description:
    - Longer description of the module
    - You might include instructions
version_added: "0.2"
author: "Karim Boumedhel, @karmab"
notes:
    - Details at https://github.com/karmab/kcli
requirements:
    - kcli python package you can grab from pypi'''

EXAMPLES = '''
- name: Create a vm from profile centos8stream
  kcli_vm:
    name: prout
    profile: centos8stream

- name: Create a vm from image centos8stream
  kcli_vm:
    name: prout
    image: centos8stream
    parameters:
     memory: 4096
     numcpus: 4
     cmds:
     - echo Welcome here > /etc/motd

- name: Delete that vm
  kcli_vm:
    name: prout
    state: absent
'''


def main():
    """

    """
    argument_spec = {
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
        "name": {"required": True, "type": "str"},
        "client": {"required": False, "type": "str"},
        "image": {"required": False, "type": "str"},
        "profile": {"required": False, "type": "str"},
        "parameters": {"required": False, "type": "dict"},
    }
    module = AnsibleModule(argument_spec=argument_spec)
    client = module.params['client']
    config = Kconfig(client=client, quiet=True)
    k = config.k
    name = module.params['name']
    exists = k.exists(name)
    state = module.params['state']
    if state == 'present':
        if exists:
            changed = False
            skipped = True
            meta = {'result': 'skipped'}
        else:
            image = module.params['image']
            profile = module.params['profile']
            if image is not None:
                profile = image
            elif profile is None:
                profile = 'kvirt'
                config.profiles[profile] = {}
            overrides = module.params['parameters'] if module.params['parameters'] is not None else {}
            meta = config.create_vm(name, profile, overrides=overrides)
            changed, skipped = True, False
    else:
        if exists:
            meta = k.delete(name)
            changed, skipped = True, False
        else:
            changed, skipped = False, True
            meta = {'result': 'skipped'}
    if 'result' in meta and meta['result'] == 'failure':
        module.fail_json(msg=meta['result'], **meta)
    else:
        module.exit_json(changed=changed, skipped=skipped, meta=meta)


if __name__ == '__main__':
    main()
