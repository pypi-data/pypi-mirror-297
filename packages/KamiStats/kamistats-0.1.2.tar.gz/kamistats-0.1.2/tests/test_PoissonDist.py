import json
import unittest
from KamiStats.distributions import PoissonDist

class PoissonDist_Test(unittest.TestCase):
    def __init__(self):
        """Load the test data from the JSON file"""
        with open('KamiStats/tests/Poisson.json', 'r') as file:
            self.data = json.load(file)
        self.positive_cases = [d for d in self.data if d["Case"] == "Positive"]
        self.negative_cases = [d for d in self.data if d["Case"] == "Negative"]

    def test_newInstance_mean(self):
        """Tests the mean property of the PoissonDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)
        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.mean
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class mean: {round(result, 6)}")
                print("Expected mean: ", d['expected']['mean'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")

        for d in self.negative_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.mean
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")

        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)
    
    def test_newInstance_variance(self):
        """Tests the variance property of the PoissonDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)

        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.variance
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class variance: {round(result, 6)}")
                print("Expected variance: ", d['expected']['variance'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")

        for d in self.negative_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.variance
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")

        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)

    def test_newInstance_std_dev(self):
        """Tests the standard deviation property of the PoissonDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)

        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.std_dev
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class std_dev: {round(result, 6)}")
                print("Expected std_dev: ", d['expected']['std_dev'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")

        for d in self.negative_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.std_dev
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")

        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)

    def test_newInstance_pmf(self):
        """Tests the pmf method of the PoissonDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)

        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.pmf()
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class pmf: {round(result, 6)}")
                print("Expected pmf: ", d['expected']['pmf'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")
             

        for d in self.negative_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.pmf()
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")

        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)
    
    def test_newInstance_cdf(self):
        """Tests the cdf method of the PoissonDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)

        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.cdf()
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class cdf: {round(result, 6)}")
                print("Expected cdf: ", d['expected']['cdf'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")

        for d in self.negative_cases:
            try:
                dist_instance = PoissonDist(d['parameters']['_λ'], d['parameters']['_k'])
                result = dist_instance.cdf()
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")

        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)
        





def main():
    test_instance = PoissonDist_Test()
    # print(25 * " ~%~")
    # print("\n\n\t\t\t\tTesting PoissonDist Class mean\n\n")
    # print(25 * " ~%~")
    # print(test_instance.test_newInstance_mean())
    # print(25 * " ~%~")
    # print("\n\n\t\t\t\tEnd of Testing PoissonDist Class mean\n\n")
    # print(25 * " ~%~")

    # print(25 * " ~%~")
    # print("\n\n\t\t\t\tTesting PoissonDist Class variance\n\n")
    # print(25 * " ~%~")
    # print(test_instance.test_newInstance_variance())
    # print(25 * " ~%~")
    # print("\n\n\t\t\t\tEnd of Testing PoissonDist Class variance\n\n")
    # print(25 * " ~%~")

    # print(25 * " ~%~")
    # print("\n\n\t\t\t\tTesting PoissonDist Class std_dev\n\n")
    # print(25 * " ~%~")
    # print(test_instance.test_newInstance_std_dev())
    # print(25 * " ~%~")
    # print("\n\n\t\t\t\tEnd of Testing PoissonDist Class std_dev\n\n")
    # print(25 * " ~%~")

    print(25 * " ~%~")
    print("\n\n\t\t\t\tTesting PoissonDist Class pmf\n\n")
    print(25 * " ~%~")
    print(test_instance.test_newInstance_pmf())
    print(25 * " ~%~")
    print("\n\n\t\t\t\tEnd of Testing PoissonDist Class pmf\n\n")
    print(25 * " ~%~")

    print(25 * " ~%~")
    print("\n\n\t\t\t\tTesting PoissonDist Class cdf\n\n")
    print(25 * " ~%~")
    print(test_instance.test_newInstance_cdf())
    print(25 * " ~%~")
    print("\n\n\t\t\t\tEnd of Testing PoissonDist Class\n\n")
    print(25 * " ~%~")

if __name__ == "__main__":
    main()