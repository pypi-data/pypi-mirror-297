import textwrap
from dataclasses import dataclass, fields

from gigui.common import get_version
from gigui.constants import DEFAULT_EXTENSIONS, DEFAULT_N_FILES


# Help for GUI tooltips and for Help button
# All dataclass vars need to be declared with a type, otherwise, nothing works and var
# declarations are silently ignored.
@dataclass
class Tip:
    # IO configuration
    input_fstrs: str = "Absolute path(s) to repository, folders or URLs to be analysed"
    outfile_base: str = (
        "Name of output file without extension, prefix or postfix (default gitinspect)"
    )
    outfile_path: str = "Full path to Output file base with optional postfix or prefix"
    out_file_option: str = (
        "Whether to add a postfix or prefix to the output file base, "
        "see result in output file path above"
    )
    postfix: str = (
        "Construct output file name by postfixing output file base with repository"
    )
    prefix: str = (
        "Construct output file name by prefixing output file base with repository"
    )
    nofix: str = "Output file name equals output file base"
    depth: str = (
        "Number of levels of subfolders of the input folder path that is "
        "searched for repositories"
    )

    # Output formats excel
    format_excel: str = "Select output formats to be generated"
    auto: str = (
        "Single repo: open webview no output file, "
        "Multiple repos: open browser on html files"
    )
    html: str = "Generate html output"
    excel: str = "Generate excel output"
    scaled_percentages: str = (
        "Show percentages that are scaled (multiplied) by the number of authors in "
        "the repository"
    )
    blame_omit_exclusions: str = (
        "Omit from blame output: comments, empty lines and author lines that are excluded"
    )
    blame_skip: str = "Do not generate blame worksheets or blame tabs"
    subfolder: str = "Restrict analysis to a subfolder of the repository"
    file_options: str = (
        'For file selection, the file pattern for "Show files" has priority '
        'over "Show N files"'
    )
    n_files: str = (
        "For each repository generate output for the first N (default "
        f"{DEFAULT_N_FILES}) biggest files"
    )
    include_files: str = (
        "Generate output for all files matching any of the specified patterns (default "
        f"the {DEFAULT_N_FILES} biggest files)"
    )
    show_renames: str = (
        "Show previous file names and alternative author names and emails"
    )

    # General configuration
    deletions: str = "Include deletions in diffs"
    whitespace: str = "Include all whitespace in diffs and in copy move detection"
    empty_lines: str = "Include empty lines in blame calculations"
    comments: str = "Include comments in blame output"
    viewer: str = (
        "auto: open matching application to view output, none: never open any viewer"
    )
    copy_move: str = (
        "0: Ignore copy and move of lines, "
        "1: Detect copy move within file, "
        "2: and across files in one commit (default), "
        "3: and across two commits, "
        "4: across all commits"
    )
    verbosity: str = (
        "0: No debug output, "
        "1: Occasional output messages, "
        "2: Detailed debug output"
    )
    dry_run: str = (
        "0: normal execution, 1: analysis without output files, 2: no analysis no output files"
    )
    multi_thread: str = (
        "Analyse multiple files for changes and blames per repository using multiple threads"
    )
    multi_core: str = (
        "Execute multiple repositories using multiple cores, disabled for GUI"
    )
    since: str = "Only show statistics for commits more recent than a specific date"
    since_box: str = "Enter a date of the form 2022-12-31 or press the dot button"
    until: str = "Only show statistics for commits older than a specific date"
    until_box: str = since_box
    extensions: str = (
        "A comma separated list of file extensions to include when computing "
        "statistics. Default extensions are: " + ", ".join(DEFAULT_EXTENSIONS) + "."
    )

    # Exclusions
    ex_files: str = (
        "Filter out all files (or paths) containing any of the comma separated "
        "strings, e.g.: myfile, test"
    )
    ex_authors: str = (
        "Filter out all authors containing any of the comma separated strings, "
        "e.g.: John, Mary"
    )
    ex_emails: str = (
        "Filter out all authors containing any of the comma separated strings, "
        "e.g.: @gmail.com, john"
    )
    ex_revisions: str = (
        "Filter out all revisions containing any of the comma separated hash strings, "
        "e.g.: 8755fb33,12345678"
    )
    ex_messages: str = (
        "Filter out all revisions containing any of the comma separated commit message "
        "strings"
    )


# Help for CLI
@dataclass
class Help(Tip):
    # Is printed using the description attribute of the ArgumentParser at the start of
    # the help output.
    help_doc: tuple[str, str, str] = (
        "For online documentation see <",
        "https://gitinspectorgui.readthedocs.io",
        ">.",
    )

    # Mutually exclusive settings
    gui: str = """
        Start the GUI, taking all settings from the settings file and ignoring all
        other CLI arguments."""
    version: str = "Output version information."
    show: str = "Show the settings location and its values."
    save: str = "Save settings file."
    save_as: str = "Save settings file to PATH."
    load: str = "Load settings file from PATH."
    reset: str = "Reset saved settings to their default values."
    about: str = "Output license information."
    about_info: str = (
        f"GitinspectorGUI version {get_version()}, available under the MIT license. It uses "
        "the PyPI pysimplegui-4-foss LGPL licensed version of the PySimpleGUI project."
    )
    # Input
    input_fstrs: str = """
         Relative or absolute PATH(s) to repository, folders or URLs to be analysed."""
    depth: str = """
        Number of levels of subfolders of the input folder PATH that is searched for
        repositories (default 5).
        DEPTH=0: the input folder itself must be a repository.
        DEPTH=1: only the input folder itself is searched for repository folders."""

    # Output
    pre_postfix: str = """
        Specify whether or not to add the name of the repository as
        prefix or postfix to the output file name."""

    # IO arguments
    format: str = """
        Define in which format output should be generated (default auto: for single repo
        open webview but generate no output file,
        for multiple repos open browser on html files)."""

    # General configuration
    multi_core: str = "Execute multiple repositories using multiple cores."

    # Exclusions
    exclude_string: str = """Exclusion patterns describing the file paths, revisions,
revisions with certain commit messages, author names or author emails that should be
excluded from the statistics. Can be specified multiple times separated by a comma and
regular expressions may be used."""

    # Logging
    cli_verbosity: str = "More verbose output for each v, e.g. -vv."
    profile: str = "Add profiling output to the console."

    exclude: str = "\n".join(
        textwrap.wrap(
            exclude_string,
            initial_indent="    ",
            subsequent_indent="    ",
            width=70,
        )
    )

    def __post_init__(self):
        for fld in fields(Tip):
            if getattr(self, fld.name) == getattr(super(), fld.name):
                setattr(self, fld.name, getattr(self, fld.name) + ".")
