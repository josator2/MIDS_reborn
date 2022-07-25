types_files_xnat = "sdnbrm"

reset_terminal = chr(27) + "[2J"

dict_path = {
    "path_download": lambda s, e, sc, r: "{}/{}/scans/{}/resources/{}/files/".format(s, e, sc, r),
    "path_download_roi": lambda s, e, ass, r: "{}/{}/assessors/{}/out/resources/{}/files".format(s, e, ass, r),
    "path_sr": lambda s, e: "{}/{}/resources/sr/files".format(s, e)
}

dict_uri = {
    "projects": "data/projects?format=csv",
    "subjects": lambda p: "data/projects/{}/subjects?format=csv".format(p),
    "experiments": lambda p, s: "data/projects/{}/subjects/{}/experiments?format=csv".format(p, s),
    "struct_reports": (
        lambda p, s, e: "data/projects/{}/subjects/{}/experiments/{}/resources/sr/files?format=csv".format(p, s, e)
    ),
    "assessors": lambda p, s, e: "data/projects/{}/subjects/{}/experiments/{}/assessors?format=csv".format(p, s, e),
    "assessors_resources": (
        lambda p, s, e, ass:
        "data/projects/{}/subjects/{}/experiments/{}/assessors/{}/out/resources?format=csv".format(p, s, e, ass)
    ),
    "roi_files": (
        lambda p, s, e, ass, r:
        "data/projects/{}/subjects/{}/experiments/{}/assessors/{}/out/resources/{}/files?format=csv".format(
            p, s, e, ass, r
        )
    ),
    "scans": lambda p, s, e: "data/projects/{}/subjects/{}/experiments/{}/scans?format=csv".format(p, s, e),
    "resources": (
        lambda p, s, e, sc:
        "data/projects/{}/subjects/{}/experiments/{}/scans/{}/resources?format=csv".format(p, s, e, sc)
    ),
    "files": (
        lambda p, s, e, sc, r:
        "data/projects/{}/subjects/{}/experiments/{}/scans/{}/resources/{}/files?format=csv".format(p, s, e, sc, r)
    ),
    "local_files": (
        lambda p, e, sc, r, f: "/mnt/datalake/xnat2_data/archive/{}/arc001/{}/SCANS/{}/{}/{}".format(p, e, sc, r, f)
    ),
}


def format_message (line, tab_value, message):
    return "\033[{:d};0H{:s}{:s}".format(
        line,
        "  " * tab_value + ("-> " if tab_value > 0 else ""),
        message)


def fformat_message (line, tab_value, message):
    return f"\033[{line};0H{'  ' * tab_value + ('-> ' if tab_value > 0 else '')}{message}"
 > 0 else "")}{message}'