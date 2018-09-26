#!/bin/bash

source .virtenv/bin/activate

PROPERTIES_FILE_NAME_2=""

if [ ! -z ${PROPERTIES_FILE_NAME} ]; then
  PROPERTIES_FILE_NAME_2=${PROPERTIES_FILE_NAME}
fi

if [[ $1 = *".properties"* ]] ; then
  PROPERTIES_FILE_NAME_2=$1
elif [[ $1 = *"test"* ]] ; then
  PROPERTIES_FILE_NAME_2="properties-test.properties"
fi

if [ -z ${PROPERTIES_FILE_NAME_2} ]; then
PROPERTIES_FILE_NAME_2="properties.properties"
fi

echo "PROPERTIES_FILE_NAME_2: ${PROPERTIES_FILE_NAME_2}"
if [ ! -z ${PROPERTIES_FILE_NAME_2} ]; then
  DOWNLOAD_DIR_2=`cat ./conf/$PROPERTIES_FILE_NAME_2 | grep "FIREFOX_DOWNLOAD_DIR=" | grep -v '#'`
  export ${DOWNLOAD_DIR_2}
  #source ./conf/${PROPERTIES_FILE_NAME_2}
fi

echo "Used DOWNLOAD_DIR: ${DOWNLOAD_DIR_2}"

NOW=`date +%Y-%m-%d_%H-%M-%S`

python3.6 -c "from run import run
r = run()
r.magic()
r.ses.close_web_driver()
" ${PROPERTIES_FILE_NAME_2}

NEW_NOW=`date +%Y-%m-%d_%H-%M-%S`
echo "Donloaded into: ${FIREFOX_DOWNLOAD_DIR}"
echo "Start: ${NOW} End: ${NEW_NOW}"
