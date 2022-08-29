class Subject(dict):
    def __init__(self, level_verbose, level_tab, **kwargs):
        super().__init__(**kwargs)
        self.level_verbose = level_verbose
        self.level_tab = level_tab

    def get_list_experiments(self, verbose):

        output = StringIO()
        if verbose: print(format_message(self.level_verbose, self.level_tab, f"Subject: {self['ID']}"), flush=True)
        output.write(
            try_to_request(
                self["project"].interface,
                self["project"].url_xnat
                + dict_uris["experiments"](self["project"]["ID"], self["ID"])
            ).text
        )
        output.seek(0)
        reader = csv.DictReader(output)
        self.dict_sessions = dict()
        for row in reader:
            self.dict_sessions[row["label"]] = Session(self, self.level_verbose + 1, self.level_tab + 1, **row)
        output.close()

    def download(self, path_download,
                 bool_list_resources=[False, False, True, False, False, False],
                 overwrite=False,
                 verbose=False
                 ):
        print("\033[6;0H\u001b[0K", end="", flush=True)
        self.get_list_experiments(verbose)
        # move the cursor
        for session_obj in self.dict_sessions.values():
            session_obj.download(
                path_download, bool_list_resources,
                overwrite=overwrite, verbose=verbose
            )

        print(format_message(self.level_verbose, self.level_tab, "\u001b[0K"), end="", flush=True)
