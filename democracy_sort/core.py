import random
from collections import Counter

def biased_vote(options, prior_votes, bias_strength=0.001):
    if not prior_votes:
        return random.choice(options)
    counts = Counter(prior_votes)
    total = sum(counts.values())
    weights = []
    for option in options:
        majority_bias = counts[option] / total if option in counts else 0
        biased_weight = (1 - bias_strength) + (bias_strength * majority_bias)
        weights.append(biased_weight)
    return random.choices(options, weights=weights, k=1)[0]

def democratic_sort(data, num_voters=10, max_rounds=1000, bias_strength=0.001, debug=False):
    lst = data[:]
    n = len(lst)

    for round_num in range(max_rounds):
        if debug:
            print(f"\n=== Round {round_num + 1} ===")
        inspect_votes = []
        if debug:
            print("Voting on index to inspect:")
        for voter_id in range(num_voters):
            vote = biased_vote(list(range(n)), inspect_votes, bias_strength)
            inspect_votes.append(vote)
            if debug:
                print(f"  Voter {voter_id} voted to inspect index {vote} (value: {lst[vote]})")

        chosen_index = Counter(inspect_votes).most_common(1)[0][0]
        item = lst[chosen_index]
        if debug:
            print(f"Chosen index to inspect (majority): {chosen_index} (value: {item})")

        ideal_index = sum(1 for x in lst if x < item)

        position_votes = []
        if debug:
            print("Voting on where to move the item:")
        for voter_id in range(num_voters):
            vote = biased_vote(list(range(n)), position_votes, bias_strength)
            position_votes.append(vote)
            if debug:
                print(f"  Voter {voter_id} voted to move to index {vote}")

        target_index = Counter(position_votes).most_common(1)[0][0]
        if debug:
            print(f"Chosen index to move to (majority): {target_index}")

        if target_index != chosen_index:
            lst.pop(chosen_index)
            lst.insert(target_index, item)
            if debug:
                print(f"Moved item {item} from index {chosen_index} to {target_index}")
        else:
            if debug:
                print("No movement this round.")

        if debug:
            print(f"Current list: {lst}")

        if lst == sorted(lst):
            if debug:
                print(f"\n🎉 Sorted in {round_num + 1} rounds.")
            break

    return lst
