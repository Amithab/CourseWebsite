import argparse

parser = argparse.ArgumentParser(description="Generate config file from comments config file minus the comments")
parser.add_argument('-p', '--package', default='package.json', help="The path to config file to write to")
parser.add_argument('-c', '--comments', default='package.comments.json', help="The path to comment config file to read from")
parser_args = parser.parse_args()

path_to_package_file = parser_args.package
path_to_comments_file = parser_args.comments

with open(path_to_comments_file) as comment_file, open(path_to_package_file, 'w') as package_file:
    for line in comment_file.readlines():
        package_file.write((line + " ")[:line.rfind("//")].rstrip()+ '\n')
