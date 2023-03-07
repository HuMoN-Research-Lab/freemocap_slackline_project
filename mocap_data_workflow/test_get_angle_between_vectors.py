import numpy as np


from extract_state_information import get_angle_between_vectors, normalize_vector

def test_forty_five_degree_angles():
    y_vector = [0,1]

    assert np.degrees(get_angle_between_vectors(y_vector,normalize_vector([1,1]))) == 45
    assert np.degrees(get_angle_between_vectors(y_vector,normalize_vector([-1,1]))) == -45
    
    print("Function properly handles forty five degree angles")

def test_right_angles():
    x_vector = [1,0]
    negative_x_vector = [-1,0]
    y_vector = [0,1]
    negative_y_vector = [0,-1]

    assert np.degrees(get_angle_between_vectors(y_vector, x_vector)) == 90
    assert np.degrees(get_angle_between_vectors(x_vector, y_vector)) == -90
    assert np.degrees(get_angle_between_vectors(x_vector, negative_y_vector)) == 90
    assert np.degrees(get_angle_between_vectors(y_vector, negative_x_vector)) == -90
    assert np.degrees(get_angle_between_vectors(negative_x_vector, y_vector)) == 90
    assert np.degrees(get_angle_between_vectors(negative_y_vector, x_vector)) == -90
    assert np.degrees(get_angle_between_vectors(negative_y_vector, negative_x_vector)) == 90
    assert np.degrees(get_angle_between_vectors(negative_x_vector, negative_y_vector)) == -90

    print("Function properly handles right angles")

def test_zero_angle():
    y_vector = [0,1]

    assert np.degrees(get_angle_between_vectors(y_vector,y_vector)) == 0

    print("Function properly handles 0 degree angle")


def main():
    test_forty_five_degree_angles()
    test_right_angles()
    test_zero_angle()


if __name__ == "__main__":
    main()