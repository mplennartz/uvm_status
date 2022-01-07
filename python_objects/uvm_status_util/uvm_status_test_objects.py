"""Placehold doc string"""
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict

#!remove since module not avail in base CentOS7
# from dataclasses import dataclass, field


# class definition used from forum thread here:
# https://stackoverflow.com/questions/11217878/python-2-7-combine-abc-abstractmethod-and-classmethod
class AbstractClassMethod(classmethod):  # pylint: disable=too-few-public-methods
    """Class to allow a decorator to be abstract and class method"""

    __isabstractmethod__ = True

    def __init__(self, local_callable) -> None:
        local_callable.__isabstractmethod__ = True
        super(AbstractClassMethod, self).__init__(callable)


class UVMTestObject(ABC):
    """TBA"""

    @AbstractClassMethod
    def create_object(cls, **kwargs):
        """TBA"""

    @abstractmethod
    def parse(self) -> None:
        """TBA"""

    @abstractmethod
    def report(self) -> Dict:
        """TBA"""


# @dataclass
class UvmTest(
    UVMTestObject
):  # pylint: disable=missing-class-docstring disable=too-many-instance-attributes

    test_name: str
    test_seed: str
    proj_path: str
    test_uref: str
    test_path: Path
    num_errs: int = 0
    num_warns: int = 0
    curr_cmd: int = -1
    max_cmd: int = -1
    status: str = "not_run"

    uref_s_len: int = 45
    errs_s_len: int = 7
    warn_s_len: int = 8
    stat_s_len: int = 8

    def __init__(self, test_name, test_seed, proj_path) -> None:
        self.test_name = test_name
        self.test_seed = test_seed
        self.proj_path = proj_path
        self.test_uref = f"{self.test_name}_{self.test_seed}"
        self.test_path = Path(
            f"{self.proj_path}\\run\\tests\\{self.test_name}\\{self.test_uref}.log"
        )

    def __str__(self) -> str:
        return json.dumps(self.report())

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def create_object(cls, **kwargs) -> "UvmTest":
        return cls(kwargs["test_name"], kwargs["test_seed"], kwargs["proj_path"])

    def parse(self) -> None:
        pass

    @staticmethod
    def print_fail_header():  # pylint: disable=missing-function-docstring
        print(
            f"+{'-' * (UvmTest.uref_s_len+2)}"
            f"+{'-' * (UvmTest.errs_s_len+2)}"
            f"+{'-' * (UvmTest.warn_s_len+2)}"
            f"+{'-' * (UvmTest.stat_s_len+2)}+"
        )
        print(
            f"| {'Test':<{UvmTest.uref_s_len}} "
            f"| {'Errors':^{UvmTest.errs_s_len}} "
            f"| {'Warnings':^{UvmTest.warn_s_len}} "
            f"| {'Status':^{UvmTest.stat_s_len}} |"
        )
        print(
            f"+{'-' * (UvmTest.uref_s_len+2)}"
            f"+{'-' * (UvmTest.errs_s_len+2)}"
            f"+{'-' * (UvmTest.warn_s_len+2)}"
            f"+{'-' * (UvmTest.stat_s_len+2)}+"
        )

    @staticmethod
    def print_run_header():  # pylint: disable=missing-function-docstring
        print(
            f"+{'-' * (UvmTest.uref_s_len+2)}"
            f"+{'-' * (UvmTest.errs_s_len+2)}"
            f"+{'-' * (UvmTest.warn_s_len+2)}+"
        )
        print(
            f"| {'Test':<{UvmTest.uref_s_len}} "
            f"| {'Errors':<{UvmTest.errs_s_len}} "
            f"| {'Warnings':<{UvmTest.warn_s_len}} |"
        )
        print(
            f"+{'-' * (UvmTest.uref_s_len+2)}"
            f"+{'-' * (UvmTest.errs_s_len+2)}"
            f"+{'-' * (UvmTest.warn_s_len+2)}+"
        )

    @staticmethod
    def print_fail_footer():  # pylint: disable=missing-function-docstring
        print(
            f"+{'-' * (UvmTest.uref_s_len+2)}"
            f"+{'-' * (UvmTest.errs_s_len+2)}"
            f"+{'-' * (UvmTest.warn_s_len+2)}"
            f"+{'-' * (UvmTest.stat_s_len+2)}+"
        )

    @staticmethod
    def print_run_footer():  # pylint: disable=missing-function-docstring
        print(
            f"+{'-' * (UvmTest.uref_s_len+2)}"
            f"+{'-' * (UvmTest.errs_s_len+2)}"
            f"+{'-' * (UvmTest.warn_s_len+2)}+"
        )

    def print_fail_test(self):  # pylint: disable=missing-function-docstring
        print(
            f"| {self.test_uref:<{UvmTest.uref_s_len}} "
            f"| {self.num_errs:>{UvmTest.errs_s_len}} "
            f"| {self.num_warns:>{UvmTest.warn_s_len}} "
            f"| {self.status:^{UvmTest.stat_s_len}} |"
        )

    def print_run_test(self):  # pylint: disable=missing-function-docstring
        print(
            f"| {self.test_uref:<{UvmTest.uref_s_len}} "
            f"| {self.num_errs:>{UvmTest.errs_s_len}} "
            f"| {self.num_warns:>{UvmTest.warn_s_len}} |"
        )

    def report(self) -> Dict:
        return {
            "test": self.test_name,
            "seed": self.test_seed,
            "errors": self.num_errs,
            "warnings": self.num_warns,
            "status": self.status,
        }

    def update(self, **kwargs) -> None:
        """TBA"""
        n_errors = kwargs.pop("errors", 0)
        n_warnings = kwargs.pop("warnings", 0)
        p_status = kwargs.pop("status", "non_run")

        self.num_warns = n_warnings
        self.num_errs = n_errors
        self.status = p_status


