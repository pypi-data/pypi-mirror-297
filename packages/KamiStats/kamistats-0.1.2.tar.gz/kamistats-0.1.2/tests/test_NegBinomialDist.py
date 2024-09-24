import json 
import unittest
from KamiStats.distributions import NegativeBinomialDist

class NegBinomialDist_Test(unittest.TestCase):
    def __init__(self):
        """Load the test data from the JSON file"""
        with open('KamiStats/tests/NegativeBinomialDist.json', 'r') as file:
            self.data = json.load(file)
        self.positive_cases = [d for d in self.data if d["Case"] == "Positive"]
        self.negative_cases = [d for d in self.data if d["Case"] == "Negative"]

    def test_newInstance_mean(self):
        """Tests the mean property of the Negative BinomialDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)
        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.mean
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class mean: {round(result, 6)}")
                print("Expected mean: ", d['expected']['mean'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")

        for d in self.negative_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.mean
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")

        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)

    def test_newInstance_variance(self):
        """Tests the variance property of the Negative BinomialDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)

        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.variance
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class variance: {round(result, 6)}")
                print("Expected variance: ", d['expected']['variance'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")
        
        for d in self.negative_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.variance
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")
        
        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)

    def test_newInstance_pmf(self):
        """Tests the pmf method of the Negative BinomialDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)

        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.pmf()
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class pmf: {round(result, 6)}")
                print("Expected pmf: ", d['expected']['pmf'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")
        
        for d in self.negative_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.pmf()
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")
        
        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)
    
    def test_newInstance_cdf(self):
        """Tests the cdf method of the Negative BinomialDist class"""
        num_positive_cases = len(self.positive_cases)
        num_negative_cases = len(self.negative_cases)
        print("Number of positive test cases: ", num_positive_cases)
        print("Number of negative test cases: ", num_negative_cases)

        count_successful_positive = 0
        count_successful_negative = 0

        for d in self.positive_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.cdf()
                self.assertIsNotNone(result)
                count_successful_positive += 1
                print(f"Test case: {d}, Class cdf: {round(result, 6)}")
                print("Expected cdf: ", d['expected']['cdf'], "\n")
            except Exception as e:
                print(f"\nError in positive test case: {d}, Error: {e}\n")
        
        for d in self.negative_cases:
            try:
                dist_instance = NegativeBinomialDist(d['parameters']['_r'], d['parameters']['_p'], d['parameters']['_q'], d['parameters']['_k'])
                result = dist_instance.cdf()
                self.assertIsNotNone(result)
            except Exception as e:
                count_successful_negative += 1
                print(f"Error in negative test case: {d}, Error: {e}\n")
        
        print("\n\n")
        print("Number of successful positive test cases: ", count_successful_positive)
        print("Number of successful negative test cases: ", count_successful_negative)
    

def main():
    test_instance = NegBinomialDist_Test()
    print(25 * " ~%~")
    print("\n\n\t\t\t\tTesting Negative Binomial Class mean\n\n")
    print(25 * " ~%~")
    print(test_instance.test_newInstance_mean())
    print(25 * " ~%~")
    print("\n\n\t\t\t\tEnd of Testing Negative Binomial Class mean\n\n")
    print(25 * " ~%~")

    print(25 * " ~%~")
    print("\n\n\t\t\t\tTesting Negative Binomial Class variance\n\n")
    print(25 * " ~%~")
    print(test_instance.test_newInstance_variance())
    print(25 * " ~%~")
    print("\n\n\t\t\t\tEnd of Testing Negative Binomial Class variance\n\n")
    print(25 * " ~%~")

    print(25 * " ~%~")
    print("\n\n\t\t\t\tTesting Negative Binomial Class pmf\n\n")
    print(25 * " ~%~")
    print(test_instance.test_newInstance_pmf())
    print(25 * " ~%~")
    print("\n\n\t\t\t\tEnd of Testing Negative Binomial Class pmf\n\n")
    print(25 * " ~%~")

    print(25 * " ~%~")
    print("\n\n\t\t\t\tTesting Negative Binomial Class cdf\n\n")
    print(25 * " ~%~")
    print(test_instance.test_newInstance_cdf())
    print(25 * " ~%~")
    print("\n\n\t\t\t\tEnd of Testing Negative Binomial Class\n\n")
    print(25 * " ~%~")


if __name__ == "__main__":
    main()