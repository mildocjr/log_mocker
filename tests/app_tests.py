import os
from datetime import datetime

from log_mocker import app

FILENAME = "messages"
TARGET_1_MSG = "target.sh: 1 failed"
TARGET_2_MSG = "target.sh: 2 failed"
TARGET_3_MSG = "target.sh: 3 failed"


def test_log_creation_success():
    app.run(datetime.now())

    with open(FILENAME, "r") as f:
        line = f.readline()
        assert line is not None
        assert "main.py: Started processing" in line

        lines = f.readlines()

        assert lines[-1] is not None
        assert "main.py: Finished processing" in lines[-1]

    os.remove(FILENAME)


def test_success_message():
    with open(FILENAME, "w") as f:
        f.writelines(line for line in app.get_date(datetime(2020, 2, 22, 22, 22, 10)))

    with open(FILENAME, "r") as f:
        common_checks(f)

        line = f.readline()
        assert line is not None
        assert "target.sh: Hit Successful" in line

    os.remove(FILENAME)


def test_fail_target_1():
    with open(FILENAME, "w") as f:
        f.writelines(line for line in app.get_date(datetime(2020, 2, 22, 22, 22, 16)))

    with open(FILENAME, "r") as f:
        common_checks(f)

        line = f.readline()
        assert line is not None
        assert TARGET_1_MSG in line

    os.remove(FILENAME)


def test_fail_target_2():
    with open(FILENAME, "w") as f:
        f.writelines(line for line in app.get_date(datetime(2020, 2, 22, 22, 22, 17)))

    with open(FILENAME, "r") as f:
        common_checks(f)

        line = f.readline()
        assert line is not None
        assert TARGET_2_MSG in line

    os.remove(FILENAME)


def test_fail_target_3():
    with open(FILENAME, "w") as f:
        f.writelines(line for line in app.get_date(datetime(2020, 2, 22, 22, 22, 18)))

    with open(FILENAME, "r") as f:
        common_checks(f)

        line = f.readline()
        assert line is not None
        assert TARGET_3_MSG in line

    os.remove(FILENAME)


def test_partial_failure():
    with open(FILENAME, "w") as f:
        f.writelines(line for line in app.get_date(datetime(2020, 2, 22, 22, 22, 25)))

    with open(FILENAME, "r") as f:
        common_checks(f)

        line = f.readline()
        assert line is not None
        assert TARGET_1_MSG in line

        line = f.readline()
        assert line is not None
        assert TARGET_2_MSG in line

    os.remove(FILENAME)


def test_total_failure():
    with open(FILENAME, "w") as f:
        f.writelines(line for line in app.get_date(datetime(2020, 2, 22, 22, 22, 35)))

    with open(FILENAME, "r") as f:
        common_checks(f)

        line = f.readline()
        assert line is not None
        assert TARGET_1_MSG in line

        line = f.readline()
        assert line is not None
        assert TARGET_2_MSG in line

        line = f.readline()
        assert line is not None
        assert TARGET_3_MSG in line

    os.remove(FILENAME)


def test_default_message():
    with open(FILENAME, "w") as f:
        f.writelines(line for line in app.get_date(datetime(2020, 2, 22, 22, 22, 1)))

    with open(FILENAME, "r") as f:
        line = f.readline()
        assert line is not None
        assert "other.sh: doing other stuff" in line

    os.remove(FILENAME)


def common_checks(f):
    line = f.readline()
    assert line is not None
    assert "target.sh: Target script running" in line
    line = f.readline()
    assert line is not None
    assert "target.sh: Doing important stuff" in line
    line = f.readline()
    assert line is not None
    assert "target.sh: Doing other important stuff" in line
