# Flow Log Parser – README

## Description
The **Flow Log Parser** processes AWS VPC flow logs and maps them to tags based on a lookup table. It generates two output files:
1. **Tag Counts**: Counts of logs mapped to each tag.
2. **Port/Protocol Combination Counts**: Counts of each port/protocol combination.


## How to Run

### Requirements
- **Python 3.x** installed on your system.

### Running the Program
1. **Place your input files**  
   Make sure the input files namely `flow_logs.txt` and `lookup.csv` are in the same directory as the script.

2. **Update the file paths**  
   Modify the paths in the `main()` function of `flow_log_parser.py`:
   - `log_filepath`: Path to the flow logs file.
   - `lookup_filepath`: Path to the lookup table file.
   - `tag_output_filepath`: Output file for tag counts.
   - `port_protocol_output_filepath`: Output file for port/protocol counts.

3. **Run the script**  
   To run the script, use this command in your terminal:
   ```bash
   python3 flow_log_parser.py
   
4. **Running Tests**  
   To run the test script and verify that everything works correctly, use this command:
   ```bash
   python3 -m unittest test_flow_log_parser.py
   
###  Check the output files
Verify the output files that are generated:
   - `tag_counts.csv`
   - `port_protocol_counts.csv`


### 

## Assumptions
1. The program only supports AWS VPC flow log format (version 2). 
2. Input files must be plain text (CSV or space-separated logs).
3. The lookup table must have all three columns (dstport, protocol, tag) correctly formatted.
4. Entries in the lookup table are case-insensitive for protocol names (e.g., tcp and TCP are treated the same).
5. Logs with unsupported protocols or non-numeric ports are considered untagged.
6. The script requires write permissions for the output directory.
7. The program overwrites existing output files with the same name.
 
## Test Cases and Descriptions
1.	test_empty_flow_logs: Verifies when the flow logs file is empty.
2.	test_invalid_flow_log_format: Verifies handling of invalid or incorrectly formatted flow log entries.
3.	test_empty_lookup_table: Checks all logs are marked as untagged when the lookup table is empty.
4.	test_non_numeric_ports: Checks how logs with non-numeric destination ports are processed (should be untagged).
5.	test_corrupted_lookup_file: Tests  when the lookup table contains non-CSV or invalid content.
6.	test_empty_file_paths: Validates that empty file paths raise appropriate errors.
7.	test_invalid_output_file_path: Verifies that the program raises an error when the output file path is invalid or unwritable.
8.	test_missing_lookup_file: Ensures a FileNotFoundError is raised when the lookup file is missing.

