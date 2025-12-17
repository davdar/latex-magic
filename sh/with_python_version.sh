python_target_version=$1
shift
command="$@"

# echo $python_target_version
# echo $command

echo "...PROBING PYTHON ENVIRONMENT..."

echo "target python version is $python_target_version."

(command -v pyenv && pyenv --version) >/dev/null 2>&1 
pyenv_exists=$?

(command -v python3 && python3 --version) >/dev/null 2>&1 
python3_exists=$?

(command -v python && python --version) >/dev/null 2>&1 
python_exists=$?

if [ $pyenv_exists -eq 0 ]
then
  echo "pyenv exists and works."
else
  echo "pyenv does not exist or is broken."
fi

if [ $python3_exists -eq 0 ]
then
  echo "python3 exists and works."
else
  echo "python3 does not exist or is broken."
fi

if [ $python_exists -eq 0 ]
then
  echo "python exists and works."
else
  echo "python does not exist or is broken."
fi

if [ $pyenv_exists -ne 0 ] && [ $python3_exists -ne 0 ] && [ $python_exists -ne 0 ]
then
  echo "None of these exist: pyenv, python3, python."
  echo "Aborting."
  exit 1
fi

(PYENV_VERSION=$python_target_version pyenv which python >/dev/null 2>&1)
pyenv_target_version_exists=$?

use_pyenv=1

if [ $pyenv_target_version_exists -eq 0 ]
then
  echo "python target version $python_target_version exists in pyenv."
  use_pyenv=0
else
  echo "python target version $python_target_version doesn't exist in pyenv."
  echo "Make sure pyenv is installed, and then run this command"
  echo "to install the correct version of python in pyenv:"
  echo ""
  echo "    pyenv install $python_target_version"
  echo ""
  echo "Falling back to global python."
  echo "↓↓↓↓ WARNING ↓↓↓↓"
  echo "↓↓↓↓ WARNING ↓↓↓↓"
  echo "Things may not work when using a python or python3 version that isn't:"
  echo ""
  echo "    $python_target_version"
  echo ""
  echo "If the next command fails, you should install the correct version of python"
  echo "via pyenv as described above. If your global versions of python or python3"
  echo "match this version, then you should be fine, but this warning will still"
  echo "always appear until you set up the correct version with pyenv."
  echo "↑↑↑↑ WARNING ↑↑↑↑"
  echo "↑↑↑↑ WARNING ↑↑↑↑"
  # echo "would you like to install it?"
  # select yn in "Yes" "No"; do
  #     case $yn in
  #         Yes ) 
  #           echo "installing python version $python_target_version via pyenv"
  #           pyenv install $python_target_version
  #           use_pyenv=0
  #           break;;
  #         No ) 
  #           echo "falling back to global python"
  #           break;;
  #     esac
  # done
fi

if [ $use_pyenv -eq 0 ]
then
  echo "Using pyenv with version $python_target_version."
  echo "> (PYENV_VERSION=$python_target_version pyenv exec $command)"
  (PYENV_VERSION=$python_target_version pyenv exec $command)
else
  if [ $python3_exists -eq 0 ]
  then
    echo "> python3 --version"
    python3 --version
  fi
  if [ $python_exists -eq 0 ]
  then
    echo "> python --version"
    python --version
  fi
  echo "> $command"
  $command
fi
