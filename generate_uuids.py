from decimal import *
import argparse
from datetime import datetime, timezone

getcontext().prec = 28 # Ensure timestamp operations are precise

def getTimestamp(date_time):
        date_part, fractional_part = date_time.split('.')
        fractional_part = (fractional_part + "0000000")[:7]
        dt = datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
        timestamp = Decimal(dt.timestamp()) + Decimal("0." + fractional_part)
        return timestamp.quantize(Decimal("0.0000001"), rounding=ROUND_DOWN)

def editUUID(timestamp, uuid):
        uuid_ts = (timestamp * 10**7) + 0x01B21DD213814000
        hex_string = format(int(uuid_ts), '#x').split("0x")[1]
        newUUID = hex_string[7:] + "-" + hex_string[3:][:4] + "-" + uuid.split("-")[2][0] + hex_string[:3] + "-" + uuid.split("-")[3] + "-" + uuid.split("-")[4]
        return newUUID

def getTimestamps(start_date, end_date):
        start_ts = getTimestamp(start_date)
        end_ts = getTimestamp(end_date)

        if start_ts >= end_ts:
                print("[-] Error, start_date should be stricly inferior to end_date")
                exit()

        timestamps = []
        ts = start_ts
        while ts != end_ts:
                timestamps.append(ts)
                ts = ts + Decimal("0.0000001")
        return timestamps

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("uuid", help="The original UUID used as base to generate other UUIDs", type=str)
        parser.add_argument("start_date", help="Start date for UUIDs generation (Format: YYYY-MM-DD HH:MM:SS.ffffffd)", type=str)
        parser.add_argument("end_date", help="End date for UUIDs generation (Format: YYYY-MM-DD HH:MM:SS.ffffffd)", type=str)
        parser.add_argument("--output", help="Path to the output file", type=str)
        args = parser.parse_args()

        timestamps = getTimestamps(args.start_date, args.end_date)
        print("[i] Original UUID :", args.uuid)
        print("[+] New UUIDs :")
        uuids = ""
        for timestamp in timestamps:
                uuid = editUUID(timestamp, args.uuid)
                uuids += uuid + "\n"
                print(" - ", uuid)
        if args.output:
                with open(args.output, "w") as file:
                        file.write(uuids)
                        print("[i] UUIDs saved to", args.output)
