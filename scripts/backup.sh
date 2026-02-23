#!/bin/bash
set -e

STAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$STAMP"
mkdir -p "$BACKUP_DIR"

cp -r data/vectordb "$BACKUP_DIR/" 2>/dev/null || true
cp -r data/uploads "$BACKUP_DIR/" 2>/dev/null || true

echo "Backup complete: $BACKUP_DIR"
