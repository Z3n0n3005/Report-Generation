#!/bin/bash

# while [[ $1 =~ ^- && ! $1 == "--" ]]
#   do 
#     case $1 in
#       -f | --file )
#         shift; file=$1
#         ;;
#     esac; shift;
# done

# while IFS = read -r line; do
#   echo "$line"
# done < $file

# fileContent = $(<$file)

# echo "$file"
# echo "$fileContent"

# import file name through command line later
# might import whole folder to run through at once since grobid initialization is slow
./gradlew run
``