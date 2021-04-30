#!/usr/bin/env bash

how_to_usage() {
	echo "$(basename $0) INSTALL_DIR BROWSER_PATH (TEMP_DIR)"
	echo '    INSTALL_DIR : Installation directory path'
	echo '    BROWSER_PATH: "Chrome" browser installation directory path'
	echo '    TEMP_DIR    : Temporary workspace directory path'
}

install() {
	export BROWSER_PATH=$(readlink -f "$2")
	if [ ! -f "${BROWSER_PATH}" ]; then
		echo error, browser not found.
		exit 101
	fi

	if [ "$3" = "" ]; then
		export TEMP_DIR=$(mktemp -d $(basename "$0" .sh)-XXXXXX)
	elif [[ "$3" =~ X{6} ]]; then
		export TEMP_DIR=$(mktemp -d "$3")
	else
		export TEMP_DIR=$3
		mkdir -p "${TEMP_DIR}"
	fi
	trap 'rm -rf "${TEMP_DIR}"' EXIT
	export TEMP_DIR=$(readlink -f "${TEMP_DIR}")

	curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o "${TEMP_DIR}/get-pip.py"
	mkdir "${TEMP_DIR}/pip"
	python "${TEMP_DIR}/get-pip.py" --no-cache-dir --upgrade --target "${TEMP_DIR}/pip" --log "${TEMP_DIR}/install-pip.log"
	export PYTHONPATH=$PYTHONPATH:${TEMP_DIR}/pip

	mkdir -p "$1"
	export INSTALL_DIR=$(readlink -f "$1")

	python -m pip install selenium --no-cache-dir --upgrade --target "${INSTALL_DIR}" --log "${TEMP_DIR}/install-selenium.log"
	export BROWSER_VERSION=$("${BROWSER_PATH}" --version | sed -r 's/[^0-9]+([0-9]+\.[0-9]+).+/\1/g')
	python -m pip install chromedriver-binary~=${BROWSER_VERSION} --no-cache-dir --upgrade --target "${INSTALL_DIR}" --log "${TEMP_DIR}/install-chromedriver.log"
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
	if [ "$2" = '' ]; then
		how_to_usage
		exit 12
	fi

	install $*
	exit 0
}
main $*
