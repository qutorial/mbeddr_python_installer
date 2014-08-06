#!/bin/sh



# !   RIGHT CLICK THE LINK AND SELECT "SAVE AS"   !

# !  Alternatively, select File Menu->"Save As"  !



UNAME=`uname`
PYTHON=`which python3`
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

if [ "$?" -ne 0 ]; then
  echo "Please, install Python 3. Find more instructions here:"
  echo "http://mbeddr.fortiss.org/download/prereq/"
  exit 1
fi

if [ "${UNAME}" = "Linux" ]; then
  mi=`mktemp` && wget --no-cache -nv $URL -O $mi && python3 $mi; 
  res=$?;
  rm $mi;
  exit $res;
fi

if [[ "${UNAME}" == CYGWIN* ]]; then
  mi=`mktemp` && wget --no-cache -nv $URL -O $mi && python3 $mi; 
  res=$?;
  rm $mi;
  exit $res;
fi

if [ "${UNAME}" = "Darwin" ]; then
  mi=`mktemp /tmp/mbeddr_install.py.XXXXX` && curl -L  $URL -o $mi && python3 $mi;
  res=$?;
  rm $mi;
  exit $res;
fi

  


