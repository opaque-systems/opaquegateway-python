# This script will install all pre-commit hooks and their dependencies
# Once the pre-commit hooks are installed, on each commit you should see a series of linter checks
# Note that this script should be run from the Opaque root directory.

# Exit on error
set -e 

echo "Installing pre-commit hooks and dependencies."
PROJECT_ROOT_DIR=$(git rev-parse --show-toplevel)


if [[ $(lsb_release -is) != "Ubuntu" ]]; then 
	echo "Unsupported OS distribution. This script currently only works on Ubuntu."
	exit 1
fi

if [[ $(lsb_release -rs) != "20.04" ]]; then 
    echo "This script has only been tested on Ubuntu 20.04, and is not guaranteed to work on another OS version."
fi

# Install actionlint to lint GitHub Actions files
go install github.com/rhysd/actionlint/cmd/actionlint@v1.6.19

# actionlint uses shellcheck to validate bash within a workflow
sudo apt-get install shellcheck

# Install pre-commit
pip3 install pre-commit

# Install pre-commit hooks
cd $PROJECT_ROOT_DIR
pre-commit install
