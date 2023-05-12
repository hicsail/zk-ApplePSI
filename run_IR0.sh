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

dir="/usr/src/app/"
orig="/code/"
cp $orig$file.py $dir$file.py


name=$target/$file$underscore$prime_fam$underscore$size

rel="picozk_test.rel"
wit0="picozk_test.type0.wit"
ins0="picozk_test.type0.ins"
wit1="picozk_test.type1.wit"
ins1="picozk_test.type1.ins"
wit2="picozk_test.type2.wit"
ins2="picozk_test.type2.ins"


[ -e $rel  ] && rm $rel
[ -e $wit0  ] && rm $wit0
[ -e $ins0 ] && rm $ins0
[ -e $wit1  ] && rm $wit1
[ -e $ins1 ] && rm $ins1
[ -e $wit2  ] && rm $wit2
[ -e $ins2 ] && rm $ins2

# Actual Execution

echo "Running $file ....";

if python3 $dir$file.py
    then
        if wtk-firealarm $rel $wit0 $ins0 $wit1 $ins1 $wit2 $ins2
            then
                echo "wtk-firealarm successfully completed"
            else
                echo "Error during wtk-firealarm"
        fi
    else
        echo "Error in the python script - abort"
fi