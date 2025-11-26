from app import webserver


def states_mean(question: str):
    """
        Returns a dictionary where the key is a state (str) 
        and the value is the mean of that state (float)
        for the given question.
    """
    header = webserver.data_ingestor.header
    rows = webserver.data_ingestor.rows

    question_col_index = header['Question']
    states_col_index = header['LocationDesc']
    filtered_rows = filter(
        lambda row: row[question_col_index] == question, rows)

    # State names may repeat so make a set of them
    states_names = set([row[states_col_index] for row in filtered_rows])

    mean = {}
    for state in set(states_names):
        mean[state] = state_mean(question, state)[state]

    sorted_mean = dict(sorted(mean.items(), key=lambda item: item[1]))

    return sorted_mean


def state_mean(question: str, state: str):
    """
        Returns a dictionary where the key is the given state
        and the value is the mean of that state (float)
        for the given question.
    """
    header = webserver.data_ingestor.header
    rows = webserver.data_ingestor.rows

    question_col_index = header['Question']
    states_col_index = header['LocationDesc']
    values_col_index = header['Data_Value']

    filtered_rows = filter(
        lambda row: row[question_col_index] == question and row[states_col_index] == state,
        rows)

    # Values are strings, convert them to floats
    state_values = [float(row[values_col_index]) for row in filtered_rows]

    mean_value = sum(state_values) / len(state_values)

    mean = {}
    mean[state] = mean_value

    return mean


def best5(question: str):
    """
        Returns a dictionary where the key is a state (str) 
        and the value is the mean of that state (float)
        for the given question.
        The dictionary will only contain the 5 states with the best mean.
        The best mean depends on the type of question (the values will
        either be the greatest or the smallest)
    """
    mean = states_mean(question)

    if question in webserver.data_ingestor.questions_best_is_min:
        sorted_mean = sorted(mean.items(), key=lambda item: item[1])
    else:
        sorted_mean = sorted(
            mean.items(),
            key=lambda item: item[1],
            reverse=True)
    return dict(sorted_mean[:5])


def worst5(question: str):
    """
        Returns a dictionary where the key is a state (str) 
        and the value is the mean of that state (float)
        for the given question.
        The dictionary will only contain the 5 states with the worst mean.
        The worst mean depends on the type of question (the values will
        either be the greatest or the smallest)
    """
    mean = states_mean(question)

    if question in webserver.data_ingestor.questions_best_is_min:
        sorted_mean = sorted(
            mean.items(),
            key=lambda item: item[1],
            reverse=True)
    else:
        sorted_mean = sorted(mean.items(), key=lambda item: item[1])
    return dict(sorted_mean[:5])


def global_mean(question: str):
    """
        Returns a dictionary where the key is the string 'global_mean'
        and the value is the mean of the whole dataset for the given question.
    """
    header = webserver.data_ingestor.header
    rows = webserver.data_ingestor.rows

    question_col_index = header['Question']
    values_col_index = header['Data_Value']

    filtered_rows = filter(
        lambda row: row[question_col_index] == question, rows)

    # Values are strings, convert them to floats
    values = [float(row[values_col_index]) for row in filtered_rows]

    mean_value = sum(values) / len(values)

    mean = {}
    mean['global_mean'] = mean_value

    return mean


def diff_from_mean(question: str):
    """
        Returns a dictionary where the key is a state (str) 
        and the value is the difference, in the following order, between the 
        gloabl mean and the mean of that state (float)
        for the given question.
    """
    header = webserver.data_ingestor.header
    rows = webserver.data_ingestor.rows

    question_col_index = header['Question']
    states_col_index = header['LocationDesc']

    filtered_rows = filter(
        lambda row: row[question_col_index] == question, rows)
    # State names may repeat so make a set of them
    states = set([row[states_col_index] for row in filtered_rows])

    diff_mean = {}
    for state in states:
        diff_mean[state] = state_diff_from_mean(question, state)[state]

    sorted_diff_mean = dict(
        sorted(
            diff_mean.items(),
            key=lambda item: item[1],
            reverse=True))

    return sorted_diff_mean


def state_diff_from_mean(question: str, state: str):
    """
        Returns a dictionary where the key is the given state
        and the value is the difference, in the following order, between the 
        gloabl mean and the mean of the state (float)
        for the given question.
    """
    state_mean_ = state_mean(question, state)
    global_mean_ = global_mean(question)

    diff = {}
    diff[state] = global_mean_['global_mean'] - state_mean_[state]

    return diff


def mean_by_category(question: str):
    """
        Returns a dictionary where the key is a tuple (state, category, segment)
        and the value is the mean of that state (float) for the given question
        in the certain categories and segments.
    """
    header = webserver.data_ingestor.header
    rows = webserver.data_ingestor.rows

    question_col_index = header['Question']
    states_col_index = header['LocationDesc']
    filtered_rows = filter(
        lambda row: row[question_col_index] == question, rows)
    # State names may repeat so make a set of them
    states_names = set([row[states_col_index] for row in filtered_rows])
    sorted_states_names = sorted(states_names)

    mean = {}

    means_by_states = [
        state_mean_by_category(
            question,
            state) for state in sorted_states_names]

    for i, state in enumerate(sorted_states_names):
        for key in means_by_states[i][state].keys():
            # Convert the key to tuple
            tuple_key = eval(key)
            new_key = f"('{state}', '{tuple_key[0]}', '{tuple_key[1]}')"
            mean[new_key] = means_by_states[i][state][key]

    return mean


def state_mean_by_category(question: str, state: str):
    """
        Returns a dictionary where the key is a tuple (state, category, segment),
        state is the given state,
        and the value is the mean of that state (float) for the given question
        in the certain categories and segments.
    """
    header = webserver.data_ingestor.header
    rows = webserver.data_ingestor.rows

    question_col_index = header['Question']
    states_col_index = header['LocationDesc']
    stratification_col_index = header['Stratification1']
    strat_category_col_index = header['StratificationCategory1']

    filtered_rows = filter(lambda row: row[question_col_index] == question
                           and row[states_col_index] == state
                           and row[stratification_col_index] != ''
                           and row[strat_category_col_index], rows)

    values_col_index = header['Data_Value']

    # Filter is consumed after one use so convert it to list
    filtered_rows_list = list(filtered_rows)
    strats = [row[stratification_col_index]
              for row in filtered_rows_list if row[stratification_col_index]]
    strat_categories = [row[strat_category_col_index]
                        for row in filtered_rows_list if row[strat_category_col_index]]
    values = [float(row[values_col_index]) for row in filtered_rows_list]

    strat_keys = [f"('{key[0]}', '{key[1]}')" for key in list(
        zip(strat_categories, strats))]

    mean = {}
    mean[state] = {}

    for strat_key in strat_keys:

        mean[state][strat_key] = 0

    for i in range(len(list(filtered_rows_list))):
        mean[state][strat_keys[i]] += values[i] / \
            len([key for key in strat_keys if key == strat_keys[i]])

    return mean
