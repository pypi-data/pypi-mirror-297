def default_directed_agg_weight(df):
    dialogue_counts = dict()

    for _, row in df.iterrows():
        speakers = row['speakers']
        listeners = row['listeners']

        for speaker in speakers:
            for listener in listeners:
                if speaker != listener:
                    if (speaker, listener) in dialogue_counts:
                        dialogue_counts[(speaker, listener)] += row['weights']
                    else:
                        dialogue_counts[(speaker, listener)] = row['weights']

    return dialogue_counts


def default_undirected_agg_weight(df):
    dialogue_counts = dict()

    for _, row in df.iterrows():
        participants = row['participants']

        # set 1 for each pair of participants
        for i, part_i in enumerate(participants):
            for part_j in participants[i + 1:]:
                if part_i != part_j:
                    if (part_i, part_j) in dialogue_counts:
                        dialogue_counts[(part_i, part_j)] += row['weights']
                    else:
                        dialogue_counts[(part_i, part_j)] = row['weights']

    return dialogue_counts
