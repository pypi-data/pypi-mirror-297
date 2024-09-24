from pathlib import Path

from ml_logger.job import RUN, instr
from termcolor import colored

assert instr  # single-entry for the instrumentation thunk factory
RUN.project = "lucidsim"  # Specify the project name
RUN.job_name += "/{now:%H%M%S.%f}-{job_counter:03d}"

# RUN.prefix = "{project}/{project}/{username}/{now:%Y/%m-%d}/{file_stem}/{job_name}"
# RUN.prefix = "{project}/{project}/{username}/{file_stem}/{job_name}"

# WARNING: do NOT change these prefixes.
RUN.prefix = "{project}/{project}/lucidsim_experiments/{file_stem}/{job_name}"
RUN.script_root = Path(__file__).parent  # specify that this is the script root.

print(
    colored("set", "blue"),
    colored("RUN.script_root", "yellow"),
    colored("to", "blue"),
    RUN.script_root,
)
