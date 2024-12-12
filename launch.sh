#l'utilisateur insère le chemin vers le fichier sam 
read -p "input sam file path: " file_path_input

#le premier if est une vérification qu'il s'agit bien d'un fichier sam 
if grep -q '^@SQ' $file_path_input; then
	echo "the given file is a sam file !" #ce message s'affiche afin de confirmer que le fichier est au bon format 
	
	#variable du chemin fournis
	file_path=$file_path_input
	
	#sauvegarde des résultats
    		
    	#demande l'utilisateur s'il souhaite fournir un chemin vers une directoire spécifique 
    	read -p "Your results will be saved. Would you like to choose a specific directory for your results? [Y/N] " path_choice&&[[ $save_results == [yY] || $save_results == [yY][eE][sS] || $save_results == [nN][oO] || $save_results == [nN] ]]
    	#while contrôle les valeurs qui sont fournis 
    	while [[ $path_choice != [yY] && $path_choice != [yY][eE][sS] && $path_choice != [nN][oO] && $path_choice != [nN] ]]; do
		echo "please enter a valid value [Y/N]"
		read -p "Would you like to choose a specific directory for your results? [Y/N] " path_choice&&[[ $save_results == [yY] || $save_results == [yY][eE][sS] || $save_results == [nN][oO] || $save_results == [nN] ]]
	done
		
	#si l'utilisateur répond oui, il fournira un chemin 
	#si l'utilisateur répond non, un message s'affiche indiquant que le travail sera sauvegardé dans la répertoire actuelle 
    	if [[ $path_choice == [yY] || $path_choice == [yY][eE][sS] ]]; then
    		read -p "Insert your desired file result path: " exit_path
    		while [[ ! -d "$exit_path" ]]; then
    			echo "The specified directory does not exist. Please provide a valid directory."
    			read -p "Insert your desired file result path: " exit_path
	else
		exit_path=$(pwd)
		echo "your results will be saved in the current directory which is [$exit_path] "
	fi
	
	result_file="$exit_path/analysis_results"
	mkdir "$result_file"

	
	#option de filtrer les résultats (avoir que des reads mappés ou pas)	
	read -p "do you want mapped reads only? [Y/N]: " mapped_only&&[[ $mapped_only == [yY] || $mapped_only == [yY][eE][sS] || $mapped_only == [nN][oO] || $mapped_only == [nN] ]]
	
	#while pour le contrôle des informations fournis
	while [[ $mapped_only != [yY] && $mapped_only != [yY][eE][sS] && $mapped_only != [nN][oO] && $mapped_only != [nN] ]]; do
		echo "please enter a valid value [Y/N]"
		read -p "do you want mapped reads only? [Y/N]: " mapped_only&&[[ $mapped_only == [yY] || $mapped_only == [yY][eE][sS] || $mapped_only == [nN][oO] || $mapped_only == [nN] ]]
	done
	
	#si l'utilisateur veut les reads mappés, on renvoie à python le paramètre true 
	if [[ $mapped_only == [yY] || $mapped_only == [yY][eE][sS] ]]; then
		mapped_only='True'
	
	#si l'utilisateur veut tous les reads, on renvoie à python le paramètre false 
	elif [[ $mapped_only == [nN] || $mapped_only == [nN][oO] ]]; then
		mapped_only='False'
	fi
	
	#option de filtrage par mapq
	read -p "do you want to filter by MAPQ? if no, then default is 0 [Y/N]: " filter_mapq&&[[ $filter_mapq == [yY] || $filter_mapq == [yY][eE][sS] || $filter_mapq == [nN][oO] || $filter_mapq == [nN] ]]
	while [[ $filter_mapq != [yY] && $filter_mapq != [yY][eE][sS] && $filter_mapq != [nN][oO] && $filter_mapq != [nN] ]]; do
	  echo "please enter a valid value [Y/N]"
	  read -p "do you want to filter by MAPQ? [Y/N]: " filter_mapq&&[[ $filter_mapq == [yY] || $filter_mapq == [yY][eE][sS] || $filter_mapq == [nN][oO] || $filter_mapq == [nN] ]]
	done

	if [[ $filter_mapq == [yY] || $filter_mapq == [yY][eE][sS] ]]; then
    read -p "do you want to chose your MAPQ score? [Y/N]:" filter_mapq_choice &&[[ $filter_mapq_choice == [yY] || $filter_mapq_choice == [yY][eE][sS] || $filter_mapq_choice == [nN] || $filter_mapq_choice == [nN][oO] ]]
    while [[ $filter_mapq_choice != [yY] && $filter_mapq_choice != [yY][eE][sS] && $filter_mapq_choice != [nN] && $filter_mapq_choice != [nN][oO] ]]; do
    echo "please enter a valid value [Y/N]"
    read -p "do you want to chose your MAPQ score? [Y/N]:" filter_mapq_choice &&[[ $filter_mapq_choice == [yY] || $filter_mapq_choice == [yY][eE][sS] || $filter_mapq_choice == [nN] || $filter_mapq_choice == [nN][oO] ]]
    done
    
    if [[ $filter_mapq_choice == [yY] || $filter_mapq_choice == [yY][eE][sS] ]]; then
      read -p "enter the desired value [0 - 100]: " mapq_value &&[[ $mapq_value =~ ^[0-9]+$ && $mapq_value -ge 0 && $mapq_value -le 100 ]]
      while [[ ! $mapq_value =~ ^[0-9]+$ || $mapq_value -le 0 || $mapq_value -ge 100 ]]; do
      echo "please enter a valid value [0 - 100]"
      read -p "enter the desired value [0 - 100]: " mapq_value &&[[ $mapq_value =~ ^[0-9]+$ && $mapq_value -ge 0 && $mapq_value -le 100 ]]
      done
      
    elif [[ $filter_mapq_choice == [nN][oO] || $filter_mapq_choice == [nN] ]]; then
      mapq_value=30
      echo "You chose no, MAPQ score is set at 30 by default"
    fi
  elif [[ $filter_mapq == [nN][oO] || $filter_mapq == [nN] ]]; then
    mapq_value=0
  fi

	read -p "Would you like to choose your intervals for viewing how the reads are mapped on the chromosome? if no, then default is 10k [Y/N]: " interval_chrs &&[[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] || $interval_chrs == [nN] || $interval_chrs == [nN][oO] ]]

	while [[ $interval_chrs != [yY] && $interval_chrs != [yY][eE][sS] && $interval_chrs != [nN] && $interval_chrs != [nN][oO] ]]; do
	  echo "please enter a valid value [Y/N]"
    read -p "Would you like to choose your intervals for viewing how the reads are mapped on the chromosome? if no, then default is 10k [Y/N]: " interval_chrs &&[[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] || $interval_chrs == [nN] || $interval_chrs == [nN][oO] ]]
	done

	if [[ $interval_chrs == [yY] || $interval_chrs == [yY][eE][sS] ]]; then
		read -p "enter the desired interval length: " interval_chrs_length &&[[ $interval_chrs_length =~ ^[0-9]+$ ]]
		while [[ ! $interval_chrs_length =~ ^[0-9]+$ ]]; do
		  echo "please enter a valid value"
		  read -p "enter the desired interval length: " interval_chrs_length &&[[ $interval_chrs_length =~ ^[0-9]+$ ]]
		done

	elif [[ $interval_chrs == [nN][oO] || $interval_chrs == [nN] ]]; then
		interval_chrs_length=10000
		echo "you chose no, interval length is set to 10k by default"
	fi
	
	read -p "Would you like to specify an interval for viewing reads based on their MAPQ score? if no, then default is 10 [Y/N]: " interval_mapq &&[[ $interval_mapq == [yY] || $interval_mapq == [yY][eE][sS] || $interval_mapq == [nN] || $interval_mapq == [nN][oO] ]]
	while [[ $interval_mapq != [yY] && $interval_mapq != [yY][eE][sS] && $interval_mapq != [nN] && $interval_mapq != [nN][oO] ]]; do
	echo "please enter a valid value [Y/N]"
	read -p "Would you like to specify an interval for viewing reads based on their MAPQ score? if no, then default is 10 [Y/N]: " interval_mapq &&[[ $interval_mapq == [yY] || $interval_mapq == [yY][eE][sS] || $interval_mapq == [nN] || $interval_mapq == [nN][oO] ]]
	done
	
	if [[ $interval_mapq == [yY] || $interval_mapq == [yY][eE][sS] ]]; then
		read -p "enter the desired interval length: " interval_mapq_length &&[[ $interval_mapq_length =~ ^[0-9]+$ ]]

	elif [[ $interval_mapq == [nN] || $interval_mapq == [nN][oO] ]]; then
		echo "You chose no interval length, it will be set to 10 by default"
		interval_mapq_length=10
	fi
else
	echo "it is not a sam file :( "
fi

echo -e "you chose the following parameters: \n Path to sam file = {$file_path_input} \n Mapped reads only: {$mapped_only} \n Mapq minimum filter = {$mapq_value} \n Interval chromosomes lengths = {$interval_chrs_length} \n Interval length for mapq = {$interval_mapq_length} \n Your results will be saved in: {$exit_path}"



python3 Main.py $file_path_input $mapped_only $mapq_value $interval_chrs_length $interval_mapq_length $result_file
