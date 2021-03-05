#!/bin/sh

set -ex

cat << EOF >> image-builder/images/capi/ansible/roles/providers/tasks/qemu.yml

- name: Make cloud-init manage /etc/hosts
  lineinfile:
    path: /etc/cloud/cloud.cfg
    line: 'manage_etc_hosts: True'
  when: ansible_os_family == "Debian"
EOF
