
def are_overlapped(gstart,gend,tstart,tend):
    return ( (( gstart <= tend )  and (gstart >= tstart)) or 
            ((gend <= tend) and (gend >= tstart)) or 
            ((tstart  <= gend)  and (tstart >= gstart))or 
            ((tend <= gend) and (tend >= gstart))
           ) 
 
# Runs through deid'ed (gs) file line by line
# Enters PHI locations in a HASH phi with KEY = (patient_number appended, note_number) and VALUE = (ARRAY of PHI locations in that note)




import re,sys
from collections import defaultdict

def run_stats(gold_path = 'id.deid', gold_cats_path= 'id-phi.phrase', test_path='phone.phi'):
    """
    Inputs:
        gold_path: path to the gold standard file that does not include categories.
        gold_cats_path: path to the gold standard file that includes category information
        test_path: path to the test file that we want to run the stats on
        
    Outputs:
        Displays:
            - All categories present in gold standard file
            - Cumulative accuracy for all categories
            - Accuracy for each category
    
    
    """
    
    patient_note_pattern = '^patient\s+(\d+)\s+note\s+(\d+)$'
    three_numbers_pattern = '^(\d+)\s+(\d+)\s+(\d+)$'

    test_phi = defaultdict(list)
    gold_phi = defaultdict(list)
    total_test_phi = 0


    with open(test_path) as test:  
        for line in test:
            results = re.findall(patient_note_pattern,line,flags=re.IGNORECASE)
            if len(results) ==1:
                #print(results)

                patient, note = results[0]
                continue

            elif len(results)>1:
                print(results)
                raise Exception("Debug here!")

            three_numbers = re.findall(three_numbers_pattern, line, flags=re.IGNORECASE)
            if len(three_numbers) ==1:
                (_,start,end) = three_numbers[0] #TODO: strings!
                #print('three',start,end)
                position = (start,end)
                test_phi[(patient,note)].append(position)
                total_test_phi +=1
                #print(total_test_phi)




    total_events_gold = 0

    with open(gold_path) as gold:  
        for line in gold:
            results = re.findall(patient_note_pattern,line,flags=re.IGNORECASE)
            if len(results) ==1:

                patient, note = results[0]
                continue

            elif len(results)>1:
                print(results)
                raise Exception("Debug here!")

            three_numbers = re.findall(three_numbers_pattern, line, flags=re.IGNORECASE)
            if len(three_numbers) ==1:
                (_,start,end) = three_numbers[0] #TODO: strings!
                #print('three',start,end)
                position = (start,end)
                gold_phi[(patient,note)].append(position)
                total_events_gold += 1


    # Runs through each patient_note combination in Gold Standard hash
    # Then in each note, runs through each PHI location 
    # For each PHI location, checks if the same location exists in the same patient_note in the deid'ed hash
    # If there is a match, true positives is incremented
    # If there is no match, false negatives is incremented   
    tp = 0;   # true positives
    fn = 0;   # false negatives
    n_checked_in_gold = 0
    for (patient,note) in gold_phi:
        for (g_start,g_end) in gold_phi[patient,note]:
            found = False
            n_checked_in_gold += 1
            if (patient,note) in test_phi:
                for t_start,t_end in test_phi[patient,note]:
                    if are_overlapped(g_start,g_end, t_start,t_end):
                        tp += 1 # true positive
                        found = True
                        break
            if not found:
                fn += 1

    # Runs through each patient_note combination in deid'ed hash
        # Then in each note, runs through each PHI location
        # For each PHI location, checks if the same location exists in the same patient_note in the Gold Standard hash
        # If there is a match, true positives is incremented
        # If there is no match, false positives is incremented

    fp = 0
    tp_test = 0
    said_negative_test = 0
    for (patient, note) in test_phi:
        for (t_start,t_end) in test_phi[patient,note]:
            found = False
            if (patient,note) in gold_phi:
                for g_start,g_end in gold_phi[patient,note]:
                    if are_overlapped(g_start,g_end, t_start,t_end):
                        found = True
                        tp_test +=1

                        break
                    else:
                        said_negative_test +=1

        if not found:
            fp += 1

    # Calculates sensitivity and positive predictive value (PPV)
    sens = round((tp/(tp+fn))*1000)/1000.0;
    ppv = round(( (total_test_phi-fp)/total_test_phi)*1000)/1000;
    # Prints code performance statistics on the screen
    print("\n\n==========================")
    print("\nNum of true positives = {}".format(tp))
    print("\nNum of false positives = {}".format(fp))
    print("\nNum of false negatives = {}".format(fn))
    print("\nSensitivity/Recall = {}".format(sens))
    print("\nPPV/Specificity = {}".format(ppv))
    print("\n==========================\n\n")  
    
    """ Per category experiments!"""
    gold_cats_map = defaultdict(dict)


    gold_cats_pattern = '^(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s(\w+)*'


    total_events_gold_cats = 0
    with open(gold_cats_path) as gold_cats:  
        for line in gold_cats:
            results = re.findall(gold_cats_pattern,line,flags=re.IGNORECASE)
            if len(results) ==1:
                #print(results)

                patient,note,start,end,category = results[0]
                total_events_gold_cats += 1
                if (patient,note) in gold_cats_map[category]:
                      gold_cats_map[category][patient,note].append((start,end))
                else:
                    gold_cats_map[category][patient,note] = [(start,end)]

            elif len(results)>1:
                print(results)
                raise Exception("Debug here!")

    print('Total events in \'{}\': {}'.format(gold_cats_path,total_events_gold_cats))
    categories = list(gold_cats_map.keys())
    print('='*40)
    print('Categories Present:')
    for cat in categories:
        print(cat)
    print('='*40)
    print('\n'*5)





    for current_cat in categories:


        print("Examining \"{}\" category.".format(current_cat))
        gold_phi = gold_cats_map[current_cat]


        # Runs through each patient_note combination in Gold Standard hash
        # Then in each note, runs through each PHI location 
        # For each PHI location, checks if the same location exists in the same patient_note in the deid'ed hash
        # If there is a match, true positives is incremented
        # If there is no match, false negatives is incremented   
        tp = 0;   # true positives
        fn = 0;   # false negatives
        n_checked_in_gold = 0
        for (patient,note) in gold_phi:
            for (g_start,g_end) in gold_phi[patient,note]:
                found = False
                n_checked_in_gold += 1
                if (patient,note) in test_phi:
                    for t_start,t_end in test_phi[patient,note]:
                        if are_overlapped(g_start,g_end, t_start,t_end):
                            tp += 1 # true positive
                            found = True
                            break
                if not found:
                    fn += 1

        # Runs through each patient_note combination in deid'ed hash
            # Then in each note, runs through each PHI location
            # For each PHI location, checks if the same location exists in the same patient_note in the Gold Standard hash
            # If there is a match, true positives is incremented
            # If there is no match, false positives is incremented

        fp = 0
        tp_test = 0
        said_negative_test = 0
        for (patient, note) in test_phi:
            for (t_start,t_end) in test_phi[patient,note]:
                found = False
                if (patient,note) in gold_phi:
                    for g_start,g_end in gold_phi[patient,note]:
                        if are_overlapped(g_start,g_end, t_start,t_end):
                            found = True
                            tp_test +=1

                            break
                        else:
                            said_negative_test +=1

            if not found:
                fp += 1

        # Calculates sensitivity and positive predictive value (PPV)
        sens = round((tp/(tp+fn))*1000)/1000.0;
        ppv = round(( (total_test_phi-fp)/total_test_phi)*1000)/1000;
        # Prints code performance statistics on the screen
        print("\n\n==========================")
        print("\nNum of true positives = {}".format(tp))
        print("\nNum of false positives = {}".format(fp))
        print("\nNum of false negatives = {}".format(fn))
        print("\nSensitivity/Recall = {}".format(sens))
        print("\nPPV/Specificity = {}".format(ppv))
        print("\n==========================\n\n") 
    
    
if __name__== "__main__":
        
    
    
    run_stats(sys.argv[1], sys.argv[2], sys.argv[3])
    
