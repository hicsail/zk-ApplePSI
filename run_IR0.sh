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

_wit0="irs/picozk_test.type0.wit"
_ins0="irs/picozk_test.type0.ins"
_wit1="irs/picozk_test.type1.wit"
_ins1="irs/picozk_test.type1.ins"
_wit2="irs/picozk_test.type2.wit"
_ins2="irs/picozk_test.type2.ins"

wit0="irs/wit/picozk_test.type0.wit"
ins0="irs/ins/picozk_test.type0.ins"
wit1="irs/wit/picozk_test.type1.wit"
ins1="irs/ins/picozk_test.type1.ins"
wit2="irs/wit/picozk_test.type2.wit"
ins2="irs/ins/picozk_test.type2.ins"

rel="irs/picozk_test.rel"
wit0="irs/wit/picozk_test.type0.wit"
ins0="irs/ins/picozk_test.type0.ins"
wit1="irs/wit/picozk_test.type1.wit"
ins1="irs/ins/picozk_test.type1.ins"
wit2="irs/wit/picozk_test.type2.wit"
ins2="irs/ins/picozk_test.type2.ins"


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
        cp $_wit0 $wit0
        cp $_ins0 $ins0
        cp $_wit1 $wit1
        cp $_ins1 $ins1
        cp $_wit2 $wit2
        cp $_ins2 $ins2
        if wtk-firealarm $rel $wit0 $ins0 $wit1 $ins1 $wit2 $ins2
            then
                echo "wtk-firealarm successfully completed"
            else
                echo "Error during wtk-firealarm"
        fi
    else
        echo "Error in the python script - abort"
fi