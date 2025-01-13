import csv
from collections import Counter

def parse_lookup_table(filepath):
     #Parse the lookup table CSV file
    lookup = {}
    with open(filepath, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            if len(row) == 3:
                dstport, protocol, tag = row
                lookup[(dstport.strip(), protocol.strip().lower())] = tag.strip()
    return lookup

def parse_flow_logs(log_filepath, lookup_table):
     #Parse flow logs and map them to tags using the lookup table
    tag_counts = Counter()
    port_protocol_counts = Counter()
    total_valid_logs = 0

    with open(log_filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 14 and parts[0] == '2':
                dstport = parts[5]
                protocol = 'tcp' if parts[7] == '6' else 'udp' if parts[7] == '17' else 'unknown'

                # Only process logs with valid protocols
                if protocol == 'unknown':
                    continue

                # Increment total valid logs
                total_valid_logs += 1

                # Count port/protocol combinations
                port_protocol_counts[(dstport, protocol)] += 1

                # Map to tags
                key = (dstport, protocol)
                if key in lookup_table:
                    tag = lookup_table[key]
                    tag_counts[tag] += 1

    # Calculate untagged count
    untagged_count = total_valid_logs - sum(tag_counts.values())

    # Filter port/protocol counts to include only valid combinations
    filtered_port_protocol_counts = {
        k: v for k, v in port_protocol_counts.items() if k in lookup_table
    }

    return tag_counts, filtered_port_protocol_counts, untagged_count

def write_tag_counts(filepath, tag_counts, untagged_count):
    #Write tag counts to a file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag", "Count"])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])
        writer.writerow(["Untagged", untagged_count])

def write_port_protocol_counts(filepath, port_protocol_counts):
     #Write port/protocol combination counts to a file
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Protocol", "Count"])
        for (port, protocol), count in sorted(port_protocol_counts.items()):
            writer.writerow([port, protocol, count])

def main():
    log_filepath = "flow_logs.txt"
    lookup_filepath = "lookup.csv"
    tag_output_filepath = "tag_counts.csv"
    port_protocol_output_filepath = "port_protocol_counts.csv"

    # Parse lookup table
    lookup_table = parse_lookup_table(lookup_filepath)

    # Parse flow logs
    tag_counts, port_protocol_counts, untagged_count = parse_flow_logs(log_filepath, lookup_table)


    write_tag_counts(tag_output_filepath, tag_counts, untagged_count)
    write_port_protocol_counts(port_protocol_output_filepath, port_protocol_counts)
    #Write the outputs in two different files named as tag_counts.csv and port_protocol_counts.csv
    
    print(f"Successfully executed! Output is displayed as Tag counts written to {tag_output_filepath} and Port/protocol combination counts written to {port_protocol_output_filepath}")

if __name__ == "__main__":
    main()

