#!/usr/bin/env bash

how_to_usage() {
	echo "$(basename $0) INSTALL_DIR (TEMP_DIR)"
	echo '    INSTALL_DIR : Installation directory path'
	echo '    TEMP_DIR    : Temporary workspace directory path'
}

install() {
	if [ "$2" = "" ]; then
		export TEMP_DIR=$(mktemp -d $(basename "$0" .sh)-XXXXXX)
	elif [[ "$2" =~ X{6} ]]; then
		export TEMP_DIR=$(mktemp -d "$2")
	else
		export TEMP_DIR=$2
		mkdir -p "${TEMP_DIR}"
	fi
	trap 'rm -rf "${TEMP_DIR}"' EXIT
	export TEMP_DIR=$(readlink -f "${TEMP_DIR}")

	curl https://bootstrap.pypa.io/pip/get-pip.py -o "${TEMP_DIR}/get-pip.py"
	mkdir "${TEMP_DIR}/pip"
	python "${TEMP_DIR}/get-pip.py" --no-cache-dir --upgrade --target "${TEMP_DIR}/pip" --log "${TEMP_DIR}/install-pip.log"
	export PYTHONPATH=$PYTHONPATH:${TEMP_DIR}/pip

	mkdir -p "$1"
	export INSTALL_DIR=$(readlink -f "$1")

	python -m pip install pyppeteer --no-cache-dir --upgrade --target "${INSTALL_DIR}" --log "${TEMP_DIR}/install-pyppeteer.log"
}

main() {
	if [ "$1" = '--help' ] || [ "$1" = '-h' ]; then
		how_to_usage
		exit 0
	fi
	if [ "$1" = '' ]; then
		how_to_usage
		exit 11
	fi

	install $*
	exit 0
}
main $*
