#!/bin/bash
# Convert draw.io files to PNG format
#
# Usage:
#   ./convert-drawio-to-png.sh file1.drawio [file2.drawio ...]
#
# Options (via environment variables):
#   DRAWIO_SCALE - Scale factor (default: 2)
#   DRAWIO_FORMAT - Output format: png, jpg, svg, pdf (default: png)
#   DRAWIO_TRANSPARENT - Enable transparency: 1 or 0 (default: 1)
#
# Requirements:
#   - draw.io desktop app (provides 'drawio' CLI)
#   - macOS: brew install --cask drawio
#   - Linux: Download from https://github.com/jgraph/drawio-desktop/releases

set -e

# Configuration with defaults
SCALE="${DRAWIO_SCALE:-2}"
FORMAT="${DRAWIO_FORMAT:-png}"
TRANSPARENT="${DRAWIO_TRANSPARENT:-1}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print usage
usage() {
    echo "Usage: $0 file1.drawio [file2.drawio ...]"
    echo ""
    echo "Environment variables:"
    echo "  DRAWIO_SCALE       Scale factor (default: 2)"
    echo "  DRAWIO_FORMAT      Output format: png, jpg, svg, pdf (default: png)"
    echo "  DRAWIO_TRANSPARENT Enable transparency: 1 or 0 (default: 1)"
    exit 1
}

# Check if drawio CLI is available
check_drawio() {
    if ! command -v drawio &> /dev/null; then
        echo -e "${RED}Error: drawio CLI is not installed.${NC}"
        echo ""
        echo "Installation instructions:"
        echo "  macOS:  brew install --cask drawio"
        echo "  Linux:  Download from https://github.com/jgraph/drawio-desktop/releases"
        exit 1
    fi
}

# Convert a single file
convert_file() {
    local input_file="$1"
    local output_file="${input_file}.${FORMAT}"

    # Build drawio command options
    local opts="-x -f ${FORMAT} -s ${SCALE}"

    if [ "${TRANSPARENT}" = "1" ] && [ "${FORMAT}" = "png" ]; then
        opts="${opts} -t"
    fi

    echo -e "${YELLOW}Converting:${NC} ${input_file}"

    # Run drawio export (suppress stderr warnings)
    if drawio ${opts} -o "${output_file}" "${input_file}" 2>/dev/null; then
        echo -e "${GREEN}  -> ${output_file}${NC}"

        # Add to git staging if in a git repository
        if git rev-parse --is-inside-work-tree &>/dev/null; then
            git add "${output_file}"
            echo -e "  ${GREEN}Added to git staging${NC}"
        fi

        return 0
    else
        echo -e "${RED}  Failed to convert ${input_file}${NC}"
        return 1
    fi
}

# Main function
main() {
    # Check arguments
    if [ $# -eq 0 ]; then
        usage
    fi

    # Check drawio CLI
    check_drawio

    local success_count=0
    local fail_count=0

    # Process each file
    for file in "$@"; do
        # Check if file exists
        if [ ! -f "${file}" ]; then
            echo -e "${RED}Error: File not found: ${file}${NC}"
            ((fail_count++))
            continue
        fi

        # Check if file is a .drawio file
        if [[ ! "${file}" =~ \.drawio$ ]]; then
            echo -e "${YELLOW}Warning: Skipping non-.drawio file: ${file}${NC}"
            continue
        fi

        # Convert file
        if convert_file "${file}"; then
            ((success_count++))
        else
            ((fail_count++))
        fi
    done

    # Summary
    echo ""
    echo -e "${GREEN}Converted: ${success_count}${NC}"
    if [ ${fail_count} -gt 0 ]; then
        echo -e "${RED}Failed: ${fail_count}${NC}"
        exit 1
    fi
}

main "$@"
