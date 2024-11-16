
#
# mlocate
#
# Check that mlocate is installed, as its required later.
# locate is used to allow for diffrences in install location
# between systems and are faster than find in the common case.
# NOTE: update db and check prune patterns if trouble shooting
if [ ! "$(command -v locate)" ]; then
    echo "\033[1;41mERROR: Please install 'plocate'\033[0m"
    return 0
fi

# 'venv' setup and activation
VENV_NAME=".venv"
# TODO: trigger on changes to requirements.txt to stay up to date.
# NOTE: to slow to always run
if [ ! -d "$VENV_NAME" ]; then
    echo -e "Python environment setup"
    python3 -m venv $VENV_NAME
    python3 -m ensurepip --default-pip
    $VENV_NAME/bin/python3 -m pip install setuptools wheel
    $VENV_NAME/bin/python3 -m pip install -r requirements.txt
fi
# TODO: Add explicit python min version and check
source $VENV_NAME/bin/activate
python3 --version


#
# Cleanup
#
unset VENV_NAME
