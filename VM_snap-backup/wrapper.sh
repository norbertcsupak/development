#!/bin/bash
#
# Get the list of all domains, active and inactive, iterate over the list with the main backup-script such that all domains get backed up.
test="$(virsh list --all | grep "running" | awk {'print $2'} )"
while read -r line; do
    bash vm_backup.sh  /tmp/backup  "$line" 2 snap
done <<< "$test"

# date converter 
# virsh snapshot-list  master  | awk '{print $2"."$3}' | tail -n +3 | head -n -1  | sed 's/://g'

