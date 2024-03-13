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

# Refresh the directory
rm -r irs
mkdir -p irs


# Actual Execution
echo "Running $file ....";

if pypy3 $dir$file.py; then
    dirlist=`ls irs`
    echo $dirlist
else
    echo "Error in the Python Script"
    exit 1
fi

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


# Run firealarm test
cd irs

if wtk-firealarm $dirlist; then
    cd ..
    echo "wtk-firealarm successfully completed"
else
    echo "Error during wtk-firealarm"
    exit 1
fi

# Creat dir
mkdir -p irs/wit
mkdir -p irs/ins

# Copy into directory compatible with mac-and-cheese
for ir in ${dirlist}
    do
        if [[ "irs/$ir" == *.ins ]]
            then
                # if it has, move it to irs/ins
                mv $dir/irs/$ir $dir/irs/ins/$ir
        fi
        if [[ "irs/$ir" == *.wit ]]
            then
                # if it has, move it to irs/ins
                mv $dir/irs/$ir $dir/irs/wit/$ir
        fi
done