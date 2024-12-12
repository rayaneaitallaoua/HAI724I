read -p "input sam file path: " file_path_input

if grep -q '^@SQ' $file_path_input; then
	echo "the given file is a sam file !"

	file_path=$file_path_input

	read -p "do you want mapped reads only? [Y/N]: " mapped_only&&[[ $mapped_only == [yY] || $mapped_only == [yY][eE][sS] || $mapped_only == [nN][oO] || $mapped_only == [nN] ]]

	while [[ $mapped_only != [yY] || $mapped_only != [yY][eE][sS] || $mapped_only != [nN][oO] || $mapped_only != [nN] ]]; do
	  echo "please enter a valid value [Y/N]"
	  read -p "do you want mapped reads only? [Y/N]: " filter&&[[ $filter == [yY] || $filter == [yY][eE][sS] || $filter == [nN][oO] || $filter == [nN] ]]
	done

	if [[ $mapped_only == [yY] || $mapped_only == [yY][eE][sS] ]]; then
	  mapped_only='True'

	elif [[ $mapped_only == [nN] || $mapped_only == [nN][oO] ]]; then
	  mapped_only='False'
	fi

	read -p "do you want to filter by MAPQ? [Y/N]: " filter_mapq&&[[ $filter_mapq == [yY] || $filter_mapq == [yY][eE][sS] || $filter_mapq == [nN][oO] || $filter_mapq == [nN] ]]
	while [[ $filter_mapq != [yY] || $filter_mapq != [yY][eE][sS] || $filter_mapq != [nN][oO] || $filter_mapq != [nN] ]]; do
	  echo "please enter a valid value [Y/N]"
	  read -p "do you want mto filter by MAPQ? [Y/N]: " filter&&[[ $filter_mapq == [yY] || $filter_mapq == [yY][eE][sS] || $filter_mapq == [nN][oO] || $filter_mapq == [nN] ]]
	done

	if [[ $filter_mapq == [yY] || $filter_mapq == [yY][eE][sS] ]]; then
    read -p "do you want to chose your MAPQ score? [Y/N]:" filter_mapq_choice &&[[ $filter_mapq_choice == [yY] || $filter_mapq_choice == [yY][eE][sS] || $filter_mapq_choice == [nN] || $filter_mapq_choice == [nN][oO] ]]
    if [[ $filter_mapq_choice == [yY] || $filter_mapq_choice == [yY][eE][sS] ]]; then
      read -p "enter the desired value " mapq_value &&[[ $mapq_value =~ ^[0-9]+$ && $mapq_value -ge 0 && $mapq_value -le 100 ]]
      #|| { echo "Invalid input. Please enter a number between 0 and 100."}

    elif [[ $filter_mapq_choice == [nN][oO] || $filter_mapq_choice == [nN] ]]; then
      mapq_value=30
      echo "You chose no, MAPQ score is set at 30 by default"
    fi
  elif [[ $filter_mapq == [nN][oO] || $filter_mapq == [nN] ]]; then
    mapq_value=0
  fi

	read -p "Would you like to choose your intervals for viewing how the reads are mapped on the chromosome? [Y/N] " interval_chrs &&[[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] || $interval_chrs == [nN] || $interval_chrs == [nN][oO] ]]

	while [[ $interval_chrs != [yY] || $interval_chrs != [yY][eE][sS] || $interval_chrs != [nN] || $interval_chrs != [nN][oO] ]]; do
	  echo "please enter a valid value [Y/N]"
    read -p "Would you like to choose your intervals for viewing how the reads are mapped on the chromosome? [Y/N] " interval_chrs &&[[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] || $interval_chrs == [nN] || $interval_chrs == [nN][oO] ]]
	done

	if [[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] ]]; then
		read -p "enter the desired interval length: " interval_chrs_length &&[[ $interval_chrs_length =~ ^[0-9]+$ ]]
		while [[ ! $interval_chrs_length =~ ^[0-9]+$ ]]; do
		  echo "please enter a valid value [Y/N]"
		  read -p "enter the desired interval length: " interval_chrs_length &&[[ $interval_chrs_length =~ ^[0-9]+$ ]]
		done

	elif [[ $filter_mapq == [nN][oO] || $filter_mapq == [nN] ]]; then
		interval_chrs_length=10000
		echo "you chose no, interval length is set to 10k by default"
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