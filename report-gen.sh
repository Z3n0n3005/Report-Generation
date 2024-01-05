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

# If both folder and file are not provided
if [[ -z "$file"  && -z "$folder" ]]; then
  echo "ERROR: No option has been provided"

# If both folder and file are provided
elif [[ ! -z "$file" && ! -z "$folder" ]]; then
  echo "ERROR: Only a file or a folder can be provided at the same time"

# If file is provided
elif [[ ! -z "$file" && -z "$folder" ]]; then 
  $relative_file="$current_directory"/"$file"
  "$current_directory"/gradlew run -Pfile=$relative_file

# If folder is provided
elif [[ -z "$file" && ! -z "$folder" ]]; then
  $relative_folder="$current_directory/$folder"
  echo "$relative_folder"
  ls $current_directory
  ls $relative_folder
  "$current_directory"/gradlew run -Pfolder=$relative_folder
fi
# import file name through command line later
# "$current_directory"/gradlew run -Pfile=$file
``