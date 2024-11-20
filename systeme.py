c=0

chemin = "/home/farah/Bureau/mapping.sam"
x = 4
compte_read=0
flag_distinct_reps = {}
with open (chemin, "r") as f:
    for line in f:
        

        if line.startswith('@'):
            continue
        columns = line.split('\t')

        name = columns[0]
        flag = columns[1]
        #print (f"name: {name}", f"flag: {flag}")
        

        
        
        if int(flag) & x == 0:
            compte_read = compte_read + 1
            if flag in flag_distinct_reps:
                flag_distinct_reps[flag] = flag_distinct_reps[flag] + 1
            else:
                flag_distinct_reps[flag] = 1


    print(compte_read)
    print(flag_distinct_reps)


