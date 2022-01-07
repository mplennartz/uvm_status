"""Placeholder doc string for imports"""
# from python_objects.uvm_status_util.uvm_status_parser import BaseParser
import json
import random
from argparse import Namespace
from pathlib import Path

from python_objects.uvm_status_util.uvm_status_parser import BaseParser
from python_objects.uvm_status_util.uvm_status_test_objects import UvmTest, UvmTestlist


def randomly_generate_test(proj_dir: str) -> UvmTest:
    """Testing method"""

    list_of_test_types = ["Alu", "AmrrRand", "OciRand", "MultiRevRand", "OOWRand"]
    list_of_test_stats = ["not_run", "Running", "Passed", "Failed", "Killed"]

    test_type = list_of_test_types[random.randrange(0, 5, 1)]

    test_seed = str(random.randrange(9999, 99999999))

    new_test = UvmTest(test_type, test_seed, proj_dir)

    test_status = list_of_test_stats[random.randrange(0, 5, 1)]

    test_war = random.randrange(0, 100)
    temp1 = random.randrange(-10000, 1000)

    if test_status == "not_run":
        test_war = 0
        test_err = 0

    elif test_status == "Running":
        if temp1 > 0:
            test_err = temp1
        else:
            test_err = 0

    elif test_status in ["Passed", "Killed"]:
        test_err = 0

    else:
        test_err = abs(temp1 % 1000) + 1

    new_test.update(errors=test_err, warnings=test_war, status=test_status)

    return new_test


def main(command_line_args: Namespace):
    """Placeholder doc string for uvm_new_status main method"""

    proj_dir = command_line_args.directory

    testlist_1 = UvmTestlist.create_object(
        testlist_name="uvm_rand_list", proj_path=proj_dir
    )

    if command_line_args.number > 0:

        for ii in range(  # pylint: disable=unused-variable disable=invalid-name
            command_line_args.number
        ):
            testlist_1.add_test(randomly_generate_test(proj_dir))

    if command_line_args.input_file is not None:
        with open(Path(command_line_args.input_file), "r", encoding="utf8") as in_log:
            tl_input_report = json.load(in_log)

        for (
            test,  # pylint: disable=unused-variable
            test_obj,
        ) in tl_input_report.items():
            new_test = UvmTest(test_obj["test"], test_obj["seed"], proj_dir)
            new_test.update(
                errors=test_obj["errors"],
                warnings=test_obj["warnings"],
                status=test_obj["status"],
            )
            testlist_1.add_test(new_test)

    tl1_report = testlist_1.report()

    if command_line_args.output_file is not None:
        with open(Path(command_line_args.output_file), "w", encoding="utf8") as out_log:
            json.dump(tl1_report, out_log)

    testlist_1.print_not_run()
    testlist_1.print_running()
    testlist_1.print_failures()
    # testlist_1.print_all()


if __name__ == "__main__":

    parser = BaseParser()

    args = parser.parse_args()

    print(args)

    # TODO instead of passing args, parse the args and pass TestObject # pylint:disable=fixme
    main(args)
