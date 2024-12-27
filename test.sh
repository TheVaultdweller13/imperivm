#!/bin/env bash
set -euxo pipefail

failed=0
for t in tests/*.imp
  do
    echo "Running test $t"
    if ./imperivm "$t"; then
      echo "OK"
    else
      failed=1
      echo "KO"
    fi

  done
exit $failed