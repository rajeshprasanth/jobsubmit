| **Continuous Integration**   | <img alt="Gitlab pipeline status" src="https://img.shields.io/gitlab/pipeline/rajeshprasanth/jobsubmit/master">   | Downloads   | <img alt="GitHub All Releases" src="https://img.shields.io/github/downloads/rajeshprasanth/jobsubmit/total">   |
|-----|-----|-----|-----|
| **Pull Requests**   | <img alt="GitHub closed pull requests" src="https://img.shields.io/github/issues-pr-closed/rajeshprasanth/jobsubmit"><br><img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/rajeshprasanth/jobsubmit">   | **Issues**   | <img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/rajeshprasanth/jobsubmit"><br><img alt="GitHub issues" src="https://img.shields.io/github/issues/rajeshprasanth/jobsubmit">|
| **License**   | <img alt="GitHub" src="https://img.shields.io/github/license/rajeshprasanth/jobsubmit">  | **Repository**  |<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/rajeshprasanth/jobsubmit">|
| **Release**  | <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/rajeshprasanth/jobsubmit"><br><img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/rajeshprasanth/jobsubmit"> | **Commit History**  | <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/rajeshprasanth/jobsubmit"><br><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/rajeshprasanth/jobsubmit"><br><img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/rajeshprasanth/jobsubmit">|


# Jobsubmit

Jobsubmit is a lightweight, platform-independent job execution utility designed for scientific computing, batch processing, and reproducible workflows. It executes commands from a list file sequentially while clearly reporting job start time, completion status, execution duration, process ID, and exit code.

The design philosophy emphasizes simplicity, transparency, and deterministic behavior, making Jobsubmit suitable for local machines, login nodes, virtual machines, CI pipelines, and development environments.



## Key Features

- Sequential execution of commands from a file
- Clear reporting of:
  - Job start date & time
  - Job completion or failure date & time
  - Execution duration (HH:MM:SS)
  - Process ID (PID)
  - Exit code
- Separate capture of standard output and error
- Clean, scientific-style console output (no colors, no emojis)
- Cross-platform support (Linux, macOS, Windows)
- No external Python dependencies
- Simple installer and clean project layout



## Project Structure

```

jobsubmit/
├── bin
│   └── jobsubmit
├── docs
│   └── jobsubmit_manual.tex
├── logs
├── tests
│   └── cmd.lst
├── tools
│   └── install.sh
├── .gitlab-ci.yml
├── .travis.yml
├── CHANGELOG
├── LICENSE
└── README.md

````



## Requirements

- Python 3.7 or newer
- Bash shell (for installer on Linux/macOS)

No third-party Python modules are required.



## Installation

### Method 1: Interactive Installer (Linux / macOS)

From the project root directory:

```bash
bash tools/install.sh
````

The installer will:

* Ask for an installation directory
* Copy the Jobsubmit executable
* Make it executable
* Optionally add it to your `PATH`
* Create required output directories (`stdout`, `stderr`)

After installation, reload your shell:

```bash
source ~/.bashrc
```



### Method 2: Manual Installation

```bash
mkdir -p ~/jobsubmit
cp bin/jobsubmit ~/jobsubmit/
chmod +x ~/jobsubmit/jobsubmit
export PATH=$PATH:~/jobsubmit
```

Add the `export PATH` line to `~/.bashrc` or `~/.profile` for permanence.



### Windows Installation

Jobsubmit can be executed directly using Python:

```powershell
python bin\jobsubmit cmd.lst all
```

Executable (`.exe`) builds generated via Nuitka or PyInstaller may also be used if provided.



## Usage

```bash
jobsubmit <command_file> <line_selection>
```

### Examples

Run all commands:

```bash
jobsubmit cmd.lst all
```

Run a single job:

```bash
jobsubmit cmd.lst 3
```

Run a range of jobs:

```bash
jobsubmit cmd.lst 1-5
```

Run selected jobs:

```bash
jobsubmit cmd.lst 1,3,7
```



## Command File Format (`cmd.lst`)

* One command per line
* Blank lines are ignored
* Commands are executed sequentially

Example:

```
echo "Job 1"
sleep 2
invalid_command
echo "Job 4"
```



## Output Files

For each executed job:

* `stdout/<cmdfile>_line_<N>.out`
* `stderr/<cmdfile>_line_<N>.err`

These files allow post-run inspection and debugging.



## Exit Codes

* Exit code `0` → Command executed successfully
* Non-zero exit code → Command failed

Jobsubmit itself exits with a non-zero status only on fatal errors (e.g., invalid input file).



## Continuous Integration

This project includes configuration files for:

* GitLab CI (`.gitlab-ci.yml`)
* Travis CI (`.travis.yml`)

These ensure consistent behavior across platforms.



## License

Jobsubmit is distributed under the **GNU General Public License (GPL)**.

You are free to use, modify, and redistribute this software under the terms of the GPL.
See the `LICENSE` file for the full license text.



## Author

**Rajesh Prashanth Anandavadivel**

Originally developed as a practical utility for managing reproducible scientific and computational workflows.



## Changelog

All notable changes, version updates, and fixes are documented in the `CHANGELOG` file.



## Philosophy

Jobsubmit is intentionally:

* Minimal
* Predictable
* Transparent
* Script-friendly

It is not intended to replace full-fledged schedulers (e.g., SLURM, PBS), but to serve as a reliable execution tool for controlled, sequential workflows.



## Contributing

Bug reports, improvements, and suggestions are welcome.
Please keep contributions focused, readable, and consistent with the project’s scientific intent.