# @dataclass
class UvmTestlist(UVMTestObject):  # pylint: disable=missing-class-docstring

    testlist_name: str
    proj_path: str
    testlist_path: Path
    test_dict: Dict

    def __init__(self, testlist_name, proj_path) -> None:
        self.testlist_name = testlist_name
        self.proj_path = proj_path
        self.testlist_path = Path(
            f"{self.proj_path}\\sim\\tests\\for_status_{self.testlist_name}"
        )
        self.test_dict = {}

    def __str__(self) -> str:
        return json.dumps(self.report())

    @classmethod
    def create_object(cls, **kwargs) -> "UvmTestlist":
        return cls(kwargs["testlist_name"], kwargs["proj_path"])

    def add_test(self, test: UvmTest) -> None:
        """TBA"""
        self.test_dict[test.test_uref] = test

    def parse(self) -> None:
        pass

    def print_all(self) -> None:  # pylint: disable=missing-function-docstring
        UvmTest.print_fail_header()

        for (
            test_uref,  # pylint: disable=unused-variable
            test_obj,
        ) in sorted(self.test_dict.items()):
            test_obj.print_fail_test()
        UvmTest.print_fail_footer()

    def print_failures(self) -> None:
        '''Print to console all tests with current status of "Failed" or "Killed"'''
        UvmTest.print_fail_header()
        for (
            test_uref,  # pylint: disable=unused-variable
            test_obj,
        ) in sorted(self.test_dict.items()):
            if (test_obj.status == "Failed") or (test_obj.status == "Killed"):
                test_obj.print_fail_test()
        UvmTest.print_fail_footer()

    def print_not_run(self) -> None:
        '''Print to console all tests with current status of "Running"'''
        UvmTest.print_run_header()
        for (
            test_uref,  # pylint: disable=unused-variable
            test_obj,
        ) in sorted(self.test_dict.items()):
            if test_obj.status == "not_run":
                test_obj.print_run_test()
        UvmTest.print_run_footer()

    def print_running(self) -> None:
        '''Print to console all tests with current status of "Running"'''
        UvmTest.print_run_header()
        for (
            test_uref,  # pylint: disable=unused-variable
            test_obj,
        ) in sorted(self.test_dict.items()):
            if test_obj.status == "Running":
                test_obj.print_run_test()
        UvmTest.print_run_footer()

    def report(self) -> Dict:
        return {
            test_uref: test_obj.report()
            for test_uref, test_obj in self.test_dict.items()
        }

    def report_failures(self) -> Dict:  # pylint: disable=missing-function-docstring
        return {
            test_uref: test_obj.report()
            for test_uref, test_obj in self.test_dict.items()
            if ((test_obj.status == "Failed") or (test_obj.status == "Killed"))
        }

    def report_running(self) -> Dict:  # pylint: disable=missing-function-docstring
        return {
            test_uref: test_obj.report()
            for test_uref, test_obj in self.test_dict.items()
            if test_obj.status == "Running"
        }
