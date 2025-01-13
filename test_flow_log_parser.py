import unittest
import os
from collections import Counter
from flow_log_parser import parse_lookup_table, parse_flow_logs, write_tag_counts, write_port_protocol_counts


class TestFlowLogParserBasic(unittest.TestCase):
    # Basic tests for flow log parser functionality

    def setUp(self):
        # Set up temporary input files for testing
        self.lookup_filepath = "test_lookup.csv"
        self.log_filepath = "test_flow_logs.txt"
        self.tag_output_filepath = "test_tag_counts.csv"
        self.port_protocol_output_filepath = "test_port_protocol_counts.csv"

    def tearDown(self):
        # Clean up temporary files
        for filepath in [self.lookup_filepath, self.log_filepath, self.tag_output_filepath, self.port_protocol_output_filepath]:
            if os.path.exists(filepath):
                os.remove(filepath)

    def write_file(self, filepath, content):
        # Utility to write content to a file
        with open(filepath, 'w') as file:
            file.write(content)

    def test_empty_flow_logs(self):
        # Test empty flow logs
        self.write_file(self.lookup_filepath, "dstport,protocol,tag\n")  # Empty lookup table
        self.write_file(self.log_filepath, "")  # Empty flow logs
        lookup = parse_lookup_table(self.lookup_filepath)
        tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(self.log_filepath, lookup)
        self.assertEqual(tag_counts, Counter())
        self.assertEqual(untagged_count, 0)

    def test_invalid_flow_log_format(self):
        # Test invalid flow log format
        self.write_file(self.lookup_filepath, "dstport,protocol,tag\n")  # Empty lookup table
        self.write_file(self.log_filepath, "2 123 eni 10.0.1.1\nINVALID_LOG_ENTRY\n")
        lookup = parse_lookup_table(self.lookup_filepath)
        tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(self.log_filepath, lookup)
        self.assertEqual(tag_counts, Counter())
        self.assertEqual(untagged_count, 0)

    def test_empty_lookup_table(self):
        # Test behavior with an empty lookup table
        self.write_file(self.lookup_filepath, "dstport,protocol,tag\n")  # Empty lookup table
        self.write_file(self.log_filepath, 
            "2 123 eni 10.0.1.1 1.1.1.1 25 1 6 25 1 1 1 ACCEPT OK\n"
            "2 123 eni 10.0.1.1 1.1.1.1 443 1 6 25 1 1 1 ACCEPT OK\n")
        lookup = parse_lookup_table(self.lookup_filepath)
        tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(self.log_filepath, lookup)
        self.assertEqual(tag_counts, Counter())
        self.assertEqual(untagged_count, 2)


class TestFlowLogParserErrorHandling(unittest.TestCase):
    # Error handling tests for flow log parser

    def setUp(self):
        # Set up temporary input files for testing
        self.lookup_filepath = "test_lookup.csv"
        self.log_filepath = "test_flow_logs.txt"
        self.tag_output_filepath = "test_tag_counts.csv"
        self.port_protocol_output_filepath = "test_port_protocol_counts.csv"

    def tearDown(self):
        # Clean up temporary files
        for filepath in [self.lookup_filepath, self.log_filepath, self.tag_output_filepath, self.port_protocol_output_filepath]:
            if os.path.exists(filepath):
                os.remove(filepath)

    def write_file(self, filepath, content):
        with open(filepath, 'w') as file:
            file.write(content)

    def test_non_numeric_ports(self):
        # Test logs with non-numeric ports
        self.write_file(self.lookup_filepath, "dstport,protocol,tag\n25,tcp,sv_P1\n")
        self.write_file(self.log_filepath, "2 123 eni 10.0.1.1 1.1.1.1 abc 1 6 25 1 1 1 ACCEPT OK\n")
        lookup = parse_lookup_table(self.lookup_filepath)
        tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(self.log_filepath, lookup)
        self.assertEqual(tag_counts, Counter())  # No tags should match
        self.assertEqual(untagged_count, 1)

    def test_corrupted_lookup_file(self):
        # Test behavior with a corrupted lookup file
        self.write_file(self.lookup_filepath, "This is not a CSV file!")
        lookup = parse_lookup_table(self.lookup_filepath)  # Should not raise errors
        self.assertEqual(lookup, {})

    def test_empty_file_paths(self):
        # Test behavior when file paths are empty strings
        with self.assertRaises(FileNotFoundError):
            parse_lookup_table("")  # Expect FileNotFoundError

    def test_invalid_output_file_path(self):
        # Test behavior when the output file path is invalid
        self.write_file(self.lookup_filepath, "dstport,protocol,tag\n25,tcp,sv_P1\n")
        self.write_file(self.log_filepath, "2 123 eni 10.0.1.1 1.1.1.1 25 1 6 25 1 1 1 ACCEPT OK\n")
        lookup = parse_lookup_table(self.lookup_filepath)
        tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(self.log_filepath, lookup)

        # Use an invalid directory path for the output files
        invalid_path = "/invalid/path/test_tag_counts.csv"
        with self.assertRaises(OSError):
            write_tag_counts(invalid_path, tag_counts, untagged_count)

    def test_missing_lookup_file(self):
        # Test behavior when the lookup file is missing
        if os.path.exists(self.lookup_filepath):
            os.remove(self.lookup_filepath)  # Ensure the lookup file is not present
        with self.assertRaises(FileNotFoundError):
            parse_lookup_table(self.lookup_filepath)  # This should raise a FileNotFoundError


if __name__ == "__main__":
    unittest.main()
