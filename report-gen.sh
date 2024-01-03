#!/bin/bash
current_directory=$(pwd)

while [[ $1 =~ ^- && ! $1 == "--" ]]
  do 
    case $1 in
      -f | --file )
        shift; file=$1
        ;;
      --folder )
        shift; folder=$1
        ;;
    esac; shift;
done

# while IFS = read -r line; do
#   echo "$line"
# done < $file

# fileContent = $(<$file)

# echo "$file"
# echo "$fileContent"

# import file name through command line later
"$current_directory"/gradlew run -Pfile=$file
``