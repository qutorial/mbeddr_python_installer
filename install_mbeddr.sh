#!/bin/sh

UNAME=`uname`

PYTHON=`which python3`

if [ "$?" -ne 0 ]; then
  echo "Please, install Python 3. Find more instructions here:"
  echo "http://mbeddr.fortiss.org/download/prereq/"
  exit 1
fi

if [ "${UNAME}" = "Linux" ]; then
  mi=`mktemp` && wget --no-cache -nv https://github.com/qutorial/mbeddr_python_installer/raw/master/mbeddr_install.py -O $mi && python3 $mi; 
  res=$?;
  rm $mi;
  exit $res;
fi

if [[ "${UNAME}" == CYGWIN* ]]; then
  mi=`mktemp` && wget --no-cache -nv https://github.com/qutorial/mbeddr_python_installer/raw/master/mbeddr_install.py -O $mi && python3 $mi; 
  res=$?;
  rm $mi;
  exit $res;
fi

if [ "${UNAME}" = "Darwin" ]; then
  mi=`mktemp /tmp/mbeddr_install.py.XXXXX` && curl -L  https://github.com/qutorial/mbeddr_python_installer/raw/master/mbeddr_install.py -o $mi && python3 $mi;
  res=$?;
  rm $mi;
  exit $res;
fi

  


