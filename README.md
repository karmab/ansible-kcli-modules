# ansible-kcli-modules

Provides access to the latest release of the kcli modules. 

Include this role in a playbook, and any other plays, roles, and includes will have access to the modules.

The modules are found in the [library folder](./library)

## Requirements

- Ansible
- [kcli](https://github.com/karmab/kcli)

## Installation and use

Use the Galaxy client to install the role:

```
$ ansible-galaxy install karmabs.kcli-modules
```

Once installed, add it to a playbook:

```
---
- hosts: localhost
  remote_user: root
  roles:
    - role: karmab.kcli-modules
```

Because the role is referenced, the `hello-underworld` role is able to make use of the kcli modules
For single tasks, you can also use `import_role`


```
---
- hosts: localhost
  remote_user: root
  tasks:
    - import_role:
        name: karmab.kcli-modules
    - name: Create a vm
      kvirt_vm:
        name: taitibob
        state: present
        profile: CentOS-7-x86_64-GenericCloud.qcow2
        parameters:
         memory: 2048
```

### Role parameters

install_kcli
> Set to true, if you want kcli installed. Defaults to false. Will install via `yum` (only for fedora)


### Available modules

- kvirt_vm
- kvirt_info
- kvirt_plan
- kvirt_product

## License

Apache V2
