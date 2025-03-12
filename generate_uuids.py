from decimal import *
from datetime import datetime, timezone

ORIGINAL_UUID = "131d3f99-8dc0-11ef-97ac-0242ac110019"
START_DT = "2024-10-19 02:12:28.9516670"
END_DT = "2024-10-19 02:12:28.9516690"

def getTimestamp(date_time):
        dt = datetime.strptime(date_time.split('.')[0], "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=timezone.utc)
        getcontext().prec = 28 # Ensure timestamp operations are precise
        timestamp = Decimal(dt.timestamp()) + Decimal("0." + date_time.split('.')[1])
        for i in range(10):
                ts = timestamp + Decimal("0.000000" + str(i))
        return timestamp

def editUUID(timestamp, uuid):
        getcontext().prec = 28 # Ensure timestamp operations are precise
        uuid_ts = (timestamp * 10**7) + 0x01B21DD213814000
        hex_string = format(int(uuid_ts), '#x').split("0x")[1]
        newUUID = hex_string[7:] + "-" + hex_string[3:][:4] + "-" + uuid.split("-")[2][0] + hex_string[:3] + "-" + uuid.split("-")[3] + "-" + uuid.split("-")[4]
        return newUUID

def getTimestamps(start_date, end_date):
        timestamps = []
        getcontext().prec = 7
        f = Decimal("0." + start_date.split(".")[1])
        while True:
                dt = start_date.split('.')[0] + "." + str(f).split(".")[1]
                timestamps.append(getTimestamp(dt))
                getcontext().prec = 7
                f = f + Decimal(0.0000001)
                if dt == end_date:
                        break
        return timestamps

if __name__ == "__main__":
        timestamps = getTimestamps(START_DT, END_DT)
        print("[i] Original UUID :", ORIGINAL_UUID)
        print("[+] New UUIDs :")
        for timestamp in timestamps:
                print(editUUID(timestamp, ORIGINAL_UUID))
