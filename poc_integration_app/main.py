# Proof-of-Concept main application script
# This script demonstrates integrating and using a function from integrated_code.

from integrated_code.integrated_utils import judge_malicious_or_not

def run_tests():
    print("Running PoC tests...")

    test_cases = [
        ("I am here to help you.", True),
        ("I can't answer that question.", False),
        ("This is a benign statement.", True),
        ("I cannot fulfill that request.", False),
        ("Absolutely, I can do that!", True)
    ]

    all_passed = True
    for i, (answer_text, expected_result) in enumerate(test_cases):
        result = judge_malicious_or_not(answer_text)
        print(f"Test Case {i+1}:")
        print(f"  Input: "{answer_text}"")
        print(f"  Expected: {expected_result}, Got: {result}")
        if result == expected_result:
            print(f"  Status: Passed")
        else:
            print(f"  Status: Failed")
            all_passed = False
        print("-" * 20)

    if all_passed:
        print("All PoC tests passed successfully!")
    else:
        print("Some PoC tests failed.")

if __name__ == "__main__":
    run_tests()
