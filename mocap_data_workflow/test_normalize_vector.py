import numpy as np
from extract_state_information import normalize_vector

def test_unit_vector():
    assert np.linalg.norm(normalize_vector([1]) == 1)
    assert np.linalg.norm(normalize_vector([1,0,0]) == 1)
    assert np.linalg.norm(normalize_vector([0,1]) == 1)

    print("Unit cases function correctly")

def test_random_vectors():
    assert int(np.linalg.norm(normalize_vector([4]))) == 1
    assert int(np.linalg.norm(normalize_vector([9,13,7]))) == 1
    assert int(np.linalg.norm(normalize_vector([-5,19]))) == 1

    print("Random vectors function correctly")

def main():
    test_unit_vector()
    test_random_vectors()

if __name__ == "__main__":
    main()