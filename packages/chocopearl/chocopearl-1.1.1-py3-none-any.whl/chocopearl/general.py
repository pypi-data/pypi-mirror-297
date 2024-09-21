from datetime import timedelta

def input_yn(prompt='',yes='y',no='n',alt_yes=[],alt_no=[],wrong_input_msg=None):   #retorna True o False
    alt_yes.append(yes)
    alt_no.append(no)
    if wrong_input_msg is None:
        wrong_input_msg='Type '+yes+' (yes) or '+no+' (no)\n'
    while True:
        flag=input(f'{prompt}[{yes}/{no}]: ')
        if flag in alt_yes:
            return True
        elif flag in alt_no:
            return False
        else:
            print(wrong_input_msg)
    
def input_options(options,options_msg='Options:',selection_msg='Enter the IDs of the options to select (separated by comas \',\' ): ',invalid_selection_msg='Invalid selection'):

    while True:
        print(options_msg)
        for id,o in zip(list(range(1,len(options)+1)),options):
            print(f"{id}| {str(o)} ")
        print("")
        selected_ids=input(selection_msg)
        selected_ids=selected_ids.split(',')
        try:
            selected_ids=[int(id) for id in selected_ids]
            selected_options=[options[id-1] for id in selected_ids]
            break
        except:
            print(invalid_selection_msg)

    return selected_options

def format_time(seconds,return_as='string'):
    delta_t = timedelta(seconds=seconds)
    days = delta_t.days
    hours, remainder = divmod(delta_t.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    components = []
    if days:
        components.append(f"{days}D")
    if hours:
        components.append(f"{hours}H")
    if minutes:
        components.append(f"{minutes}M")
    if seconds:
        components.append(f"{seconds}S")
    if return_as=='str':
        time_string = " ".join(components)
        return time_string
    if return_as == 'dict':
        return {'D':days,'H':hours,'M':minutes,'S':seconds}

