import re

from xnat2mids import io_json
from xnat2mids.procedures.magnetic_resonance_procedures import ProceduresMR
from xnat2mids.protocols.scans_tagger import Tagger
from xnat2mids.dicom_converters import dicom2niix

subses_pattern = r"[A-z]+(?P<prefix_sub>\d*)?(_S)(?P<suffix_sub>\d+)/[A-z]+(?P<prefix_ses>\d*)?(_E)(?P<suffix_ses>\d+)"
dict_keys = {
    'Modality': '00080060',
    'SeriesDescription': '0008103E',
    'ProtocolName': '00181030',
    'ComplexImage Component Attribute': '00089208',
    "ImageType" :'00080008',
    #"difusion Directionality": ''
}

dict_mr_keys = {
    'Manufacturer': '00080070',
    'ScanningSequence': '00180020',
    'SequenceVariant': '00180021',
    'ScanOptions': '00180022',
    'AngioFlag': '00180025',
    'MagneticFieldStrength': '00180087',
    'RepetitionTime': '00180080',
    'InversionTime': '00180082',
    'FlipAngle': '00181314',
    'EchoTime': '00180081',
    'SliceThickness': '00180050',
}

BIOFACE_PROTOCOL_NAMES = [
    '3D-T2-FLAIR SAG',
    '3D-T2-FLAIR SAG NUEVO-1',
    'AAhead_scout',
    'ADVANCED_ASL',
    'AXIAL T2 TSE FS',
    'AX_T2_STAR',
    'DTIep2d_diff_mddw_48dir_p3_AP', #
    'DTIep2d_diff_mddw_4b0_PA', #
    'EPAD-3D-SWI',
    'EPAD-B0-RevPE', # PA
    'EPAD-SE-fMRI',
    'EPAD-SE-fMRI-RevPE',
    'EPAD-SingleShell-DTI48', # AP
    'EPAD-rsfMRI (Eyes Open)',
    'MPRAGE_GRAPPA2', # T1 mprage
    'asl_3d_tra_iso_3.0_highres',
    'pd+t2_tse_tra_p2_3mm',
    't1_mprage_sag_p2_iso', # t1
    't2_space_dark-fluid_sag_p2_iso', # flair
    't2_swi_tra_p2_384_2mm'
]

BIOFACE_PROTOCOL_NAMES_DESCARTED = [
    #'DTIep2d_diff_mddw_48dir_p3_AP',
    #'DTIep2d_diff_mddw_4b0_PA',
    'EPAD-B0-RevPE',
    'EPAD-SingleShell-DTI48',
    'EPAD-3D-SWI',
    'EPAD-SE-fMRI',
    'EPAD-rsfMRI (Eyes Open)',
    'EPAD-SE-fMRI-RevPE',
    'AAhead_scout',
    'ADVANCED_ASL',
    'MPRAGE_GRAPPA2',
    '3D-T2-FLAIR SAG',
    '3D-T2-FLAIR SAG NUEVO-1'
]

options_dcm2niix = "-w 0 -i y -m y -ba n -f %j_%p -z y"

def create_directory_mids_v1(xnat_data_path, mids_data_path, body_part):
    procedure_class_mr = ProceduresMR()
    for subject_xnat_path in xnat_data_path.glob('*/'):
        num_sessions = len(list(subject_xnat_path.glob('*/')))
        for sessions_xnat_path in subject_xnat_path.glob('*/'):
            #print(sessions_xnat_path)
            procedure_class_mr.reset_indexes()
            department = sessions_xnat_path.parts[-3]
            findings = re.search(subses_pattern, str(sessions_xnat_path), re.X)
            print('subject,', findings.group('prefix_sub'), findings.group('suffix_sub'))
            print('session,', findings.group('prefix_ses'), findings.group('suffix_ses'))
            subject_name = f"sub-{findings.group('prefix_sub')}S{findings.group('suffix_sub')}"
            session_name = f"ses-{findings.group('prefix_ses')}S{findings.group('suffix_ses')}"

            mids_session_path = mids_data_path.joinpath(department, subject_name, session_name)
            xml_session_rois = list(sessions_xnat_path.rglob('*.xml'))

            tagger = Tagger()
            tagger.load_table_protocol(
                '/home/josator2/Documentos/projects/MIDS_reborn/xnat2mids/protocols/protocol_RM_brain_siemens.tsv'
            )

            for scans_path in sessions_xnat_path.joinpath("scans").iterdir():
                print(scans_path)
                print("numero de jsons:", len(list(scans_path.joinpath("resources", "DICOM", "files").glob("*.dcm"))))


                folder_nifti = dicom2niix(scans_path.joinpath("resources", "DICOM", "files"), options_dcm2niix)
        #         print(f"longitud archivos en {folder_nifti}: {len(list(folder_nifti.iterdir()))}")
        #         print(list(folder_nifti.iterdir()))
        #         if len(list(folder_nifti.iterdir())) == 0: continue
        #
        #
        #
        #
        #         dict_json = io_json.load_json(folder_nifti.joinpath(list(folder_nifti.glob("*.json"))[0]))
        #
        #
        #         modality = dict_json.get("Modality", "n/a")
        #         study_description = dict_json.get("SeriesDescription", "n/a")
        #         image_type = dict_json.get("ImageType", "n/a")
        #         if modality == "MR":
        #             # via BIDS protocols
        #             if body_part in ["head", "brain"]:
        #                 ProtocolName = dict_json.get("ProtocolName", "n/a")
        #                 if ProtocolName not in BIOFACE_PROTOCOL_NAMES_DESCARTED:
        #                     if 'AP' in  ProtocolName:
        #                         protocol, acq, dir_, folder_BIDS = ["dwi", None, "AP", "dwi"]
        #                     elif 'PA' in ProtocolName:
        #                         protocol, acq, dir_, folder_BIDS = ["dwi", None, "PA", "dwi"]
        #                     else:
        #                         print(dict_json)
        #                         json_adquisitions = {
        #                             f'{k} (\'{v}\')': dict_json.get(k, "nan") for k, v in dict_mr_keys.items()
        #                         }
        #                         dir_ = ''
        #                         protocol, acq, folder_BIDS = tagger.classification_by_min_max(json_adquisitions)
        #
        #                     print(protocol, acq, dir_, folder_BIDS)
        #
        #                     procedure_class_mr.control_sequences(
        #                         folder_nifti, mids_session_path, session_name, protocol, acq, dir_, folder_BIDS, body_part
        #                     )
        # procedure_class_mr.copy_sessions(subject_name)

