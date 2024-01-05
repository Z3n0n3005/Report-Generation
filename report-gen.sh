#!/bin/bash
current_directory=$(pwd)
# current_directory="/home"

while [[ $1 =~ ^- && ! $1 == "--" ]]
  do 
    case $1 in
      -f | --file )
        shift; file=$1
        ;;
      --folder )
        shift; folder=$1
        ;;
      -a | --algo )
        shift; algo=$1
    esac; shift;
done

# check algo type first
if [[ -z "$algo" ]]; then
  echo "error: algorithm type is not allowed to be null"
  exit 1
elif [[ "$algo" != "textrank" 
    && "$algo" != "lsa" ]]; then 
  echo "error: inappropriate algo value: "
  exit 1
fi
 
# if both folder and file are not provided
if [[ -z "$file"  && -z "$folder" ]]; then
  echo "error: no file option has been provided"
  exit 1

# if both folder and file are provided
elif [[ ! -z "$file" && ! -z "$folder" ]]; then
  echo "error: only a file or a folder can be provided at the same time"
  exit 1

# if file is provided
elif [[ ! -z "$file" && -z "$folder" ]]; then 
  relative_file="$current_directory/$file"
  # "$current_directory"/gradlew run -Pfile="$current_directory/$file" -Palgo="$algo"
  "$current_directory"/gradlew run -Pfile="$relative_file" -Palgo="$algo"
# If folder is provided
elif [[ -z "$file" && ! -z "$folder" ]]; then
  relative_folder="$current_directory/$folder"
  # "$current_directory"/gradlew run -Pfolder="$current_directory/$folder" -Palgo="$algo"
  "$current_directory"/gradlew run -Pfolder="$relative_folder" -Palgo="$algo"
fi