import os

def loadcase(data_folder, case):
    #Getting all the nifti files in the folder
    image_file_list = sorted([file_name for file_name in os.listdir(data_folder) if file_name.lower().endswith('nii.gz')])
    image_file_list = image_file_list[(case-1)*2:(case-1)*2+2]   
    for i in range(len(image_file_list)):
        image_file_list[i] = os.path.join(data_folder, image_file_list[i])
    #Returning the exhale, inhale pair given by case
    path_e = image_file_list[0]
    path_i = image_file_list[1]
    print(path_e, path_i)
    return path_e, path_i

def loadlm(data_folder, case):
    #Getting all the landmark files in the folder
    files_old = sorted(os.listdir(data_folder))
    files = []
    for i in files_old:
        if i.endswith('xyz_r1.txt'):
            files.append(data_folder + '/' + i)
    files = files[(case-1)*2:(case-1)*2+2]   
    #Returning the exhale, inhale pair given by case
    lm_e = files[0]
    lm_i = files[1]
    print(lm_e, lm_i)
    return lm_e, lm_i