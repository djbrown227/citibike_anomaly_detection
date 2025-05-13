import pandas as pd
import re
import sys

def parse_log_file(filepath, output_csv="data/parsed_station_data.csv"):
    """
    Parses a structured log file and returns a DataFrame with station stats.
    Assumes each record is delimited by dashed lines.
    """
    data = []
    with open(filepath, 'r') as file:
        content = file.read()

    # Split into blocks by dashed lines
    blocks = content.split('------------------------')
    print(f"Found {len(blocks)} blocks in the log file.")

    for block in blocks:
        lines = block.strip().splitlines()
        if not lines or 'Timestamp:' not in block:
            continue  # skip irrelevant blocks

        record = {}
        for line in lines:
            if 'Timestamp:' in line:
                record['timestamp'] = pd.to_datetime(line.split('Timestamp:')[1].strip())
            elif 'Station:' in line:
                match = re.match(r"Station: (.*) \(ID: ([^)]+)\)", line)
                if match:
                    record['station_name'] = match.group(1).strip()
                    record['station_id'] = match.group(2).strip()
            elif 'Longitude:' in line:
                record['longitude'] = float(line.split('Longitude:')[1].strip())
            elif 'Latitude:' in line:
                record['latitude'] = float(line.split('Latitude:')[1].strip())
            elif 'Capacity:' in line:
                record['capacity'] = int(line.split('Capacity:')[1].strip())
            elif 'Bikes Available:' in line:
                record['bikes_available'] = int(line.split('Bikes Available:')[1].strip())
            elif '% Filled:' in line:
                record['percent_filled'] = float(line.split('% Filled:')[1].strip().replace('%', ''))
            elif '% Empty:' in line:
                record['percent_empty'] = float(line.split('% Empty:')[1].strip().replace('%', ''))

        if record:
            data.append(record)

    if data:
        print(f"Parsed {len(data)} records.")
    else:
        print("No records were parsed from the file.")
        
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"✅ Parsed data saved to {output_csv}")

    return df

if __name__ == "__main__":
    input_file = "data/station_data_1.log"
    output_file = "data/parsed_station_data.csv"

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    parse_log_file(input_file, output_file)
