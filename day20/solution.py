from typing import List, Tuple, Dict
from abc import abstractmethod
from queue import Queue
from math import lcm


class Switch:
    def __init__(self, name: str, to_connections: List[str]):
        self.name = name
        self.to_connections = to_connections

    @abstractmethod
    def handle_input(self, ip: Tuple[str, str, str]) -> List[Tuple[str, str]]:
        """
        Handle the input.
        Arguments:
            - `ip` - Tuple[str, str] - (from, to, high/low)
                - from should be the name of the previous switch
                - to should be the name of this switch
                - high/low should just be a str that is high or low; the pulse type
        """
        pass

    def generate_impulse(self, impulse: str) -> List[Tuple[str, str, str]]:
        return [(self.name, conn, impulse) for conn in self.to_connections]

    def __eq__(self, __value: object) -> bool:
        return (
            type(self) == type(__value)
            and self.name == __value.name
            and self.to_connections == __value.to_connections
        )


class FlipFlop(Switch):
    def __init__(self, name: str, to_connections: List[str]) -> None:
        super().__init__(name, to_connections)
        self.state = False  # False = Off, True = On

    def handle_input(self, ip: Tuple[str, str, str]) -> List[Tuple[str, str]]:
        _, _, high_low = ip
        if high_low == "high":
            return []
        else:
            if self.state:
                # was On, switching to off, so send low
                ret = self.generate_impulse("low")
            else:
                # was off, switching to on, so send high
                ret = self.generate_impulse("high")

            # switch
            self.state = not self.state
            return ret

    def __repr__(self) -> str:
        return f"Swich: {'on' if self.state else 'off'}"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, __value: object) -> bool:
        return super() == __value and __value.state == self.state

    def __hash__(self) -> int:
        return hash((self.name, tuple(self.to_connections), self.state))


class Conjunction(Switch):
    def __init__(
        self, name: str, to_connections: List[str], from_connections: List[str]
    ):
        super().__init__(name, to_connections)
        self.from_connections = {conn: "low" for conn in from_connections}

    def handle_input(self, ip: Tuple[str, str, str]) -> List[Tuple[str, str]]:
        from_, _, high_low = ip
        self.from_connections[from_] = high_low

        if all(map(lambda v: v == "high", self.from_connections.values())):
            # if it remembers highs for all its incoming connections
            return self.generate_impulse("low")
        else:
            return self.generate_impulse("high")

    def __repr__(self) -> str:
        return f"Conjunction: {self.from_connections}"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, __value: object) -> bool:
        return super() == __value and __value.from_connections == self.from_connections

    def __hash__(self) -> int:
        return hash(
            (
                self.name,
                tuple(self.to_connections),
                tuple(list(self.from_connections.values())),
                tuple(list(self.from_connections.keys())),
            )
        )


def parse_lines(lines: List[str]) -> Tuple[List[str], Dict[str, Switch]]:
    """
    Returns the broadcaster's connections and a map of
    connection_name: Switch
    """

    def get_connections(line: str) -> List[str]:
        return list(map(lambda s: s.strip(), line[line.index(">") + 1 :].split(",")))

    broadcaster_connections = []
    connections = {}
    types = {}
    for line in lines:
        if line[0] != "b":  # it isn't 'broadcaster'
            name = line[: line.index("-")].strip("%").strip("&").strip()
            connects = get_connections(line)
            connections[name] = connects
            types[name] = line[0]
        else:
            broadcaster_connections = get_connections(line)

    switch_connections = {}
    for conn_name in connections:
        if types[conn_name] == "%":
            switch_connections[conn_name] = FlipFlop(conn_name, connections[conn_name])
        elif types[conn_name] == "&":
            from_connections = list(
                filter(lambda key: conn_name in connections[key], connections)
            )
            switch_connections[conn_name] = Conjunction(
                conn_name, connections[conn_name], from_connections
            )
        else:
            print("shouldn't happen")
    return broadcaster_connections, switch_connections


def simulate_button(
    broadcaster_connections: List[str],
    switch_conns: Dict[str, Switch],
    listeners: List[str] = [],
) -> Tuple[int, int, List[Tuple[str, str, str]]]:
    """
    Modifies switch_conns in place
    Returns:
        - Tuple[int, int, List[Tuple[str, str, str]]] - the number of high impulses sent
            and the number of low impulses sent, as well as a list of all the impulses
            to listen for
    """
    num_low = len(broadcaster_connections) + 1  # add 1 bc of the button
    num_high = 0
    listened = []

    q = Queue()  # stores tuples of (from, to, high/low)
    for conn_name in broadcaster_connections:
        q.put(("broadcaster", conn_name, "low"))

    while not q.empty():
        impulse = q.get()
        from_, to, _ = impulse
        if from_ in listeners:
            listened.append(impulse)

        # reached an unconnected switch
        if to not in switch_conns:
            continue

        next_impulses = switch_conns[to].handle_input(impulse)
        for next_impulse in next_impulses:
            q.put(next_impulse)
            _, _, high_low = next_impulse
            if high_low == "high":
                num_high += 1
            else:
                num_low += 1

    return num_high, num_low, listened


def part1(lines: List[str], n: int = 1000) -> int:
    def to_state(d: Dict[str, Switch]) -> Tuple[Switch]:
        return tuple(list(d.values()))

    broadcaster_connections, switch_conns = parse_lines(lines)

    total_high, total_low = 0, 0
    # state: (high, low, n)
    seen_states = {to_state(switch_conns): [total_high, total_low, 0]}
    loops: Dict[Tuple[Switch], Tuple[int, int, int]] = {}

    i = 0
    num_simulated = 0
    while i < n:
        cur_state = to_state(switch_conns)
        if cur_state in loops and i + loops[cur_state][2] < n:
            temp_high, temp_low, length = loops[cur_state]
            times_repeated = (n - i) // length
            i += times_repeated * length
            total_high += temp_high * times_repeated
            total_low += temp_low * times_repeated
        else:
            i += 1
            num_simulated += 1
            temp_high, temp_low, _ = simulate_button(
                broadcaster_connections, switch_conns
            )
            total_high += temp_high
            total_low += temp_low

            cur_state = to_state(switch_conns)
            if cur_state in seen_states and i + (i - seen_states[cur_state][2]) < n:
                loops[cur_state] = [
                    total_high - seen_states[cur_state][0],
                    total_low - seen_states[cur_state][1],
                    i - seen_states[cur_state][2],
                ]
            else:
                seen_states[cur_state] = [total_high, total_low, i]

    return total_high * total_low


def part2(lines: List[str]) -> int:
    broadcaster_connections, switch_conns = parse_lines(lines)

    # apparently there are 4 independent submaps according to reddit
    # looking at the input, it seems like each one ends at ft, which
    # feeds to rx
    # thus all we have to do is figure out when each of these independent submaps
    # will produce a high pulse (which will cause ft to produce low pulse)

    # these are the 4 items that feed to ft
    items = ["vz", "bq", "qh", "lt"]
    nums = {}
    i = 0
    while len(nums) != len(items):
        i += 1
        _, _, listened = simulate_button(broadcaster_connections, switch_conns, items)
        # need a high pulse
        listened = list(filter(lambda pair: pair[2] == "high", listened))

        # as it turns out, each of the submaps is independent and repeats,
        # so we can just store the first number we get that produces
        # a high result
        if len(listened) != 0:
            for item in listened:
                nums[item[0]] = i

    return lcm(*nums.values())


if __name__ == "__main__":
    lines = open("input.txt", "r").read().strip().split("\n")
    print(part1(lines))
    print(part2(lines))
