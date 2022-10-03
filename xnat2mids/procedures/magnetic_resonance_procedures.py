from xnat2mids.dicom_converters import dicom2nii


class ProceduresMR:

    def reset_indexes(self):
        """Reset all values in dictionary of the atribute "dict_indexes"."""

        self.dict_indexes_MIDS = {}
        self.dict_indexes_BIDS = {}


    def convert_to_bids(
        self, json_path, mids_session_path, protocol, acq, folder_BIDS, body_part
    ):

        folder_to_image = mids_session_path.joinpath(folder_BIDS)
        folder_to_image.mkdir(parents=True, exist_ok=True)
        nifti_path = dicom2nii(json_path)

        if folder_BIDS == "dwi":
            pass
        if folder_BIDS == "anat":
            self.anatomic_procedure(nifti_path)
        if folder_BIDS == "fmap":
            pass
        if folder_BIDS == "func":
            pass
        if folder_BIDS == "perf":
            pass
    def anatomic_procedure(self, nifti_path):

        """
            Function that copies the elements to the anatomical folder of
            BIDS/MIDS structure.
        """


        # Search all nifti files in the old folder and sort them
        nifti_files = sorted([str(i) for i in nifti_path.glob("*.nii.gz")])

        len_nifti_files = len(nifti_files)
        if len_nifti_files == 0: return

        # This is a counter for several nifties in one adquisition
        for acq_index, nifti_file in enumerate(nifti_files, 1):





