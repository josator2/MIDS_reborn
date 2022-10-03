import dicom2nifti
import pathlib
import SimpleITK as sitk
import dicom2nifti.settings as settings

def dicom2nii(dicom_path):
    settings.disable_validate_slice_increment()
    print(dicom_path.parent)
    nifti_path = dicom_path.parent.parent.joinpath("LOCAL_NIFTI", files)
    dicom2nifti.convert_directory(dicom_path.parent, nifti_path)
    #save_dicom_metadata(
    #    dicom_path, nifti_path.parent.joinpath(nifti_path.name.split(".")[0] + ".json")
    #)
    return nifti_path

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