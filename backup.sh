#!/bin/bash

# danny local, unlike the git includes the data dir (loads of other nearby stuff too)

# Source and destination directories
SOURCE_DIR="/home/danny/foaf-archive-support/"
DEST_DIR="/space/foaf-archive-support-rsync"

cp /home/danny/HKMS/postcraft/danny.ayers.name/entries/2024-08-14_video-enhancement.md /home/danny/foaf-archive-support/video-magic/docs/

# Use rsync to perform the backup
rsync -av --update "$SOURCE_DIR" "$DEST_DIR"

echo "Backup completed successfully."
