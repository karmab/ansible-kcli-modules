#!/usr/bin/env python
# coding=utf-8

from ansible.module_utils.basic import AnsibleModule
from kvirt.config import Kconfig


DOCUMENTATION = '''
module: kcli_plan
short_description: Deploy a plan using kcli
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
- name: Deploy origin
  kcli_plan:
    name: my_plan
    inputfile: my_plan.yml

- name: Delete that plan
  kcli_plan:
    name: my_plan
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
        "inputfile": {"required": False, "type": "str"},
        "parameters": {"required": False, "type": "dict"},
    }
    module = AnsibleModule(argument_spec=argument_spec)
    client = module.params['client']
    config = Kconfig(client, quiet=True)
    name = module.params['name']
    inputfile = module.params['inputfile']
    state = module.params['state']
    if state == 'present':
        overrides = module.params['parameters'] or {}
        meta = config.plan(name, inputfile=inputfile, overrides=overrides)
        changed = True if 'newvms' in meta else False
        skipped = False
    else:
        meta = config.plan(name, delete=True)
        changed = True if 'deletedvms' in meta else False
        skipped = False
    if 'result' in meta and meta['result'] == 'failure':
        module.fail_json(msg=meta['result'], **meta)
    else:
        module.exit_json(changed=changed, skipped=skipped, meta=meta)


if __name__ == '__main__':
    main()
