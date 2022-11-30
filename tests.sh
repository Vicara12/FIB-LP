#!/bin/bash

all_ok="yes"

echo
echo " ~~~~ RUNNING TESTS ~~~~"

for f in ./tests/*.funx
do
    res=$(./funx.py $f)
    corr=$(cat $f | head -1 | sed 's/#//g')

    if [[ $res = $corr ]]; then
        echo " - Test OK: $f"
    else
        echo " - Test FAILED: $f (expected: $corr   got: $res)"
        all_ok="no"
    fi
done

echo

if [[ $all_ok = "yes" ]]; then
    echo "All tests passed successfully! :)"
else
    echo "WARNING: one or more tests failed"
fi

echo
