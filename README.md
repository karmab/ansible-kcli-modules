# ansible-kcli-modules

Provides access to the latest release of the kcli modules. 

Include this role in a playbook, and any other plays, roles, and includes will have access to the modules.

The modules are found [here](./plugins/modules)

## Requirements

- Ansible >= 2.9, it is recommended to download the latest version of [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).
- [kcli](https://github.com/karmab/kcli)

## Installation

Use the Ansible Galaxy client to install the latest version of the collection:

```
$ ansible-galaxy collection install karmab.kcli
```

or using `requirements.yml`:

```yaml
collections:
  - name: karmab.kcli
```

## How to use

The following modules are available

- kcli_vm
- kcli_info
- kcli_plan
- kcli_product
- kcli_cluster

For all of them, apart from mandatory parameters, you can provide a parameters dict with all your parameters

#### kcli_vm

```yaml
  - name: Create vm tahitibob from centos8stream image and forcing memory to be 2G
    karmab.kcli.kcli_vm:
      name: tahitibob
      state: present
      image: centos8stream
      parameters:
       memory: 2048
    register: result
  - debug: var=result
```

|Parameter   |Required |Default Value         |
|------------|---------|----------------------|
|name        |true     |                      |
|client      |false    |                      |
|image       |false    |                      |
|profile     |false    |                      |
|parameters  |false    |Empty dict            |

#### kcli_info

```yaml
- name: Get ip from vm tahitibob
  karmab.kcli.kcli_info:
    name: tahitibob
  register: result
- debug: var=result.meta.ip
```

|Parameter   |Required |Default Value         |
|------------|---------|----------------------|
|name        |true     |                      |
|client      |false    |                      |
|fields      |false    |Empty list            |
|parameters  |false    |Empty dict            |

#### kcli_plan

```yaml
- name: Launch plan wilibonka from plan file myplan.yml
  karmab.kcli.kcli_plan:
    name: wilibonka
    inputfile: myplan.yml
  register: result
- debug: var=result
```

|Parameter   |Required |Default Value         |
|------------|---------|----------------------|
|name        |true     |                      |
|client      |false    |                      |
|inputfile   |false    |                      |
|parameters  |false    |Empty dict            |

#### kcli_cluster

```yaml
- name: Create a k8s cluster
  karmab.kcli.kcli_cluster:
    state: absent
    name: myclu
    type: kubeadm
    parameters:
     ctlplanes: 3
     workers: 2
  register: result
- debug: var=result
```

|Parameter   |Required |Default Value         |
|------------|---------|----------------------|
|name        |true     |                      |
|client      |false    |                      |
|type        |false    |generic               |
|parameters  |false    |Empty dict            |

#### kcli_product

```yaml
- name: Deploy product origin, provided there is a kcli repo providing it
  karmab.kcli.kcli_product:
    name: microshift
    product: microshift
```

|Parameter   |Required |Default Value         |
|------------|---------|----------------------|
|name        |true     |                      |
|client      |false    |                      |
|product     |true     |                      |
|repo        |false    |                      |
|parameters  |false    |Empty dict            |


## License

Apache V2
