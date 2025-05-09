#!/bin/bash
set -e

BASE="tests/fixtures/test_dirs"
mkdir -p "$BASE"

# Empty directory
mkdir -p "$BASE/empty_dir"

# simple_project
mkdir -p "$BASE/simple_project/sub_dir1"
head -c 1024 </dev/urandom | base64 > "$BASE/simple_project/file1.txt"
head -c 2048 </dev/urandom | base64 > "$BASE/simple_project/file2.md"
head -c 1024 </dev/urandom | base64 > "$BASE/simple_project/sub_dir1/script.py"

# complex_project
mkdir -p "$BASE/complex_project"/{src/feature,tests,docs,data,.git,__pycache__,node_modules}
echo "# Complex Project" > "$BASE/complex_project/README.md"
echo "SECRET_KEY=keepitsecret" > "$BASE/complex_project/.env"
echo "setting: value" > "$BASE/complex_project/config.yaml"
echo 'print("main")' > "$BASE/complex_project/src/main.py"
echo 'def helper(): pass' > "$BASE/complex_project/src/utils.py"
echo 'class MyModule: pass' > "$BASE/complex_project/src/feature/module.py"
echo '# test main' > "$BASE/complex_project/tests/test_main.py"
echo '# test utils' > "$BASE/complex_project/tests/test_utils.py"
echo '# Project Docs' > "$BASE/complex_project/docs/index.md"
echo '# API Reference' > "$BASE/complex_project/docs/api.md"
echo -e 'col1,col2\n1,2' > "$BASE/complex_project/data/small_data.csv"
echo 'INFO: Started' > "$BASE/complex_project/data/temp.log"
echo 'ref: refs/heads/main' > "$BASE/complex_project/.git/HEAD"
touch "$BASE/complex_project/__pycache__/utils.cpython-39.pyc"
touch "$BASE/complex_project/node_modules/placeholder.js"

# large_files_dir
mkdir -p "$BASE/large_files_dir"
head -c 5120 </dev/urandom > "$BASE/large_files_dir/small.txt"
head -c 10240 </dev/urandom > "$BASE/large_files_dir/medium.txt"
head -c 15360 </dev/urandom > "$BASE/large_files_dir/large.txt"
touch "$BASE/large_files_dir/empty.txt"

# hidden_files_dir
mkdir -p "$BASE/hidden_files_dir/.hidden_subdir"
echo 'hidden_setting=true' > "$BASE/hidden_files_dir/.config_file"
echo 'This is visible.' > "$BASE/hidden_files_dir/visible_file.txt"
echo 'data' > "$BASE/hidden_files_dir/.hidden_subdir/another_hidden.dat"
echo 'data' > "$BASE/hidden_files_dir/.hidden_subdir/.another_hidden.dat"
echo 'Visible inside hidden.' > "$BASE/hidden_files_dir/.hidden_subdir/visible_in_hidden.txt"

# symlink_dir
mkdir -p "$BASE/symlink_dir/actual_dir"
echo 'This is the actual file.' > "$BASE/symlink_dir/actual_file.txt"
echo 'Inside actual dir.' > "$BASE/symlink_dir/actual_dir/file_in_actual_dir.txt"
ln -sf actual_file.txt "$BASE/symlink_dir/link_to_file"
ln -sf actual_dir "$BASE/symlink_dir/link_to_dir"
ln -sf no_such_file.txt "$BASE/symlink_dir/broken_link"

# symlink_loop_dir
mkdir -p "$BASE/symlink_loop_dir/dir_a" "$BASE/symlink_loop_dir/dir_b"
ln -sf ../dir_b "$BASE/symlink_loop_dir/dir_a/link_to_dir_b"
ln -sf ../dir_a "$BASE/symlink_loop_dir/dir_b/link_to_dir_a"

# content_processing_dir
mkdir -p "$BASE/content_processing_dir"
touch "$BASE/content_processing_dir/empty_file.txt"

# Create text files with precise byte counts
# small_file.txt: 5KB = 5120 bytes
yes a | head -n 5120 | tr -d '\n' > "$BASE/content_processing_dir/small_file.txt"
# exact_size_file.txt: 10KB = 10240 bytes
yes a | head -n 10240 | tr -d '\n' > "$BASE/content_processing_dir/exact_size_file.txt"
# large_file.txt: 15KB = 15360 bytes
yes a | head -n 15360 | tr -d '\n' > "$BASE/content_processing_dir/large_file.txt"

echo "你好世界, Привет, €αβγ" > "$BASE/content_processing_dir/utf8_chars.txt"
echo -ne '\x80\x81\x82\x83\x84' > "$BASE/content_processing_dir/binary_file.bin"
echo "Secrets!" > "$BASE/content_processing_dir/permission_denied_file.txt" # Readable in fixture source
echo "Readable" > "$BASE/content_processing_dir/permission_ok_file.txt"

# lang_hint_project
mkdir -p "$BASE/lang_hint_project"
echo 'print("python")' > "$BASE/lang_hint_project/script.py"
echo 'body { color: blue; }' > "$BASE/lang_hint_project/styles.css"
echo '{"key": "value"}' > "$BASE/lang_hint_project/data.json"
echo '# Markdown' > "$BASE/lang_hint_project/README.md"
echo 'some data' > "$BASE/lang_hint_project/unknown.xyz"
echo 'text with no extension' > "$BASE/lang_hint_project/no_ext_file"


# encoding_issues_dir
mkdir -p "$BASE/encoding_issues_dir"
echo "UTF-8 text éàç" > "$BASE/encoding_issues_dir/utf8_file.txt"
echo -e "Latin-1 text éàç" | iconv -f UTF-8 -t LATIN1 > "$BASE/encoding_issues_dir/latin1_file.txt"
head -c 256 </dev/urandom > "$BASE/encoding_issues_dir/binary_file.bin"

# all_ignored_dir
mkdir -p "$BASE/all_ignored_dir/node_modules"
touch "$BASE/all_ignored_dir/.DS_Store"
touch "$BASE/all_ignored_dir/file.pyc"
touch "$BASE/all_ignored_dir/image.jpg"
touch "$BASE/all_ignored_dir/node_modules/index.js"

# special_chars_dir
mkdir -p "$BASE/special_chars_dir/path with 'quotes'"
echo 'Spaces file' > "$BASE/special_chars_dir/file with spaces.txt"
echo 'Special chars' > "$BASE/special_chars_dir/file&name=problem?.py"
echo 'Inside quotes' > "$BASE/special_chars_dir/path with 'quotes'/file.txt"
echo 'Unicode filename' > "$BASE/special_chars_dir/über_cool_file.txt"

echo "✅ Test directories created under $BASE"
