#!/bin/sh

set -ex

cat << EOF >> image-builder/images/capi/ansible/roles/providers/tasks/qemu.yml

- name: Symlink /run/systemd/resolve/resolv.conf to /etc/resolv.conf
  file:
    src:   /run/systemd/resolve/resolv.conf
    dest:  /etc/resolv.conf
    mode: 0644
    state: link
    force: yes
  when: ansible_os_family == "Debian"
EOF
