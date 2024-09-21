
# Wuodan CLI

Wuodan is a command-line tool designed for efficiently searching through files and directories for strings or regular expressions. It is especially useful for **threat hunting** and **Digital Forensics and Incident Response (DFIR)**, where rapid analysis of logs, configuration files, or other data is critical.

[![Upload Python Package](https://github.com/izm1chael/wuodan/actions/workflows/python-publish.yml/badge.svg)](https://github.com/izm1chael/wuodan/actions/workflows/python-publish.yml)


## Features  

-  **Search files and directories**: Recursively search for a string or regex pattern within files in a directory. Ideal for locating key artefacts during incident response or threat investigations.

-  **Real-time progress bars**: Provides feedback on the progress of both file scanning and searching operations with `tqdm`. This is useful when searching through large log files or multiple directories for specific indicators of compromise (IOCs).

-  **Supports multiple threads**: Use multiple worker threads to speed up searching. This can greatly improve performance when scanning through massive datasets.

## Use Cases in Threat Hunting and DFIR

  
-  **Log Analysis**: Search for known IOCs such as IP addresses, hashes, or suspicious strings in large log files (e.g., web server logs, firewall logs, or SIEM exports).

-  **Malware Forensics**: Quickly scan directories and files for strings or patterns commonly associated with malware (e.g., suspicious URLs, encoded payloads).

-  **File Carving**: Search through file systems for specific file signatures or regex patterns to extract evidence.

-  **Post-Intrusion Investigation**: Hunt for specific patterns or indicators after a breach, such as known backdoor behaviours, malicious commands, or traces of lateral movement.

  

## Installation

  

### Prerequisites

  

- Python 3.6 or higher.

  

### Install Locally

  

To install Wuodan locally, navigate to the root of your project directory (where `setup.py` is located) and run:

  
    pip  install  .


## Usage

After installing, you can use the `wuodan` command in your terminal

#### Basic Command

    wuodan "search_string" /path/to/directory

This will search for the specified `search_string` in all files in the specified directory and its subdirectories.

### Options

-   `--use-regex`: Enable regular expression search instead of simple string matching. Useful for finding complex patterns such as encoded malware strings or specific file signatures.
-   `--max-workers`: Specify the number of worker threads to use for parallel searching (default is 5). Multiple threads can be used to speed up investigations, especially on large forensic dumps or log sets.
-   `--output-file`: Write the search results to a specified file instead of printing to the console. Handy for creating evidence reports.


## Example Commands

**Simple string search**:

    wuodan "error" /var/log

This will search for the string `"error"` in all files under `/var/log`. Ideal for locating suspicious log entries during a DFIR investigation.

**Using regular expressions for IOCs**:

    `wuodan "\d{4}-\d{2}-\d{2}" /path/to/logs --use-regex`
This will search for a date pattern (e.g., `YYYY-MM-DD`) using regex in all files under `/path/to/logs`. It can be useful for finding timestamps or other patterns across forensic data

**Saving results to a file**:

    wuodan "search_string" /path/to/search --output-file results.txt
This will search for `"search_string"` and save the results in `results.txt`.

**Using multiple worker threads**:

    wuodan "critical" /var/log --max-workers 10

This will search for the string `"critical"` using 10 worker threads for faster performance.


### Example Output

    System Information: 
    Number of Workers: 5 
    ========================================
    Scanning files: 45%|███████████ | 450/1000 [00:12<00:15, 35.00file/s] 
    Searching files: 40%|████████▉ | 400/1000 [00:14<00:18, 30.00file/s]


    Summary: 
    ======================================== 
    Total files scanned: 1000 
    Total matches found: 25 
    Number of Workers: 5 
    Total time taken: 35.72 seconds 
    ========================================

