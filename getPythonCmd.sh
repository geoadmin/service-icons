#!/bin/bash

# Search for a compatible python version on the system or in the local path
# and return the path to it if found, otherwise returns nothing

set -euo pipefail

PYTHON_VERSION=${1-}
PYTHON_LOCAL_DIR=${2-}
PYTHON_MAJOR_VERSION=${PYTHON_VERSION%.*}

if [ -z "${PYTHON_VERSION}" ]; then
    >&2 echo "First parameter missing"
    exit 1
fi

# shellcheck disable=SC2086
for TMP_PYTHON_CMD in $(find ${PATH//:/ } ${PYTHON_LOCAL_DIR} -maxdepth 1 -executable -regextype sed -regex ".*/python3\.[0-9]*" 2> /dev/null | sort -V) ; do
    VERSION=$(${TMP_PYTHON_CMD} --version 2>&1 | awk  '{print $2}')
    if (( $(echo "${VERSION%.*} >= ${PYTHON_MAJOR_VERSION}" | bc -l) )); then
        # echo "Found compatible python version: ${VERSION}"
        SYSTEM_PYTHON_CMD=${TMP_PYTHON_CMD}
        break
    fi
done

echo "${SYSTEM_PYTHON_CMD-}"


