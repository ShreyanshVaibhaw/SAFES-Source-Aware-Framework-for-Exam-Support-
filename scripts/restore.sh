#!/bin/bash
set -e

BACKUP_DIR=$1
if [ -z "$BACKUP_DIR" ]; then
  echo "Usage: ./scripts/restore.sh <backup_directory>"
  exit 1
fi

cp -r "$BACKUP_DIR/vectordb" data/ 2>/dev/null || true
cp -r "$BACKUP_DIR/uploads" data/ 2>/dev/null || true

echo "Restore complete from: $BACKUP_DIR"
