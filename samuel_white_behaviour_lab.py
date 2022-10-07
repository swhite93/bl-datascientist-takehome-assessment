def get_password_steps(password):
    
    ###### ------- import libraries
    import pandas as pd
    import numpy as np 
    import sympy
    
    
    ##### define functions used    
    
    def find_sub(string,substring):
        
        ### returns the indexs of any time a substring starts within the string        
        start_indexs = []
        for i in range(len(string)):
            if string[i:i+len(substring)] == substring:
                start_indexs.append(i)
        return(start_indexs)

    def multiply(list):
        
        ## multiplies all elements in list
        tot = 1
        for i in list:
            tot = int(tot) * int(i)      
        return(tot)

    min_len = 7 # minimum length of password
    max_len = 25 # maximum length of password
    primes = list(sympy.primerange(0, 1000)) # a list of primes, used for defining unique sets of boundaries
    
    
    ## read in the disallowed passwords
    with open('common-passwords.txt') as file:
        lines = file.readlines()
        not_allowed = [line.rstrip() for line in lines]
        
    ## append these disallowed passwords with three-in-a-row versions of each unique char
    all_unique = list(set([password[i] for i in range(len(password))]))
    for i in all_unique:
        not_allowed.append(i + i + i)

    ### get the necessary changes from all constraints - length, consecutive runs, banned strings 
    ### and types of char
    
    
    ## here we find all instances of disallowed substrings, make a note of the start and end, and give it 
    ## a prime number as an identifier - the reason for this is explained later
    count = 0
    now_allowed_details = []
    for i in range(len(not_allowed)):
        if not_allowed[i] in password:   
            first_indexs = find_sub(password,not_allowed[i])
            for l in range(len(first_indexs)):           
               
                now_allowed_details.append([primes[count],first_indexs[l],first_indexs[l] + len(not_allowed[i]) - 1])
                count+=1

    
    ### this section of code iterates through each position of the password string, and finds the 
    ### smallest set of indicies, such that every single instance forbidden substring that exists within the 
    ### password has at least one element within the set. From this we know what the smallest number of 
    ## changes that have to be made in order to change all forbidden substrings.
    ## We do this by noting the product of all of the primes associated with each forbidden substring 
    ## as we iterate through. If the value increases, it means we have entered a new forbidden string
    ## and if the product divdes the previous product, we know that we haven't 'left' any of the other 
    ## forbidden stings we were previously in. 
    
    now_allowed_details = np.array(now_allowed_details) # convert to numpy array for ease of filtering
    number_total = 0 
    if len(now_allowed_details) > 0:
        old_product = 1    
        grad = 'negative' # keep a running note of whether the prime product has previously increased or decreased
        
        # now we iterate through the password
        for i in range(len(password)):
            
            ## find the forbidden strings which our i iterator is within
            rows = np.where((now_allowed_details[:,1] <= i) & (now_allowed_details[:,2] >= i))[0]
            
            ## take new product and see if anything has changed
            new_product = multiply(now_allowed_details[rows][:,0])
            if new_product != old_product:
            
                ## if it has changed then figure out the nature of the change
            
                if new_product > old_product and new_product%old_product != 0:
                
                    ## this means we have hit a new forbidden string at the same time as exiting another one
                    number_total+=1
                    last_grad = 'positive'
                
                elif new_product < old_product and last_grad == 'positive':
                
                    number_total+=1
                    last_grad = 'negative'        
                
                elif new_product > old_product:
                    last_grad = 'positive'
                else:
                    last_grad = 'negative'                             
                old_product = new_product   

    ## quickly get the different char types
    types = []
    for i in all_unique:
        if i.isnumeric():
            types.append(0)
        elif not i.isupper():
            types.append(1)
        else:
            types.append(2)

    ## get the number of steps above the max limit - this for the moment is just added to the final value
    additional_steps = max(len(password)-max_len,0) 

    ## IMPORTANT - this calculation to give the final value is only correct if we assume that you can add a 
    ## char to the password at any point along the password. Therefore, if you have 'abcdefg' then making this 
    ## 'abTcdefg' would be just one step. This is how I interpreted the task?
    final_steps = max(min_len - len(password),3 - len(set(types)),number_total) + additional_steps
    return(final_steps)



if __name__ == '__main__':
    
    password = '00000000'
    number_changes = get_password_steps(password)
    
    print('required number of changes:',number_changes)
    
    
    