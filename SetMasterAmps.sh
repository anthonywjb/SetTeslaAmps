#!/bin/bash

# Exit on error in any command
set -o errexit -o pipefail

# Check arguments
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <numeric_value> <output_directory> <tesla_account_name>"
    exit 1
fi

AMP_VALUE="$1"
OUTPUT_DIR="$2"
ACCOUNT_NAME="$3"

# Validate numeric (integer or decimal, allows leading minus)
if ! [[ "$AMP_VALUE" =~ ^-?[0-9]+([.][0-9]+)?$ ]]; then
    echo "Error: <numeric_value> must be a valid number (e.g., 12, -3, 4.5)."
    exit 1
fi

# Create the directory if it doesn't exist
# -p makes it idempotent (no error if it already exists)
if ! mkdir -p "$OUTPUT_DIR"; then
    echo "Error: Could not create directory: $OUTPUT_DIR"
    exit 1
fi

# Verify directory is writable
if [ ! -w "$OUTPUT_DIR" ]; then
    echo "Error: Directory is not writable: $OUTPUT_DIR"
    exit 1
fi

# Write the value to MasterAmpControl.txt inside the target directory
MASTER_FILE="$OUTPUT_DIR/control.txt"

# Use a temporary file then move into place for atomic-ish write
TMP_FILE="$(mktemp "${OUTPUT_DIR%/}/.TempControl.txt.XXXXXX")"
echo "$AMP_VALUE" > "$TMP_FILE"
echo "$ACCOUNT_NAME" >> "$TMP_FILE"
mv -f "$TMP_FILE" "$MASTER_FILE"

echo "Created:"
echo "  - $MASTER_FILE"
