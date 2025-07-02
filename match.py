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


def collect_people(klass, role):
    people = []
    count = int(input(f"Enter number of {role}: "))
    for i in range(count):
        name = input(f"{role.capitalize()} #{i+1} name: ")
        location = input(f"{role.capitalize()} #{i+1} location: ")
        people.append(klass(name, location))
    return people


if __name__ == "__main__":
    makers = collect_people(KimchiMaker, "makers")
    requesters = collect_people(KimchiRequester, "requesters")

    matches = match_makers_to_requesters(makers, requesters)

    for maker, requester in matches:
        print(f"{maker.name} can make kimchi for {requester.name} in {maker.location}")
