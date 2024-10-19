from decimal import *
import time
import struct
from datetime import datetime, timezone

getcontext().prec=28

def getTimestamp(date_time):
        dt = datetime.strptime(date_time.split('.')[0], "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
        getcontext().prec = 28
        timestamp = Decimal(dt.timestamp()) + Decimal("0." + date_time.split('.')[1])
        for i in range(10):
                ts = timestamp + Decimal("0.000000" + str(i))
        return timestamp

def editUUID(timestamp, uuid):
        getcontext().prec = 28
        uuid_ts = (timestamp * 10**7) + 0x01B21DD213814000
        hex_string = format(int(uuid_ts), '#x').split("0x")[1]
        newUUID = hex_string[7:] + "-" + hex_string[3:][:4] + "-" + uuid.split("-")[2][0] + hex_string[:3] + "-" + uuid.split("-")[3] + "-" + uuid.split("-")[4]
        return newUUID

def getTimestamps(start_date, end_date):
        timestamps = []
        getcontext().prec = 7
        f = Decimal("0." + start_dt.split(".")[1])
        while True:
                dt = start_dt.split('.')[0] + "." + str(f).split(".")[1]
                timestamps.append(getTimestamp(dt))
                print(dt)
                getcontext().prec = 7
                f = f + Decimal(0.0000001)
                if dt == end_date:
                        break
        return timestamps

if __name__ == "__main__":
        start_dt = "2024-10-19 02:12:28.9516670"
        end_dt = "2024-10-19 02:12:28.9516690"
        timestamps = getTimestamps(start_dt, end_dt)
        original_uuid = "131d3f99-8dc0-11ef-97ac-0242ac110019"
        print("[i] Original UUID :", original_uuid)
        print("[+] New UUIDs :")
        for timestamp in timestamps:
                print(editUUID(timestamp, original_uuid))
