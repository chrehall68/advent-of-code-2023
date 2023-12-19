from typing import List, Callable, Union
import re
from collections import OrderedDict


class Checker:
    def __init__(self, condition: str) -> None:
        self.num = int(condition[2 : condition.index(":")])
        self.dest = condition[condition.index(":") + 1 :]
        self.comparable = condition[0]
        self.operation = condition[1]

    def __call__(self, ip: dict) -> str:
        if self.operation == "<":
            ret = ip[self.comparable] < self.num
        elif self.operation == ">":
            ret = ip[self.comparable] > self.num

        if ret:
            return self.dest
        return ""

    def __repr__(self) -> str:
        return f"{self.comparable}{self.operation}{self.num}:{self.dest}"

    def __str__(self) -> str:
        return self.__repr__()

    def opposite(self):
        ret = Checker(str(self))
        if self.operation == "<":
            ret.operation = ">"
        else:
            ret.operation = "<"
        return ret


class Workflow:
    def __init__(self, line: str):
        condition_start = line.index("{")
        self.name = line[:condition_start]
        self.conditions: List[Union[Callable[[dict], str], Checker]] = []
        self.destinations: List[str] = []

        for condition in line[condition_start + 1 : -1].split(","):
            if ":" not in condition:
                self.conditions.append(lambda d: condition)
                self.destinations.append(condition)
            else:
                temp = Checker(condition)
                self.conditions.append(temp)
                self.destinations.append(temp.dest)

    def get_next_destination(self, ip: dict) -> str:
        for condition in self.conditions:
            ret = condition(ip)
            if ret != "":
                return ret
        raise Exception("Something went wrong!!")


def parse_lines(lines: List[str]):
    workflow_end = lines.index("")
    workflows = list(map(Workflow, lines[:workflow_end]))
    inputs = lines[workflow_end + 1 :]

    inputs = list(
        map(
            lambda line: {
                "x": int(re.findall("x=([0-9]*),", line)[0]),
                "m": int(re.findall("m=([0-9]*),", line)[0]),
                "a": int(re.findall("a=([0-9]*),", line)[0]),
                "s": int(re.findall("s=([0-9]*)}", line)[0]),
            },
            inputs,
        ),
    )
    workflows = {workflow.name: workflow for workflow in workflows}
    return workflows, inputs


def part1(lines: List[str]) -> int:
    workflows, inputs = parse_lines(lines)
    accepted_sum = 0
    for ip in inputs:
        workflow_name = "in"

        while workflow_name != "A" and workflow_name != "R":
            workflow_name = workflows[workflow_name].get_next_destination(ip)
        if workflow_name == "A":
            accepted_sum += sum(ip.values())
    return accepted_sum


