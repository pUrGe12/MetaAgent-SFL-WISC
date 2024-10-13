
def occurance_substring(main_string, sub_string):
    positions = []
    start = 0
    while True:
        start = main_string.find(sub_string, start)
        if start == -1:
            break
        positions.append(start)
        start += len(sub_string)
    
    if not positions:
        return None
    
    return (sub_string, positions[0], len(positions))

# Test cases
test_cases = [
    (' programming,  language', '', ('', 0, 2)),
    (' programming,  language', 'java', None),
    (' programming,  language', '', None),
    ('', '', None),
    ('', '', None),
    ('hello world', 'world', ('world', 6, 1)),
    ('', '', ('', 0, 1)),
    ('aaaaa', 'aaa', ('aaa', 0, 1)),
    ('Python programming,  language', '', ('', 19, 1)),
    ('hello!@#hello!@#', '!@#', ('!@#', 5, 2))
]

# Running the test cases
results = []
for main_string, sub_string, expected in test_cases:
    result = occurance_substring(main_string, sub_string)
    results.append((result, result == expected))

results
