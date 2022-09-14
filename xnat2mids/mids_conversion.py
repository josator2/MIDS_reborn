
from xnat2mids.procedures.magnetic_resonance_procedures import procedures_mr


subject_pattern = "[A-z]+(?P<prefix>\d*)?(_S)(?P<suffix>\d+)"
sesion_pattern = "[A-z]+(?P<prefix>\d+)?(_E)(?P<suffix>\d+)"
def create_directory_mids_v1(xnat_data_path, mids_data_path):

    procedure_class_mr = procedures_mr()
    for sessions_xnat_path in Path(xnat_data_path).glob('*/*/'):
        procedure_class_mr.reset_indexes()
        department = str(sessions_xnat_path).split('/')[-3]