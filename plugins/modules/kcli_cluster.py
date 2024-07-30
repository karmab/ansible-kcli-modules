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
    - kcli python package'''

EXAMPLES = '''
- name: Create a k8s cluster
  kcli_cluster:
    name: myclu
    type: generic
    parameyters:
     ctlplanes: 3
     workers: 2

- name: Delete that cluster
  kcli_cluster:
    name: myclu
    state: absent
'''

valid_cluster_types = ['aks', 'eks', 'generic', 'gke', 'kubeadm', 'k3s', 'microshift', 'openshift', 'rke2']


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
        "type": {"required": True, "type": "str", "choices": valid_cluster_types},
        "parameters": {"required": False, "type": "dict"},
    }
    module = AnsibleModule(argument_spec=argument_spec)
    client = module.params['client']
    overrides = module.params['parameters'] if module.params['parameters'] is not None else {}
    cluster_type = module.params['type']
    config = Kconfig(client=client, quiet=True)
    cluster = module.params['name']
    clusters = config.list_kubes()
    exists = cluster in clusters
    state = module.params['state']
    if state == 'present':
        if exists:
            meta = {'result': 'skipped'}
            changed, skipped = False, True
        else:
            meta = config.create_kube(cluster, cluster_type, overrides=overrides)
            changed, skipped = True, False
    else:
        if exists:
            meta = config.delete_kube(cluster, overrides=overrides)
            changed, skipped = True, False
        else:
            meta = {'result': 'skipped'}
            changed, skipped = False, True
    if 'result' in meta and meta['result'] == 'failure':
        module.fail_json(msg=meta['result'], **meta)
    else:
        module.exit_json(changed=changed, skipped=skipped, meta=meta)


if __name__ == '__main__':
    main()
