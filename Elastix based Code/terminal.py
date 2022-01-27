import os

#Function to avoid problems with parameter files already created in a folder
#where elastix was previously run. Deletes all file to run a registration with empty output dir
def delete_files(dir):
    '''Delte all files in directory '''
    all_files = os.listdir(dir)
    for f in all_files:
        os.remove(dir+f)

def run_command(vol_e, vol_i, dir, params):
    '''Run thorugh terminal simple registration command'''
    if not os.path.isdir(dir):
        os.mkdir(dir)
    delete_files(dir)
    if len(params)==2:
        params = ' -p ' + params[0] + ' -p ' + params[1]
    else:
        params = ' -p ' + params[0]
    command = 'elastix -f ' + vol_i + ' -m ' + vol_e + ' -out ' + dir + params
    print(command)
    os.system(command)

def run_command2(vol_e, vol_i, dir, params, mask_e, mask_i):
    '''Run thorugh terminal simple registration command with masks'''
    if not os.path.isdir(dir):
        os.mkdir(dir)
    delete_files(dir)
    if len(params)==2:
        params = ' -p ' + params[0] + ' -p ' + params[1]
    else:
        params = ' -p ' + params[0]
    command = 'elastix -f ' + vol_i + ' -m ' + vol_e + ' -fMask ' + mask_i + ' -mMask ' + mask_e + ' -out ' + dir + params
    print(command)
    os.system(command)

def get_def_field(path, compose=False):
    if compose==False:
        mode='0'
    else:
        mode='1'
    command = 'transformix -def \'all\' -out ' + path + ' -tp ' + path + '/TransformParameters.' + mode + '.txt'
    print(command)
    os.system(command)