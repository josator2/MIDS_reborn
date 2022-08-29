class scan_resources(dict):
    def __init__(self, scan, level_verbose, level_tab, **kwargs):
        super().__init__(**kwargs)
        self["scan"] = scan
        self.level_verbose = level_verbose
        self.level_tab = level_tab

    def get_list_files(self, verbose):
        output = StringIO()
        if verbose: print(format_message(self.level_verbose, self.level_tab, f"resource: {self['label']}"), end=" ----> ",
                          flush=True)
        file_text = try_to_request(
            self["scan"]["session"]["subject"]["project"].interface,
            self["scan"]["session"]["subject"]["project"].url_xnat
            + dict_uri["files"](
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
                path_download + dict_path["path_download"](
            self["scan"]["session"]["subject"]["ID"],
            self["scan"]["session"]["ID"],
            self["scan"]["ID"],
            self["label"]
        )
        )
        complet_path_metadata = (
                path_download + dict_path["path_download"](
            self["scan"]["session"]["subject"]["ID"],
            self["scan"]["session"]["ID"],
            self["scan"]["ID"],
            "NIFTI"
        )
        )

        dicom_path = os.path.join(complet_path, filename)
        dicom_path_metadata = os.path.join(complet_path_metadata, "dicom.json")
        if not overwrite and (os.path.exists(dicom_path) and os.path.exists(dicom_path_metadata)):
            #if verbose: print("DICOM file already exist")
            return dicom_path, dicom_path_metadata
        # if not overwrite and os.path.exists(dicom_path):
        #    if verbose: print("          DICOM metadata file already exist")
        #    return
        if verbose:
            pass
            #print("Downloading DICOM file...", flush=True, end="")
            # print("          Downloading DICOM  Metadata file...",flush=True)

        os.makedirs(complet_path, exist_ok=True)
        os.makedirs(complet_path_metadata, exist_ok=True)
        try:
            copyfile(dict_uri["local_files"](
                self["scan"]["session"]["subject"]["project"]["ID"],
                self["scan"]["session"]["label"],
                self["scan"]["ID"],
                self["label"],
                filename

            ), dicom_path)
        except FileNotFoundError as e:
            url_dicom = (self["scan"]["session"]["subject"]["project"].url_xnat
                         + dict_uri["files"](
                        self["scan"]["session"]["subject"]["project"]["ID"],
                        self["scan"]["session"]["subject"]["ID"],
                        self["scan"]["session"]["ID"],
                        self["scan"]["ID"],
                        self["label"]
                    ).split("?")[0] + "/"
                         + filename
                         )

            #with open(path_download + "urls_descarga.txt", "a") as f:
            #    f.write("%s \n %s # %r # %r # %r \n" % (
            #        url_dicom, dicom_path, overwrite, verbose, os.path.exists(dicom_path)))
            #    f.close()

            dicom = try_to_request(
                self["scan"]["session"]["subject"]["project"].interface,
                url_dicom
            )
            # nifti = self["scan"]["session"]["subject"]["project"].interface.get(url_nifti, allow_redirects=True)
            dicom.raise_for_status()

            with open(dicom_path, 'wb') as dicom_file:
                dicom_file.write(dicom.content)

        return dicom_path, dicom_path_metadata

    def download_nifti(self, path_download, filename, overwrite=False, verbose=False):
        complet_path = (path_download + dict_path["path_download"](
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
                     + dict_uri["files"](
                    self["scan"]["session"]["subject"]["project"]["ID"],
                    self["scan"]["session"]["subject"]["ID"],
                    self["scan"]["session"]["ID"],
                    self["scan"]["ID"],
                    self["label"]
                ).split("?")[0] + "/"
                     + filename
                     )

        #with open(path_download + "urls_descarga.txt", "a") as f:
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

    def download_bids(self):
        pass

    def download_png(self, path_download, filename, overwrite=False, verbose=False):
        complet_path = (path_download + dict_path["path_download"](
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
                   + dict_uri["files"](
                    self["scan"]["session"]["subject"]["project"]["ID"],
                    self["scan"]["session"]["subject"]["ID"],
                    self["scan"]["session"]["ID"],
                    self["scan"]["ID"],
                    self["label"]
                ).split("?")[0] + "/"
                   + filename
                   )

        #with open(path_download + "urls_descarga.txt", "a") as f:
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

    def download(
            self,
            path_download,
            bool_list_resources=[False, False, True, False, False, False],
            overwrite=False,
            verbose=False
    ):

        self.get_list_files(verbose)
        is_metadata_saved = False

        for index, file_obj in enumerate(self.dict_resources.values()):

            if self["label"] == "DICOM" and bool_list_resources[1]:
                print(format_message(self.level_verbose + 1, self.level_tab + 1, f"{index} of {self['file_count']}"), end="",
                      flush=True)
                #self.download_dicom(path_download, file_obj["Name"], overwrite=overwrite, verbose=verbose)

            if self["label"] == "SECONDARY" and bool_list_resources[2]:
                #self.download_dicom(path_download, file_obj["Name"], overwrite=overwrite, verbose=verbose)
                pass
        print(format_message(self.level_verbose, self.level_tab, "\u001b[0K"), end="", flush=True)
        print(format_message(self.level_verbose+1, self.level_tab+1, "\u001b[0K"), end="", flush=True)
