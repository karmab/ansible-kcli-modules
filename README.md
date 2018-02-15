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
      install_kcli: no
    - role: hello-underworld
```

Because the role is referenced, the `hello-underworld` role is able to make use of the kcli modules

### Module parameters

install_kcli
> Set to true, if you want kcli installed. Defaults to false. Will install via `yum` (only for fedora)

## License

Apache V2
