"""Core matching logic and a small interactive command-line demo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class KimchiMaker:
    name: str
    location: str


@dataclass(frozen=True)
class KimchiRequester:
    name: str
    location: str


def match_makers_to_requesters(makers, requesters):
    """Return maker/requester pairs whose normalized locations match."""
    return [
        (maker, requester)
        for maker in makers
        for requester in requesters
        if maker.location.strip().casefold() == requester.location.strip().casefold()
    ]


def collect_people(person_type, role):
    while True:
        try:
            count = int(input(f"Enter number of {role}: "))
            if count < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a non-negative whole number.")

    people = []
    for index in range(count):
        while not (name := input(f"{role.capitalize()} #{index + 1} name: ").strip()):
            print("Name cannot be empty.")
        while not (location := input(f"{role.capitalize()} #{index + 1} location: ").strip()):
            print("Location cannot be empty.")
        people.append(person_type(name, location))
    return people


if __name__ == "__main__":
    makers = collect_people(KimchiMaker, "makers")
    requesters = collect_people(KimchiRequester, "requesters")

    matches = match_makers_to_requesters(makers, requesters)
    if not matches:
        print("No matches found.")
    for maker, requester in matches:
        print(f"{maker.name} can make kimchi for {requester.name} in {maker.location}")
