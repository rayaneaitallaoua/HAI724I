read -p "input sam file path: " file_path_input

if grep -q '^@SQ' $file_path_input; then
	echo "the given file is a sam file !"
	file_path=$file_path_input
	read -p "do you want the reads to be filtered? [Y/N]: " filter&&[[ $filter == [yY] || $filter == [yY][eE][sS] ]] || exit
	read -p "do you want to filter by MAPQ? [Y/N]: " filter_mapq &&[[ $filter == [yY] || $filter == [yY][eE][sS] ]] || exit
	
	read -p "do you want to chose your MAPQ score? " filter_mapq_choice &&[[ $filter_mapq_choice == [yY] || $filter_mapq_choice == [yY][eE][sS] || $filter_mapq_choice == [nN] || $filter_mapq_choice == [nN][oO] ]]
	if [[ $filter_mapq_choice == [yY] || $filter_mapq_choice == [yY][eE][sS] ]]; then
		read -p "enter the desired value " mapq_value &&[[ $mapq_value =~ ^[0-9]+$ && $mapq_value -ge 0 && $mapq_value -le 100 ]]
		#|| { echo "Invalid input. Please enter a number between 0 and 100."}
	else
		filter_mapq_score=30
		echo "you chose no, MAPQ score is set at 30 by default"
	fi
		
	read -p "Would you like to choose your interval for viewing how the reads are mapped on the chromosome? [Y/N] " interval_chrs &&[[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] || $interval_chrs == [nN] || $interval_chrs == [nN][oO] ]]
	
	if [[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] ]]; then
		read -p "enter the desired interval length: " interval_chrs_length &&[[ $interval_chrs_length =~ ^[0-9]+$ ]]
	else 
		interval_chrs_length=100000
		echo "you chose no, interval length is set to 100k by default"
	fi
	
	read -p "Would you like to specify an interval for viewing reads based on their MAPQ score? " interval_mapq &&[[ $interval_mapq == [yY] || $interval_mapq == [yY][eE][sS] || $interval_mapq == [nN] || $interval_mapq == [nN][oO] ]]
	if [[ $interval_mapq == [yY] || $interval_mapq == [yY][eE][sS] ]]; then
		read -p "enter the desired interval length: " interval_mapq_length &&[[ $interval_mapq_length =~ ^[0-9]+$ ]]

	
	
	else
		echo "You chose no interval length, it will be set to 10 by default"
		interval_mapq_length=10
	fi
else
	echo "it is not a sam file :( "
fi
