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
        target="./irs"
        echo "test directory is set to './irs' "
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


# Refresh the directory
rm -r irs
mkdir -p irs


# Actual Execution
echo "Running $file ....";

python3 $dir$file.py
dirlist=`ls irs`
echo $dirlist

# firealarm format check

# Check if wtk-firealarm is installed.
if ! command -v wtk-firealarm >/dev/null 2>&1; then
    echo "wtk-firealarm is not installed. Please follow the instructions below to install it:"
    echo "  git clone git@github.mit.edu:sieve-all/wiztoolkit.git"
    echo "  cd wiztoolkit && make && make install"
    echo "  cp /usr/src/app/wiztoolkit/target/wtk-firealarm /usr/bin/wtk-firealarm"
    echo "  cd .. #Go back to the current directory"
    exit 1
fi


# Creat dir
mkdir -p irs/wit
mkdir -p irs/ins

# Run firealarm test
cd irs && wtk-firealarm $dirlist && cd ..

if wtk-firealarm "$rel" "$wit" "$ins"; then
    echo "wtk-firealarm successfully completed"
else
    echo "Error during wtk-firealarm"
fi

# Copy into directory compatible with mac-and-cheese
for ir in ${dirlist}
    do
        if [[ "irs/$ir" == *.ins ]]
            then
                # if it has, move it to irs/ins
                mv ./irs/$ir ./irs/ins/$ir
        fi
        if [[ "irs/$ir" == *.wit ]]
            then
                # if it has, move it to irs/ins
                mv ./irs/$ir ./irs/wit/$ir
        fi
done
# copy the irs into local
cp -r ./irs /code