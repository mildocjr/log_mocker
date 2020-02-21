import os
from datetime import timedelta
from random import randrange

# String format for logging
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Log file name
FILENAME = "messages"

# Default is append; if the file does not exist, write a new file
write_mode = "a"
if not os.path.exists(FILENAME):
    write_mode = "w"


def get_date(write_time):
    # Common Target Messages
    time_str = write_time.strftime(DATE_FORMAT)
    target_string = (
        time_str
        + " target.sh: Target script running\n"
        + time_str
        + " target.sh: Doing important stuff\n"
        + time_str
        + " target.sh: Doing other important stuff\n"
    )

    # Target Success Message
    target_success = time_str + " target.sh: Hit Successful\n"

    # Target Error Messages
    target_1 = time_str + " target.sh: 1 failed\n"
    target_2 = time_str + " target.sh: 2 failed\n"
    target_3 = time_str + " target.sh: 3 failed\n"

    # Default message
    default_message = time_str + " other.sh: doing other stuff\n"

    # Get the current write time seconds
    write_time_seconds = int(time_str[-2:])

    # Target ran successfully
    if write_time_seconds % 10 == 0:
        yield target_string + target_success

    # Target 1 failed
    elif write_time_seconds % 16 == 0:
        yield target_string + target_1

    # Target 2 failed
    elif write_time_seconds % 17 == 0:
        yield target_string + target_2

    # Target 3 failed
    elif write_time_seconds % 18 == 0:
        yield target_string + target_3

    # Partial target failure
    elif write_time_seconds % 25 == 0:
        yield target_string + target_1 + target_2

    # Total target failure
    elif write_time_seconds % 35 == 0:
        yield target_string + target_1 + target_2 + target_3

    # Something else is running
    else:
        yield default_message


def run(current_time):
    # Open our file and write logs
    with open(FILENAME, write_mode) as f:
        f.write(current_time.strftime(DATE_FORMAT) + " main.py: Started processing\n")

        # 15k iterations is more than enough to hit all test cases
        for _ in range(150000):
            f.writelines(line for line in get_date(current_time))
            current_time += timedelta(seconds=randrange(10))

        f.write(current_time.strftime(DATE_FORMAT) + " main.py: Finished processing\n")
