from summa.summarizer import summarize
import argparse
import os
import yaml

current_working_dir = os.getcwd()
segmentation_yaml_folder_path = current_working_dir + '/../output/segmentationYaml'
summary_yaml_folder_path = current_working_dir + '/../output/summaryYaml'
stop_word_file_loc = current_working_dir + '/../app/build/resources/stopwords.txt'

sum_file_prefix = 'sum-'
sum_yaml_relative_path = '/../output/summaryYaml/'
sum_yaml_path = current_working_dir + sum_yaml_relative_path


def get_seg_sum_yaml_path(file: str):
    return sum_yaml_path + sum_file_prefix + file[4:]

def get_stop_word_list():
    result = []
    with open(stop_word_file_loc, 'r') as f:
        result = f.read().split("\n", -1)
    return result

def parse_yaml_file(full_file_path):
    with open(full_file_path, 'r') as f:
        return yaml.safe_load(f)

def summarize_text(text):
    return summarize(
        text=text, 
        ratio=0.2,
        words=50,
        additional_stopwords=get_stop_word_list() 
    )

file_list = []
root_dir = []

# Get the files list in the folder
for root, dirs, files in os.walk(segmentation_yaml_folder_path):
    file_list = files
    root_dir = root

# Parse through the list
for file in file_list:
    full_file_path = root_dir + '/' + file

    # Get the yaml content of the file
    yaml_file = parse_yaml_file(full_file_path)

    # Get the abstract segment -> summarize it
    abstract_seg = yaml_file['abstractSeg']
    abstract_seg_sum = summarize_text(abstract_seg)

    # Get the section list and parse through it
    section_list = yaml_file['sectionList']
    section_sum_list = []
    for section in section_list:
        header = section['header']
        content = section['content']
        # Summarize the content
        content_sum = summarize_text(content)
        section_sum_list.append({"header": header, "content": content_sum})

    # Build yaml file content
    sum_file_content = dict(
        abstractSeg = abstract_seg_sum,
        sectionList = section_sum_list
    )

    # Output content to a file
    sum_full_file_path = get_seg_sum_yaml_path(file)
    with open(sum_full_file_path, 'w') as output_file:
        yaml.dump(sum_file_content, output_file, default_flow_style=False)
