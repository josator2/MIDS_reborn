import dicom2nifti
import pathlib
import SimpleITK as sitk
import dicom2nifti.settings as settings
import subprocess
def sitk_dicom2mifti(dicom_path):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_path.parent)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()

    # Added a call to PermuteAxes to change the axes of the data
    image = sitk.PermuteAxes(image, [2, 1, 0])

    sitk.WriteImage(image, 'nifti.nii.gz')

def dicom2nii(dicom_path):
    #settings.disable_validate_slice_increment()
    print(dicom_path.parent)
    nifti_path = dicom_path.parent.parent.parent.joinpath("LOCAL_NIFTI", "files")
    nifti_path.mkdir(parents=True, exist_ok=True)
    #dicom2nifti.convert_directory(dicom_path.parent, nifti_path,  compression=True, reorient_nifti=True)
    array_nifty = dicom2nifti.convert_dicom.dicom_series_to_nifti(str(dicom_path.parent),str(nifti_path), reorient_nifti=True)
    #save_dicom_metadata(
    #    dicom_path, nifti_path.parent.joinpath(nifti_path.name.split(".")[0] + ".json")
    #)
    return array_nifty
def dicom2niix(folder_json, str_options):
    folder_nifti = folder_json.parent.parent.parent.joinpath("LOCAL_NIFTI", "files")
    folder_nifti.mkdir(parents=True, exist_ok=True)
    subprocess.call(f"dcm2niix {str_options} -o {folder_nifti} {folder_json.parent}", shell=True)
    return folder_nifti
def dicom2png(dicom_path, nifti_path):

    sitk_img = sitk.ReadImage(path_to_dicom)
    #img = sitk.GetArrayFromImage(sitk_img)[0, :, :]
    sitk.WriteImage(sitk_img, path_to_png)
    save_dicom_metadata(
        dicom_path, nifti_path.parent.joinpath(nifti_path.name.split(".")[0] + ".json")
    )

def save_dicom_metadata(dicom_path, json_path):

    dicom = dicom2nifti.common.read_dicom_directory(dicom_path, stop_before_pixels=True)
    try:
        string_json = dicom.to_json()
    except TypeError as e:
        string_json = "{}"
    dict_json = json.loads(string_json)
    string_json = json.dumps(dict_json, default=lambda o: o.__dict__,
                             sort_keys=True)
    with open(json_path, 'w') as dicom_file:
        dicom_file.write(string_json)