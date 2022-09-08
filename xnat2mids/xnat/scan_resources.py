import csv
import os
import pydicom
import json
from io import StringIO
from shutil import copyfile

from xnat2mids.variables import format_message
from xnat2mids.variables import dict_uris
from xnat2mids.variables import dict_paths

from xnat2mids.request import try_to_request


class ScanResources(dict):
    def __init__(self, scan, level_verbose, level_tab, **kwargs):
        super().__init__(**kwargs)
        self["scan"] = scan
        self.level_verbose = level_verbose
        self.level_tab = level_tab

    def get_list_files(self, verbose):
        output = StringIO()
        if verbose: print(format_message(self.level_verbose, self.level_tab, f"resource: {self['label']}"),
                          end=" ----> ",
                          flush=True)
        file_text = try_to_request(
            self["scan"]["session"]["subject"]["project"].interface,
            self["scan"]["session"]["subject"]["project"].url_xnat
            + dict_uris["scan_resource_files"](
                self["scan"]["session"]["subject"]["project"]["ID"],
                self["scan"]["session"]["subject"]["ID"],
                self["scan"]["session"]["ID"],
                self["scan"]["ID"],
                self["label"]
            )
        )
        file_text.raise_for_status()
        output.write(file_text.text)
        output.seek(0)
        reader = csv.DictReader(output)
        self.dict_resources = dict()
        for row in reader:
            self.dict_resources[row["Name"]] = dict(**row)
        output.close()

    def download_dicom(self, path_download, filename, overwrite=False, verbose=False):

        complet_path = (
                path_download + dict_paths["path_download"](
            self["scan"]["session"]["subject"]["ID"],
            self["scan"]["session"]["ID"],
            self["scan"]["ID"],
            self["label"]
        )
        )
        complet_path_metadata = (
            path_download + dict_paths["path_download"](
                self["scan"]["session"]["subject"]["ID"],
                self["scan"]["session"]["ID"],
                self["scan"]["ID"],
                "DICOM"
            )
        )

        dicom_path = os.path.join(complet_path, filename)
        dicom_path_metadata = os.path.join(complet_path_metadata, "dicom.json")
        if not overwrite and (os.path.exists(dicom_path)) and (os.path.exists(dicom_path_metadata)):
            #    #if verbose: print("DICOM file already exist")
            return

        os.makedirs(complet_path, exist_ok=True)
        os.makedirs(complet_path_metadata, exist_ok=True)

        url_dicom = (self["scan"]["session"]["subject"]["project"].url_xnat
                     + dict_uris["scan_resource_files"](
                    self["scan"]["session"]["subject"]["project"]["ID"],
                    self["scan"]["session"]["subject"]["ID"],
                    self["scan"]["session"]["ID"],
                    self["scan"]["ID"],
                    self["label"]
                ).split("?")[0] + "/"
                     + filename
                     )

        dicom = try_to_request(
            self["scan"]["session"]["subject"]["project"].interface,
            url_dicom
        )
        # nifti = self["scan"]["session"]["subject"]["project"].interface.get(url_nifti, allow_redirects=True)
        dicom.raise_for_status()

        with open(dicom_path, 'wb') as dicom_file:
            dicom_file.write(dicom.content)

        if not self.is_metadata_saved:
            self.is_metadata_saved = True
            self.store_metadata(dicom_path, dicom_path_metadata.format("DICOM"))

    def download_nifti(self, path_download, filename, overwrite=False, verbose=False):
        complet_path = (path_download + dict_paths["path_download"](
            self["scan"]["session"]["subject"]["ID"],
            self["scan"]["session"]["ID"],
            self["scan"]["ID"],
            self["label"]
        )
                        )

        nifti_path = os.path.join(complet_path, filename)
        if not overwrite and os.path.exists(nifti_path):
            if verbose: print("nifti file already exist")
            return
        if verbose: print("Downloading NIFTI file...", flush=True)
        os.makedirs(complet_path, exist_ok=True)
        url_nifti = (self["scan"]["session"]["subject"]["project"].url_xnat
                     + dict_uris["scan_resource_files"](
                    self["scan"]["session"]["subject"]["project"]["ID"],
                    self["scan"]["session"]["subject"]["ID"],
                    self["scan"]["session"]["ID"],
                    self["scan"]["ID"],
                    self["label"]
                ).split("?")[0] + "/"
                     + filename
                     )

        # with open(path_download + "urls_descarga.txt", "a") as f:
        #    f.write(
        #        "%s \n %s # %r # %r # %r \n" % (url_nifti, nifti_path, overwrite, verbose, os.path.exists(nifti_path)))
        #    f.close()
        nifti = try_to_request(
            self["scan"]["session"]["subject"]["project"].interface,
            url_nifti
        )
        # nifti = self["scan"]["session"]["subject"]["project"].interface.get(url_nifti, allow_redirects=True)
        nifti.raise_for_status()

        with open(os.path.join(complet_path, filename), 'wb') as nifti_file:
            nifti_file.write(nifti.content)


    def download_png(self, path_download, filename, overwrite=False, verbose=False):
        complet_path = (path_download + dict_paths["path_download"](
            self["scan"]["session"]["subject"]["ID"],
            self["scan"]["session"]["ID"],
            self["scan"]["ID"],
            self["label"]
        )
                        )

        png_path = os.path.join(complet_path, filename)
        if not overwrite and os.path.exists(png_path):
            if verbose: print("png file already exist")
            return
        if verbose: print("Downloading png file...", flush=True)
        os.makedirs(complet_path, exist_ok=True)
        url_png = (self["scan"]["session"]["subject"]["project"].url_xnat
                   + dict_uris["scan_resource_files"](
                    self["scan"]["session"]["subject"]["project"]["ID"],
                    self["scan"]["session"]["subject"]["ID"],
                    self["scan"]["session"]["ID"],
                    self["scan"]["ID"],
                    self["label"]
                ).split("?")[0] + "/"
                   + filename
                   )

        # with open(path_download + "urls_descarga.txt", "a") as f:
        #    f.write("%s \n %s # %r # %r # %r \n" % (url_png, png_path, overwrite, verbose, os.path.exists(png_path)))
        #    f.close()
        png = try_to_request(
            self["scan"]["session"]["subject"]["project"].interface,
            url_png
        )
        # png = self["scan"]["session"]["subject"]["project"].interface.get(url_png, allow_redirects=True)
        png.raise_for_status()

        with open(os.path.join(complet_path, filename), 'wb') as png_file:
            png_file.write(png.content)

    def store_metadata(self, dicom_path, dicom_path_metadata):

        dicom = pydicom.dcmread(dicom_path, stop_before_pixels=True)
        try:
            string_json = dicom.to_json(suppress_invalid_tags=True)
        except TypeError as e:
            self.is_metadata_saved = False
            return
        dict_json = json.loads(string_json)
        # del dict_json["7FE00010"]
        string_json = json.dumps(dict_json, default=lambda o: o.__dict__,
                                 sort_keys=True)
        with open(dicom_path_metadata, 'w') as dicom_file:
            dicom_file.write(string_json)

    def download(
            self,
            path_download,
            bool_list_resources=[False, False, True, False, False, False],
            overwrite=False,
            verbose=False
    ):

        self.get_list_files(verbose)
        self.is_metadata_saved = False
        dicom_path, dicom_path_metadata = "", ""
        for index, file_obj in enumerate(self.dict_resources.values()):

            if self["label"] == "DICOM":
                print(format_message(self.level_verbose + 1, self.level_tab + 1, f"{index} of {self['file_count']}"),
                      end="",
                      flush=True)
                dicom_path, dicom_path_metadata = self.download_dicom(
                    path_download, file_obj["Name"], overwrite=overwrite, verbose=verbose
                )

            if self["label"] == "NIFTI":
                self.download_nifti(path_download, file_obj["Name"], overwrite=overwrite, verbose=verbose)

            if self["label"] == "PNG":
                self.download_png(path_download, file_obj["Name"], overwrite=overwrite, verbose=verbose)

        print(format_message(self.level_verbose, self.level_tab, "\u001b[0K"), end="", flush=True)
        print(format_message(self.level_verbose + 1, self.level_tab + 1, "\u001b[0K"), end="", flush=True)
