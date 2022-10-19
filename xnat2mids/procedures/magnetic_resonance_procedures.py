from shutil import copyfile

import nibabel as nib
from xnat2mids.dicom_converters import dicom2niix

body_part_bids = ['head','brain']

class ProceduresMR:
    def __init__(self):
        self.reset_indexes()

    def reset_indexes(self):
        """Reset all values in dictionary of the atribute "dict_indexes"."""

        self.run_dict = {}


    def control_sequences(
        self, folder_nifti, mids_session_path, session_name,  protocol, acq, dir_, folder_BIDS, body_part
    ):

        folder_image_mids = mids_session_path.joinpath(
             "" if body_part in body_part_bids else "mim-mr",
            folder_BIDS
        )
        folder_image_mids.mkdir(parents=True, exist_ok=True)



        self.control_image(folder_nifti, folder_image_mids, session_name, protocol, acq, dir_, body_part)

    def control_image(self, nifti_path, folder_image_mids, session_name, protocol, acq, dir_, body_part):

        """

        """


        # Search all nifti files in the old folder and sort them
        nifti_files = sorted([i for i in nifti_path.glob("*.nii.gz")])

        len_nifti_files = len(nifti_files)
        if len_nifti_files == 0: return

        # This is a counter for several nifties in one adquisition


        print("processing file -> ", nifti_files)
        protocol_label = f'_{protocol}'
        acq_label = f'_acq-{acq}' if acq else ''
        bp_label = f"" if body_part in body_part_bids else f"_bp-{body_part}"
        vp_label = [
            (
                f"_desc-{self.get_plane_nib(nifti_file)}"
                if body_part in body_part_bids
                else f"_vp-{self.get_plane_nib(nifti_file)}"
            )
            for nifti_file in nifti_files
        ]
        key = str([session_name, protocol_label, acq_label, bp_label, dir_, vp_label])
        value = self.run_dict.get(key, [])
        value.append([nifti_files, folder_image_mids])
        self.run_dict[key] = value

    def copy_sessions(self, subject_name):
        for key, value in self.run_dict.items():

            print("-"*79)
            list_key = eval(key)
            print(key, value)
            print("-" * 79)
            list_of_sesions = value


    def get_plane_nib(self, nifti):
        """
            Calculate the type of plane with the tag image orientation patient
            in dicom metadata.
        """

        img = nib.load(nifti)
        plane = nib.aff2axcodes(img.affine)[2]
        return "ax" if plane in ["S", "I"] else "sag" if plane in ["R", "L"] else "cor"



