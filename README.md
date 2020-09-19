<p align="center">
<img alt="Gitlab pipeline status" src="https://img.shields.io/gitlab/pipeline/rajeshprasanth/jobsubmit/master">

<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/rajeshprasanth/jobsubmit">

<img alt="GitHub All Releases" src="https://img.shields.io/github/downloads/rajeshprasanth/jobsubmit/total">

<img alt="GitHub closed pull requests" src="https://img.shields.io/github/issues-pr-closed/rajeshprasanth/jobsubmit">

<img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/rajeshprasanth/jobsubmit">

<img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/rajeshprasanth/jobsubmit">

<img alt="GitHub issues" src="https://img.shields.io/github/issues/rajeshprasanth/jobsubmit">

<img alt="GitHub" src="https://img.shields.io/github/license/rajeshprasanth/jobsubmit">

<img alt="GitHub release (latest by date)" src="https://img.shields.io/github/v/release/rajeshprasanth/jobsubmit">

<img alt="GitHub Release Date" src="https://img.shields.io/github/release-date/rajeshprasanth/jobsubmit">

<img alt="GitHub contributors" src="https://img.shields.io/github/contributors/rajeshprasanth/jobsubmit">

<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/rajeshprasanth/jobsubmit">

<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/rajeshprasanth/jobsubmit">

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="86" height="20" role="img" aria-label="Python: &gt;2.0"><title>Python: &gt;2.0</title><linearGradient id="s" x2="0" y2="100%"><stop offset="0" stop-color="#bbb" stop-opacity=".1"/><stop offset="1" stop-opacity=".1"/></linearGradient><clipPath id="r"><rect width="86" height="20" rx="3" fill="#fff"/></clipPath><g clip-path="url(#r)"><rect width="49" height="20" fill="#555"/><rect x="49" width="37" height="20" fill="#007ec6"/><rect width="86" height="20" fill="url(#s)"/></g><g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110"><text aria-hidden="true" x="255" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="390">Python</text><text x="255" y="140" transform="scale(.1)" fill="#fff" textLength="390">Python</text><text aria-hidden="true" x="665" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="270">&gt;2.0</text><text x="665" y="140" transform="scale(.1)" fill="#fff" textLength="270">&gt;2.0</text></g></svg>
</p>

# jobsubmit
jobsubmit is a python script designed for reading the list of command from a file and execute in particular order.

It is licensed under version 3.0 of the GNU General Public License. See LICENSE
for more information.

The jobsubmit is official hosted in github repository at https://github.com/rajeshprasanth/jobsubmit/ and mirrored by gitlab reposistory at https://gitlab.com/rajeshprasanth/jobsubmit/

## Table of contents
- [Dependency](#dependency)
- [Download](#download)
- [Installation](#installation)
- [Running of jobsubmit](#running)
- [Features](#features)

## Dependency
jobsubmit has been written in python. It is tested in python 3.6.8. However, any version of python 3.x will support.

## Download
jobsubmit can be downloaded in two ways:

### Method:1
The stable version of jobsubmit can be directly downloaded as an archive file from below address.

### Method:2
Alternatively, developmental version can be download from this repository following below steps:

#### From github
Run below command to download from github repository
```
git clone https://github.com/rajeshprasanth/jobsubmit.git
cd jobsubmit
./jobsubmit
```
#### From gitlab
Run below command to download from github repository
```
git clone https://gitlab.com/rajeshprasanth/jobsubmit.git
cd jobsubmit
./jobsubmit
```

## Installation

For Bash shell system, add these lines in ~/.bashrc or ~/.profile or /etc/profile:
```
     export PATH=/{jobsubmit_path}:$PATH
```
For C shell system, add these lines in ~/.cshrc or ~/.profile or /etc/profile:
```
     setenv PATH "/{jobsubmit_path} :$PATH"
```

Once added please do restart your login shell for the installation to take effect immediately.


## Running of jobsubmit

If jobsubmit is setup added to $PATH variable, then invoking jobsubmit anywhere in the file system should work.

Running jobsubmit without arguments will display help message as below.
```
Usage: jobsubmit [options] [args]

option:
   -h|--help            Display this information
   -v|--version         Display the version of script.
   -c|--cleanup         Cleanup stdout and stderr directories in current directory(if any)
  -fc|--fullcleanup     Cleanup stdout,stderr directories and logfile in current directory(if any)

args:
  <file> all            Run all the lines from the <file>
  <file> 1              Run 1st line from the <file>
  <file> 1,2,3          Run 1,2 and 3rd lines from the <file>
  <file> 1-5            Run 1 to 5th lines from the <file>

For bug reporting please reach out <rajeshprasanth@rediffmail.com>

```
