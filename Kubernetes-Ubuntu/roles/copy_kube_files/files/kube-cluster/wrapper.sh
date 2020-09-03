#!/bin/bash
ansible-playbook -i inventory_file kube-dependencie.yaml
ansible-playbook -i inventory_file master.yaml
ansible-playbook -i inventory_file workers.yaml
