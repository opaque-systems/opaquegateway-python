# This script will install all pre-commit hooks and their dependencies
# Once the pre-commit hooks are installed, on each commit you should see a series of linter checks
# Note that this script should be run from the Opaque root directory.

# Exit on error
set -e 

echo "Installing pre-commit hooks and dependencies."
OPAQUE_DIR=$(git rev-parse --show-toplevel)


if [[ $(lsb_release -is) != "Ubuntu" ]]; then 
	echo "Unsupported OS distribution. This script currently only works on Ubuntu."
	exit 1
fi

if [[ $(lsb_release -rs) != "20.04" ]]; then 
    echo "This script has only been tested on Ubuntu 20.04, and is not guaranteed to work on another OS version."
fi

# Install Go
# cd $OPAQUE_DIR/ci-cd/build/requirements/mp
# ./setup.sh --skip-redis
# 
# export PATH=$PATH:/usr/local/go/bin
# if [[ "$(which go)" != "/usr/local/go/bin/go" ]]
# then
#     echo "Find your Go installation by manually sourcing your bashrc then typing `which go`, and add it to your $PATH: `export PATH=$PATH:$(dirname $(which go))`. Then re-run this script."
#     exit 1
# fi
# go_installation=$(dirname $(which go))

# Install dependencies in /tmp directory
# cd /tmp

# Install golangci-lint, a Go linter
# echo "Installing golangci-lint at $go_installation"
# curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sudo sh -s -- -b $go_installation v1.53.2

# Install clang-format for C++ linting
# Need >= version 14 for `QualifierAlignment`, but the version should match the 
# version of clang found in install_reqs.sh
# sudo add-apt-repository 'deb http://apt.llvm.org/focal/ llvm-toolchain-focal-15 main'
# sudo apt-get update
# sudo apt-get -y install clang-format-15
# sudo update-alternatives --install /usr/bin/clang-format clang-format /usr/bin/clang-format-15 100
# sudo update-alternatives --set clang-format /usr/bin/clang-format-15

# Install Java for Scala linting
# sudo apt-get -y install openjdk-8-jdk
# 
# # Install coursier and scalafmt for Scala linting
# curl -sfL https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux.gz | gzip -d > cs
# chmod +x cs
# ./cs setup
# COURSIER_BIN=~/.local/share/coursier/bin
# echo "export PATH=$PATH:$COURSIER_BIN" >> ~/.bashrc
# rm cs
# 
# export PATH=$PATH:$COURSIER_BIN
# cs install scalafmt:3.6.1

# Install actionlint to lint GitHub Actions files
go install github.com/rhysd/actionlint/cmd/actionlint@v1.6.19

# actionlint uses shellcheck to validate bash within a workflow
sudo apt-get install shellcheck

# Install pre-commit
pip3 install pre-commit

# Install pre-commit hooks
cd $OPAQUE_DIR
pre-commit install
