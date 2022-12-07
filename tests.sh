#!/bin/bash

all_ok="yes"

echo
echo " ~~~~ RUNNING TESTS ~~~~"

for f in ./tests/*.funx
do
    res=$(./funx.py $f)
    corr=$(cat $f | grep \# | sed 's/#//g')

    if [[ $res = $corr ]]; then
        echo " - Test OK: $f"
    else
        echo " - Test FAILED: $f"
        echo "      * Expected: $corr"
        echo "      * Result:   $res"
        echo
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
