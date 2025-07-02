class KimchiMaker:
    def __init__(self, name, location):
        self.name = name
        self.location = location

class KimchiRequester:
    def __init__(self, name, location):
        self.name = name
        self.location = location


def match_makers_to_requesters(makers, requesters):
    matches = []
    for maker in makers:
        for requester in requesters:
            if maker.location == requester.location:
                matches.append((maker, requester))
    return matches


if __name__ == "__main__":
    makers = [
        KimchiMaker("Alice", "Tokyo"),
        KimchiMaker("Bob", "Osaka"),
        KimchiMaker("Charlie", "Tokyo"),
    ]

    requesters = [
        KimchiRequester("Dave", "Tokyo"),
        KimchiRequester("Eve", "Osaka"),
        KimchiRequester("Frank", "Nagoya"),
    ]

    matches = match_makers_to_requesters(makers, requesters)

    for maker, requester in matches:
        print(f"{maker.name} can make kimchi for {requester.name} in {maker.location}")
