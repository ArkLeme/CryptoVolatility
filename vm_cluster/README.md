# Virtual machine cluster

*Warning: Work in progress*

---

This directory contains the configuration files to create a virtual machine cluster of Hadoop nodes.
The virtual machines are created using Vagrant and VirtualBox provider.

## How to use

You must install [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

To create the virtual machines, run the following command in this directory:

```bash
vagrant up
```

To destroy the virtual machines, run the following command in this directory:

```bash
vagrant destroy
```

To SSH into the namenode node, run the following command in this directory:

```bash
vagrant ssh namenode
```

To SSH into the datanode node, run the following command in this directory:

```bash
vagrant ssh datanode1
```