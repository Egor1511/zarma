import timeit
import unittest


class TestOptimization(unittest.TestCase):

    def test_speed_comparison(self):
        def original():
            numbers = [i for i in range(1, 1000001)]
            squares = []
            for number in numbers:
                squares.append(number ** 2)
            return squares

        def optimized():
            numbers = range(1, 1000001)
            squares = [number ** 2 for number in numbers]
            return squares

        original_time = timeit.timeit(original, number=10)
        optimized_time = timeit.timeit(optimized, number=10)

        print(f"Original script time: {original_time:.4f} seconds")
        print(f"Optimized script time: {optimized_time:.4f} seconds")


if __name__ == '__main__':
    unittest.main()
