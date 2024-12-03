file_path = $1
if grep -q '^@HD' "$file_path"; then
	echo "the given file is a sam file. Python will be executed"
	python3 main.py "$file_path"
else
	echo "it is not a sam file"
