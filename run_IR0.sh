# # #!/bin/sh


# Taking tags from the command line

while getopts f: flag
do
    case "${flag}" in
        f) file=${OPTARG};;
    esac
done



# Checking if a file name is properly specified

if [ -z "$file" ]
    then
        echo "Please specify an object code"
        exit 1
fi



# Setting missing parameters if any

if [ -z "$target" ]
    then
        target="./tests"
        echo "test directory is set to './tests' "
fi

if [ -z "$size" ]
    then
        size=0
        echo "test size is set to 0 "
fi


# Copying a designated statement file

dir="/usr/src/app/examples/"
orig="/code/"
cp $orig$file.py $dir$file.py


name=$target/$file$underscore$prime_fam$underscore$size
# rel=$name.rel
# wit=$name.type1.wit
# ins=$name.type1.ins

rel="picozk_test.rel"
wit="picozk_test.type1.wit"
ins="picozk_test.type1.ins"


[ -e $rel  ] && rm $rel
[ -e $wit  ] && rm $wit
[ -e $ins  ] && rm $ins


# Actual Execution

echo "Running $file ....";

if python3 $dir$file.py
    then
        if wtk-firealarm $rel $wit $ins
            then
                echo "wtk-firealarm successfully completed"
            else
                echo "Error during wtk-firealarm"
        fi
    else
        echo "Error in the python script - abort"
fi