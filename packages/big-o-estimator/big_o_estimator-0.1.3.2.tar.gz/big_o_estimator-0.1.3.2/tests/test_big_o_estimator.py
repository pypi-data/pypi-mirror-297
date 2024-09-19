from big_o_estimator.estimator import get_big_o_of_function


def nested_loop_algorithm(n):
    for i in range(n):
        for j in range(n):
            pass


def recursive_algorithm(n):
    if n <= 1:
        return 1
    else:
        return recursive_algorithm(n - 1) + recursive_algorithm(n - 2)


def constant_time_algorithm(n):
    return n * 2

def test_big_o_estimation():
    results = {
        "Nested Loop Algorithm": get_big_o_of_function(nested_loop_algorithm),
        "Recursive Algorithm": get_big_o_of_function(recursive_algorithm),
        "Constant Time Algorithm": get_big_o_of_function(constant_time_algorithm),
        # Add more test cases here...
    }
    return results


if __name__ == "__main__":
    test_results = test_big_o_estimation()
    for test_name, result in test_results.items():
        print(f"{test_name}: {result}")
