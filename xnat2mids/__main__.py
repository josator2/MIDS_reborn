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
# serialize model to json

from xnat import *
from mids_conversion import *
from variables import *


###############################################################################
# Functions
###############################################################################
def list_directory_xnat(project_list):
    loop = True
    project_names = [path_.split(os.sep)[-1] for path_ in project_list]
    while loop:
        for i, project_item in enumerate(project_names):
            if not i % 5:
                print((""))
            string = str(i + 1) + ") " + project_item
            print("{0:20s}".format(string), end=" ", flush=True)
        answer = input("\nChoose the project: ")
        answer = str(answer)
        answer_list = []
        answer_list_aux = answer.split(' ')

        for ans in answer_list_aux:
            if ans.isdigit():
                ans = int(ans) - 1
                if ans >= len(project_names):
                    print("the number " + ans + " is not corrected, try again", flush=True)
                    break
                else:
                    answer_list.append(project_names[ans])
            else:
                if not (any([ans in path_ for path_ in project_names])):
                    if ans == "exit":
                        exit(1)
                    else:
                        print("the project " + ans
                              + " is not corrected, try again")
                        break
                else:
                    answer_list.append(ans)
        else:
            loop = False

    return answer_list


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
    args = parser.parse_args()
    print(reset_terminal, end="", flush=True)

    page = args.web
    user = args.user
    xnat_data_path = args.input
    mids_data_path = args.output
    project_list = args.projects
    verbose = args.verbose
    body_part = args.body_part
    types = args.types[0]
    overwrite = args.overwrite

    if xnat_data_path and page:
        with xnat.Xnat_Session(page, user) as xnat_session:
            xnat_session.download_projects(
                xnat_data_path,
                with_department=True,
                project_list=project_list,
                bool_list_resources=[char in types for char in types_files_xnat],
                overwrite=overwrite,
                verbose=verbose
            )
    # conditions to move xnat project to MIDS project
    if xnat_data_path and mids_data_path and body_part:
        # if project_list is None, the projects in the folder xnat must be
        # chosen
        if not project_list:
            project_paths = [dirs for dirs in os.listdir(xnat_data_path)]
            project_list = list_directory_xnat(project_paths)
        project = xnat_data_path.split("/")[-2]
        if not os.path.isdir(mids_data_path):
            os.mkdir(args.output)
        mids_data_path = args.output
        # for each project choice
        for xnat_project in project_list:
            print("MIDS are generating...")
            MIDS_funtions.create_directory_mids_v1(
                os.path.join(xnat_data_path, xnat_project),
                mids_data_path,
                body_part
            )

            print("participats tsv are generating...")
            MIDS_funtions.create_participants_tsv(
                os.path.join(mids_data_path, xnat_project)
            )

            print("scan tsv are generating...")
            MIDS_funtions.create_scans_tsv(
                os.path.join(mids_data_path, xnat_project)
            )

            print("sessions tsv are generating...")
            MIDS_funtions.create_sessions_tsv(
                os.path.join(xnat_data_path, xnat_project),
                mids_data_path
            )