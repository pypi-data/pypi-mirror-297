def exclusion_policy():
    """Returns a callable which, when passed a directory path and a list
    of files in that directory, will return a subset of the files which should
    be excluded from a copy or some other action.

    See https://docs.python.org/3/library/shutil.html#shutil.ignore_patterns

    Adapted from dallinger.utils.exclusion_policy
    """
    patterns = set(
        [
            ".git",
            "snapshots",
        ]
    )

    return shutil.ignore_patterns(*patterns)


def get_directory_size(directory):
    """Returns the size of an (experiment) directory in MB.

    Inspired and adapted from dallinger.utils.ExperimentFileSource
    """
    total_size = 0
    exclusions = exclusion_policy()

    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        current_exclusions = exclusions(dirpath, os.listdir(dirpath))

        # Modifying dirnames in-place will prune the subsequent files and
        # directories visited by os.walk. This is only possible when
        # topdown = True
        dirnames[:] = [d for d in dirnames if d not in current_exclusions]

        git_filepaths = {
            os.path.join(os.path.abspath("."), normalize("NFC", f))
            for f in GitClient().files()
        }
        legit_filepaths = {
            os.path.join(dirpath, f) for f in filenames if f not in current_exclusions
        }
        if git_filepaths:
            normalized = {normalize("NFC", str(f)): f for f in legit_filepaths}
            legit_filepaths = {v for k, v in normalized.items() if k in git_filepaths}

        for filepath in legit_filepaths:
            print(f"Adding: {filepath}")
            total_size += os.path.getsize(filepath)

    print(total_size)
    return total_size
