#!/bin/bash
#

BACKUPDEST="$1"
DOMAIN="$2"
MAXBACKUPS="$3"
BCKNAME="$4"
STYPE="$5"

if [ -z "$BACKUPDEST" -o -z "$DOMAIN" -o -z "$BCKNAME" ]; then
    echo "Usage: ./vm-backup <backup-folder> <domain> [max-backups] <backupname>"
    exit 1
fi

if [ -z "$MAXBACKUPS" ]; then
    MAXBACKUPS=6
fi

echo "Beginning backup for $DOMAIN"

#
# Generate the backup path
#
XML_SNAP_PATH="/var/lib/libvirt/qemu/snapshot"
BACKUPDATE=`date "+%Y-%m-%d.%H%M%S"`
BACKUPDOMAIN="$BACKUPDEST/$DOMAIN"
BACKUP="$BACKUPDOMAIN/$BACKUPDATE"
SNAPNAME="${BCKNAME}@`date '+%Y%m%d.%H%M'`"
mkdir -p "$BACKUP"

#
# Get the list of targets (disks) and the image paths.
#
TARGETS=`virsh domblklist "$DOMAIN" --details | grep ^file | awk '{print $3}'`
IMAGES=`virsh domblklist "$DOMAIN" --details | grep ^file | awk '{print $4}'`
#
# Create the snapshot.
#
DISKSPEC=""
for t in $TARGETS; do
    DISKSPEC="$DISKSPEC --diskspec $t,snapshot=external"
done
echo "The disk_specs are: $DISKSPEC"
virsh snapshot-create-as --domain "$DOMAIN" --name $SNAPNAME --atomic --disk-only $DISKSPEC>/dev/null
if [ $? -ne 0 ]; then
    echo "Failed to create snapshot for $DOMAIN"
    exit 1
fi
echo "The snapshot list: `virsh snapshot-list $DOMAIN`"
#
# Copy disk images
#
echo "Copy disk images:"

for t in $IMAGES; do
    NAME=`basename "$t"`
    echo "Copying image $t ... "
#    cp "$t" "$BACKUP"/"$NAME" 
    rsync -ah --progress $t "$BACKUP"/"$NAME"

done

#
# Merge changes back.
#


BACKUPIMAGES=`virsh domblklist "$DOMAIN" --details | grep ^file | awk '{print $4}'`
for t in $TARGETS; do
    echo "Merge the target (blockcomit): $t"
    virsh blockcommit "$DOMAIN" "$t" --active --pivot >/dev/null
    if [ $? -ne 0 ]; then
        echo "Could not merge changes for disk $t of $DOMAIN. VM may be in invalid state."
        exit 1
    fi
done

#
# Cleanup left over backup images.
#
##for t in $BACKUPIMAGES; do
##    rm -f "$t"
##done

#
# Dump the configuration information.
#
echo "Dump the configuration informations to : $BACKUP/$DOMAIN.xml"
virsh dumpxml "$DOMAIN" >"$BACKUP/$DOMAIN.xml"

#
# Cleanup older backups.
#
echo "Cleanup left over backup image"
LIST=`ls -r1 "$BACKUPDOMAIN" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}\.[0-9]+$'`
i=1
for b in $LIST; do
    echo "From snap list...: $b"
    if [ $i -gt "$MAXBACKUPS" ]; then
	xmltmp=`echo $b | sed -e 's/-//g'`
	XMLFILE=${xmltmp::-2}
	
        echo "Removing old backup "`basename $b`
        rm -rf "$BACKUPDOMAIN/$b"
	echo "Finding xml file based on date in /var/lib/libvirt/qemu/snapshot/$DOMAIN/: $XMLFILE"
	find /var/lib/libvirt/qemu/snapshot/$DOMAIN/ -maxdepth 1 -name "*$XMLFILE*" -print 
	echo "Removing old snapshot xml file ..."
	find /var/lib/libvirt/qemu/snapshot/$DOMAIN/ -maxdepth 1 -name "*$XMLFILE*" -exec rm -rf {} \;
    fi

    i=$[$i+1]
done

echo "Restarting libvirtd..."
systemctl  restart libvirtd
echo""
echo "Finished backup"
echo ""

