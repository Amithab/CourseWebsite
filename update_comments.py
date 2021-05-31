"""
Examples:

pc.json
"a" //
"b" //
"a" //
"c"
"d" //
"e" //
"e" //

p.json
"a" // don't print a since duplicate a's, but log
"b" // don't print b since duplicate b's, but log
"b"
"c" // print both c's since c doesn't have comment
"c"
"d" // print d since single comment in d
    // don't print e since duplicate e's, but log in erased
"""

import argparse

parser = argparse.ArgumentParser(description="Update the comments config file")
parser.add_argument('-p', '--package', default='package.json', help="The path to config file to read from")
parser.add_argument('-c', '--comments', default='package.comments.json', help="The path to comment config file to update")
parser_args = parser.parse_args()

path_to_package_file = parser_args.package
path_to_comments_file = parser_args.comments

comment_map = {}
key_set = set()
comment_duplicate_keys = set()
both_duplicate_keys = set()
package_duplicate_keys = set()

def get_key(line):
    # Find key in "key"
    first = line.find("\"")
    if first == -1:
        return None
    second = line.find("\"", first + 1)
    if second == -1:
        return None
    return line[first + 1 : second]

with open(path_to_comments_file) as comments_file:
    for line in comments_file.readlines():
        key = get_key(line)
        if key is None:
            continue

        # Find // in "key": "value" // or { //
        comment_ind = line.rfind("//")
        last_quote = line.rfind("\"")

        if key in comment_map: # "a" // \n "a"
            comment_duplicate_keys.add(key)

        if comment_ind != -1 and comment_ind > last_quote:
            if key in key_set: # "a" (//)? \n "a" //
                comment_duplicate_keys.add(key)
            if key in comment_map:
                comment_map[key].append(line[comment_ind+2:].strip())
            else:
                comment_map[key] = [line[comment_ind+2:].strip()]
        key_set.add(key)

key_set = set()

with open(path_to_package_file) as package_file:
    for line in package_file.readlines():
        key = get_key(line)
        if key is None:
            continue

        if key in comment_duplicate_keys:
            # Duplicate in package.comments.json that appears in package.json
            both_duplicate_keys.add(key)
            comment_duplicate_keys.remove(key)
        elif key not in both_duplicate_keys and key in key_set and key in comment_map:
            # Duplicate only in package.json
            package_duplicate_keys.add(key)
        key_set.add(key)


with open(path_to_package_file) as package_file, open(path_to_comments_file, 'w') as comments_file:
    for line in package_file.readlines():
        key = get_key(line)
        if key is None:
            comments_file.write(line)
            continue

        if key in package_duplicate_keys or key in both_duplicate_keys or key not in comment_map:
            comments_file.write(line)
        else:
            comments_file.write(line.rstrip() + " // " + comment_map[key][0] + "\n")

if len(package_duplicate_keys) > 0:
    print("Duplicates in package.json with dangling comments:")
    for key in package_duplicate_keys:
        print(key, ":\n//", '\n// '.join(comment_map[key]))

if len(both_duplicate_keys) > 0:
    print("Duplicate comment keys that aren't mapped:")
    for key in both_duplicate_keys:
        print(key, ":\n//", '\n// '.join(comment_map[key]))

if len(comment_duplicate_keys) > 0:
    print("Duplicate comment keys that are deleted:")
    for key in comment_duplicate_keys:
        print(key, ":\n//", '\n// '.join(comment_map[key]))
