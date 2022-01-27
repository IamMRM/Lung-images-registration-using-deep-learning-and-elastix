import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

def plot_slices(num_rows, num_columns, width, height, data):
    """Plot slices of 3D volume (z-axis should be given in the 3rd dimension)"""
    data = np.rot90(np.array(data))
    data = np.transpose(data)
    data = np.reshape(data, (num_rows, num_columns, width, height))
    rows_data, columns_data = data.shape[0], data.shape[1]
    
    heights = [slc[0].shape[0] for slc in data]
    widths = [slc.shape[1] for slc in data[0]]
    fig_width = 12.0
    fig_height = fig_width * sum(heights) / sum(widths)
    f, axarr = plt.subplots(
        rows_data,
        columns_data,
        figsize=(fig_width, fig_height),
        gridspec_kw={"height_ratios": heights},
    )
    for i in range(rows_data):
        for j in range(columns_data):
            axarr[i, j].imshow(data[i][j], cmap="gray")
            axarr[i, j].axis("off")
    plt.subplots_adjust(wspace=0, hspace=0, left=0, right=1, bottom=0, top=1)
    plt.show()

def basic_plot(volume, slice, title):
    plt.imshow(volume[slice,:,:],);plt.axis('off');plt.title(title)

def basic_plot_lm(volume, slice, title, lm):
    plt.imshow(volume[slice,:,:],);plt.axis('off');plt.title(title)
    plt.scatter(x=lm[lm[:,2]==slice][:,0], y=lm[lm[:,2]==slice][:,1], c='r', s=1);plt.axis('off')

def basic_plot_def(path, slice, title):
    def_f = sitk.GetArrayFromImage(sitk.ReadImage(path + '/deformationField.nii.gz'))
    def_f = np.sqrt(np.sum(np.power(def_f,2),3))
    plt.imshow(def_f[slice,:,:],);plt.axis('off');plt.title(title)
