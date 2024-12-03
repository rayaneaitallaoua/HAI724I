file_path=$1
echo $file_path
if grep -q '^@SQ' $file_path; then
	echo "the given file is a sam file. Python will be executed"
	python3 Main.py $file_path
else
	echo "it is not a sam file"
fi