def part2(lines: List[str]) -> int:
    workflows, _ = parse_lines(lines)

    def get_guaranteed_end(dests: List[str]) -> List[str]:
        ret = list(
            filter(
                lambda workflow: workflow.name not in dests
                and all(map(lambda d: d in dests, workflow.destinations)),
                workflows.values(),
            )
        )
        return list(map(lambda workflow: workflow.name, ret))

    guaranteed_rejected = get_guaranteed_end(["R"])
    guaranteed_accepted = get_guaranteed_end(["A"])

    # extrapolate to try to get rid of as many guaranteed rejected as possible
    prev_len = 0
    cur_len = len(guaranteed_rejected)
    while prev_len != cur_len:
        guaranteed_rejected.extend(get_guaranteed_end(guaranteed_rejected))
        prev_len = cur_len
        cur_len = len(guaranteed_rejected)

    # extrapolate to try to get as many guaranteed accepted as possible
    prev_len = 0
    cur_len = len(guaranteed_accepted)
    while prev_len != cur_len:
        guaranteed_accepted.extend(get_guaranteed_end(guaranteed_accepted))
        prev_len = cur_len
        cur_len = len(guaranteed_accepted)

    # remove the guaranteed accepted/rejected
    workflows = list(
        filter(
            lambda workflow: workflow.name not in guaranteed_accepted
            and workflow.name not in guaranteed_rejected,
            workflows.values(),
        )
    )
    workflows = {workflow.name: workflow for workflow in workflows}

    # go through possibilities
    # each range is inclusive
    cur_options = OrderedDict(
        {"in": [{"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}]}
    )
    next_options = OrderedDict()
    grand_total = 0  # total num accepted
    while len(cur_options) > 0:  # while we haven't exhausted all connections
        while len(cur_options) > 0:  # go through all the items in the current stack
            workflow, ranges = cur_options.popitem()

            # for each range, sort it to its corresponding next workflow
            for r in ranges:
                # go through the conditions to see which workflow the range ends up
                for i in range(len(workflows[workflow].conditions)):
                    # it's the final one, so just pass the range to the next workflow
                    if i == len(workflows[workflow].conditions) - 1:
                        dest = workflows[workflow].destinations[-1]
                        if dest not in next_options:
                            next_options[dest] = []
                        next_options[dest].append(r)
                    else:
                        # split the range
                        checker: Checker = workflows[workflow].conditions[i]
                        if checker.operation == ">":
                            # if the max value is less than or equal to the val
                            # that it has to be greater than, then everything is 'false'
                            if r[checker.comparable][1] <= checker.num:
                                # since it's false, continue to the next check
                                continue
                            # if it's entirely larger, then just keep the range as is
                            # but pass it to the next workflow
                            elif r[checker.comparable][0] > checker.num:
                                if checker.dest not in next_options:
                                    next_options[checker.dest] = []
                                next_options[checker.dest].append(r)
                            else:
                                # need to split it into a section that goes to the next workflow
                                # and one that goes to the next check
                                rgt = {key: val.copy() for key, val in r.items()}
                                # set min  of gt range
                                rgt[checker.comparable][0] = checker.num + 1

                                # add it
                                if checker.dest not in next_options:
                                    next_options[checker.dest] = []
                                next_options[checker.dest].append(rgt)

                                # set max of lt range
                                r[checker.comparable][1] = checker.num
                        elif checker.operation == "<":
                            # if the min value is greater than or equal to the val
                            # that it has to be less than, then everything is 'false'
                            if r[checker.comparable][0] >= checker.num:
                                # since it's false, continue to the next check
                                continue
                            # if it's entirely smaller, then just keep the range as is
                            # but pass it to the next workflow
                            elif r[checker.comparable][1] < checker.num:
                                if checker.dest not in next_options:
                                    next_options[checker.dest] = []
                                next_options[checker.dest].append(r)
                            else:
                                # need to split it into a section that goes to the next workflow
                                # and one that goes to the next check
                                rlt = {key: val.copy() for key, val in r.items()}
                                # set max of lt range
                                rlt[checker.comparable][1] = checker.num - 1

                                # add it
                                if checker.dest not in next_options:
                                    next_options[checker.dest] = []
                                next_options[checker.dest].append(rlt)

                                # set min of gt range
                                r[checker.comparable][0] = checker.num

        # don't count any R values or values that are guaranteed to be R
        for reject in guaranteed_rejected + ["R"]:
            if reject in next_options:
                del next_options[reject]

        # count any A values or values that are guaranteed to be A
        for accept in guaranteed_accepted + ["A"]:
            if accept in next_options:
                # sum the total numbers
                for accepted_range in next_options[accept]:
                    num_x = accepted_range["x"][1] - accepted_range["x"][0] + 1
                    num_a = accepted_range["a"][1] - accepted_range["a"][0] + 1
                    num_m = accepted_range["m"][1] - accepted_range["m"][0] + 1
                    num_s = accepted_range["s"][1] - accepted_range["s"][0] + 1
                    grand_total += num_x * num_a * num_m * num_s
                del next_options[accept]
        cur_options = next_options
        next_options = OrderedDict()
        i += 1

    return grand_total


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
