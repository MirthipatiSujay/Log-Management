from collections import deque,defaultdict
logs = [
    "[2025-06-16T10:00:00] INFO user1: Started process",
    "[2025-06-16T10:00:01] ERROR user1: Failed to connect",
    "[2025-06-16T10:00:02] INFO user2: Login successful",
    "[2025-06-16T10:00:03] WARN user3: Low memory",
    "[2025-06-16T10:00:04] ERROR user2: Timeout occurred",
    "[2025-06-16T10:00:05] INFO user1: Retrying connection"
]
userdict = defaultdict(list)
leveldict = defaultdict(int)
recentlogs = deque(maxlen=3)


def parse_log(add_log):
    def wrapper(line):
        parts = line.split()
        user = parts[2][:-1]
        level = parts[1]
        userdict[user].append(line)
        leveldict[level] += 1
        recentlogs.append(line)
        result =  add_log(line)
        print("Converted from string to dict")
        return result
    return wrapper

@parse_log
def add_log(line: str) -> None:
    pass

def get_user_logs(user_id: str) -> list[dict]:
    logs = userdict.get(user_id, [])
    result = []
    for line in logs:
        parts = line.split()
        timestamp = parts[0][1:]
        timestamp = timestamp + " " + parts[0][11:-1] if len(parts[0]) > 20 else timestamp
        level = parts[1]
        user = parts[2][:-1]
        message = " ".join(parts[3:])
        result.append({
            "timestamp": line[1:20],
            "level": level,
            "user": user,
            "message": message
        })
    return result

def count_levels() -> dict[str, int]:
    return dict(leveldict)

def filter_logs(keyword: str) -> list[dict]:
    keyword = keyword.lower()
    all_logs = sum(userdict.values(), [])
    result = []
    for line in all_logs:
        if keyword in line.lower():
            parts = line.split()
            result.append({
                "timestamp": line[1:20],
                "level": parts[1],
                "user": parts[2][:-1],
                "message": " ".join(parts[3:])
            })
    return result

def get_recent_logs() -> list[dict]:
    result = []
    for line in recentlogs:
        parts = line.split()
        result.append({
            "timestamp": line[1:20],
            "level": parts[1],
            "user": parts[2][:-1],
            "message": " ".join(parts[3:])
        })
    return result

for log in logs:
    add_log(log)

print("User Logs (user1):")
print(get_user_logs("user1"))

print("\nLevel Counts:")
print(count_levels())

print("\nFiltered Logs (connect):")
print(filter_logs("connect"))

print("\nRecent Logs:")
print(get_recent_logs())
