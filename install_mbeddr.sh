#!/bin/sh



# !   RIGHT CLICK THE LINK AND SELECT "SAVE AS"   !

# !  Alternatively, select File Menu->"Save As"  !



UNAME=`uname`
BRANCH=master
SCRIPTNAME=$0


if [ $# = 1 ]; then 
  if [ $1 = latest ]; then 
    BRANCH=cuttingedge
  else
    echo "Usage: $SCRIPTNAME [latest]"
    echo " latest - install mbeddr from the master branch, otherwise from fortiss_stable branch "
    exit 2
  fi  
fi

URL="https://github.com/qutorial/mbeddr_python_installer/raw/"$BRANCH"/mbeddr_install.py"

PYTHON=""

arr="python3
python3.4
python3.3
python3.2"

for py in $arr
do
  PYTHON=`which $py`
  if [ "$?" -eq 0 ]; then
    break;
  fi
done

PYTHON=`which $PYTHON`
if [ "$?" -ne 0 ]; then
  echo "Please, install Python 3. Find more instructions here:"
  echo "http://mbeddr.fortiss.org/download/prereq/"
  exit 1
fi

echo "Using Python at: $PYTHON"

if [ "${UNAME}" = "Linux" ]; then
  mi=`mktemp` && wget --no-cache -q $URL -O $mi && $PYTHON $mi; 
  res=$?;
  rm $mi;
  exit $res;
fi

if [[ "${UNAME}" == CYGWIN* ]]; then
  mi=`mktemp` && wget --no-cache -q $URL -O $mi && $PYTHON $mi; 
  res=$?;
  rm $mi;
  exit $res;
fi

if [ "${UNAME}" = "Darwin" ]; then
  mi=`mktemp /tmp/mbeddr_install.py.XXXXX` && curl -L  $URL -o $mi && $PYTHON $mi;
  res=$?;
  rm $mi;
  exit $res;
fi

  


