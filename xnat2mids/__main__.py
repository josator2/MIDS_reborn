#!/usr/bin/env  python   #iniciaize enviroment
# -*- coding: utf-8 -*-.
u"""
Subdirección General de Sistemas de Información para la Salud

Centro de Excelencia e Innovación Tecnológica de Bioimagen de la Conselleria de Sanitat

http://ceib.san.gva.es/

María de la Iglesia Vayá -> delaiglesia_mar@gva.es or miglesia@cipf.es

Jose Manuel Saborit Torres -> jmsaborit@cipf.es

Jhon Jairo Saenz Gamboa ->jsaenz@cipf.es

Joaquim Ángel Montell Serrano -> jamontell@cipf.es

---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.

---

Prerequisites

Python --version >= 3.8

Description:
    This application allow the user to download one project on XNAT and
    transform this project in MIDS format

    There are 2 functions in this code:
        download one project from xnat application:
        arguments:
            Prefix  -w --web PAGE_WEB        1) The URL page where XNAT is.
            Prefix  -p --project [PROJECTS]  2) The project name to download
            Prefix  -i --input PATH          3) the directory where the files
                                                will be downloaded
            Prefix  -u --user [USER]         4) The username to login in XNAT
                                                If not write a username, It
                                                loggin as guest.

        Convert the xnat directories of the project in MIDS format:
        arguments:
            Prefix      -i --input      PATH   1) the directory where the files will
                                        be downloaded
            Prefix      -o --output     PATH   2) Directory where the MIDS model
                                        is applied.
"""
###############################################################################
# Imports
###############################################################################

import os
import argparse
from pathlib import Path
# serialize model to json

from xnat2mids.xnat.xnat_session import XnatSession
from xnat2mids.xnat.xnat_session import list_directory_xnat
#import mids_conversion
from xnat2mids.variables import types_files_xnat
from xnat2mids.variables import format_message
from xnat2mids.variables import reset_terminal
from xnat2mids.variables import dict_paths
from xnat2mids.variables import dict_uris
from xnat2mids.mids_conversion import  create_directory_mids_v1
from xnat2mids.mids_conversion import create_tsvs


###############################################################################
# Functions
###############################################################################


def main():
    """
    This Fuction is de main programme
    """
    # Control of arguments of programme
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description="""
    This sorfware allows the user to Download one project into XNAT platform
    of BIMCV and convert the XNAT images directory in a MIDS directory.

    The aplication execution needs Python --version >= 3.5.

    there are 2 functions in this code:

      Download temporary projects from xnat application:

         arguments:
          + Prefix    -w --web PAGE_WEB         1) The URL page where XNAT is.

          + Prefix    -u --user [USER]          2) The username to login in XNAT
                                                If not write a username, It logins
                                                as guest.

          + Prefix    -p --project [PROJECT]    3) The project name to download,
                                                if the project is omitted, the
                                                application shows all projects in
                                                xnat to choice.

          + Prefix    -i --input INPUT          4) The directory where the
                                                files will be downloaded.

          + Prefix    -t --types [sdnbr]         5) Download types of MRI images
                                                   included in xnat
                                                   - d = dicom + dicom metadata in
                                                         folder NIFTI
                                                   - n = nifti or png if image is
                                                         one slide (2D) + roi
                                                   - b = BIDS (only in CENTRAL XNAT)
                                                   - r = Structural report
                                                   default = nr


          + Prefix    --overwrite                5) Overwrite download files


      Convert the xnat directories of the project in MIDS format:

        arguments:

          + Prefix    -i --input INPUT          1) The directory where the files
                                                will be downloaded.

          + Prefix    -o --output OUTPUT        2) Directory where the MIDS model
                                                is applied.
          + Prefix    -bp --body-part           3) Specify which part of the body are 
                                                    in the dataset(A clear dataset with
                                                    only one part are needed)
        """
    )
    parser.add_argument('-w', '--web', type=str, default=None,
                        help='The URL page where XNAT is.')
    parser.add_argument('-u', '--user', type=str, default=None,
                        help="""The username to login in XNAT
                                    If not write a username, It logins
                                    as guest.""")
    parser.add_argument('-i ', '--input', type=str,
                        help="""the directory where the files will
                            be downloaded.""")
    parser.add_argument('-o ', '--output', type=str,
                        help='Directory where the MIDS model is applied.')
    parser.add_argument('-p ', '--projects', nargs='*', default=None, type=str,
                        help="""The project name to download, if the project is
                            omitted,the aplication show all projects in xnat
                            to choice.""")
    parser.add_argument('-v ', '--verbose', default=False, action='store_true',
                        help="""Active Verbose""")
    parser.add_argument('-bp', '--body-part', dest="body_part", type=str,
                       help="""Specify which part of the body are 
                        in the dataset(A clear dataset with only one part are needed)""")
    parser.add_argument('--overwrite', default=False, action='store_true',
                        help=""" Overwrite download files""")
    parser.add_argument('-t', '--types', type=str, default="nr", nargs=1,
                        help="""Download types of MRI images
                            included in xnat
                            - s = snapshoot
                            - d = dicom + dicom metadata in folder NIFTI
                            - n = nifti or png if image is one slide (2D)
                            - r = Structural report
                            - m = Roi segmentation (Mask)
                            default = nr""")
    args = parser.parse_args()
    print(reset_terminal, end="", flush=True)
    print(args)
    page = args.web
    user = args.user
    xnat_data_path = Path(args.input) if args.input else None
    mids_data_path = Path(args.output) if args.output else None
    project_list = args.projects
    verbose = args.verbose
    body_part = args.body_part
    types = args.types[0]
    overwrite = args.overwrite

    if xnat_data_path and page:
        xnat_data_path.mkdir(exist_ok=True)
        with XnatSession(page, user) as xnat_session:
            xnat_session.download_projects(
                xnat_data_path,
                with_department=True,
                project_list=project_list,
                bool_list_resources=[True for char in types_files_xnat],
                overwrite=overwrite,
                verbose=verbose
            )
    # conditions to move xnat project to MIDS project
    if xnat_data_path and mids_data_path and body_part:
        # if project_list is None, the projects in the folder xnat must be
        # chosen
        if not project_list:
            project_paths = [dirs for dirs in xnat_data_path.iterdir()]
            project_names = [path_.name for path_ in project_paths]
            project_list = list_directory_xnat(project_names)
        mids_data_path.mkdir(exist_ok=True)
        # for each project choice
        for xnat_project in project_list:
            print("MIDS are generating...")
            # create_directory_mids_v1(
            #     xnat_data_path.joinpath(xnat_project),
            #     mids_data_path,
            #     body_part
            # )

            print("participats tsv are generating...")
            create_tsvs(xnat_data_path.joinpath(xnat_project), mids_data_path.joinpath(xnat_project))

            # print("scan tsv are generating...")
            # MIDS_funtions.create_scans_tsv(
            #     os.path.join(mids_data_path, xnat_project)
            # )
            #
            # print("sessions tsv are generating...")
            # MIDS_funtions.create_sessions_tsv(
            #     os.path.join(xnat_data_path, xnat_project),
            #     mids_data_path
            # )

if __name__ == "__main__":
    main()