import time

# dummies
feedings = []
walks = []


def current_time():
    return time.strftime('%a %d.%m.%Y %H:%M:%S %z')


def add_feeding(by_whom, time_at=None):
    time_at = time_at or current_time()
    db_record = {
        "by_whom": by_whom,
        "time_at": time_at
    }

    global feedings
    feedings.append(db_record)


def add_walk(by_whom, time_at=None):
    time_at = time_at or current_time()
    db_record = {
        "by_whom": by_whom,
        "time_at": time_at
    }

    global walks
    walks.append(db_record)


async def get_all_feedings():
    response_lines = []
    global feedings
    for feeding in feedings:
        line = f"Когда: {feeding['time_at']}\nКто: @{feeding['by_whom']}"
        response_lines.append(line)

    return '\n\n'.join(response_lines)


async def get_all_walks():
    response_lines = []
    global walks
    for walk in walks:
        line = f"Когда: {walk['time_at']}\nКто: @{walk['by_whom']}"
        response_lines.append(line)

    return '\n\n'.join(response_lines)
