#!/usr/bin/python
# coding=utf-8

from ansible.module_utils.basic import AnsibleModule
from kvirt.config import Kconfig


DOCUMENTATION = '''
module: kcli_cluster
short_description: Handles K8s clusters using kcli
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
- name: Create a k8s cluster
  kcli_cluster:
    name: myclu
    type: kubeadm
    parameyters:
     ctlplanes: 3
     workers: 2

- name: Delete that cluster
  kcli_cluster:
    name: myclu
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
        "type": {"required": True, "type": "str", "choices": ['k3s', 'generic', 'kubeadm', 'okd', 'openshift']},
        "parameters": {"required": False, "type": "dict"},
    }
    module = AnsibleModule(argument_spec=argument_spec)
    client = module.params['client']
    overrides = module.params['parameters'] if module.params['parameters'] is not None else {}
    cluster_type = module.params['type']
    config = Kconfig(client=client, quiet=True)
    cluster = module.params['name']
    clusters = config.list_kubes()
    exists = True if cluster in clusters else False
    state = module.params['state']
    if state == 'present':
        if exists:
            changed = False
            skipped = True
            meta = {'result': 'skipped'}
        else:
            if cluster_type in ['okd', 'openshift']:
                meta = config.create_kube_openshift(cluster, overrides=overrides)
            elif cluster_type == 'k3s':
                meta = config.create_kube_k3s(cluster, overrides=overrides)
            else:
                meta = config.create_kube_generic(cluster, overrides=overrides)
            changed = True
            skipped = False
    else:
        if exists:
            meta = config.delete_kube(cluster, overrides=overrides)
            changed = True
            skipped = False
        else:
            changed = False
            skipped = True
            meta = {'result': 'skipped'}
    module.exit_json(changed=changed, skipped=skipped, meta=meta)


if __name__ == '__main__':
    main()
