#!/bin/env bash
set -euo pipefail

failed=0
for t in tests/*.imp
  do
    echo "Running test $t"
    if ./imperivm "$t"; then
      echo -e "\e[32mOK\e[0m"
    else
      failed=1
      echo -e "\e[31mKO\e[0m"
    fi


  done
exit $failed