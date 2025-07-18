"""Upper Body connections."""

POSE_CONNECTIONS = ((0, 1), (0,2), (1, 3), (2, 4), (3, 5), (5, 27), (4, 6))

#Left Hand
LEFT_HAND_PALM_CONNECTIONS = ((6, 7), (6, 11), (15, 19), (19, 23), (11, 15), (6, 23))
LEFT_HAND_THUMB_CONNECTIONS = ((7, 8), (8, 9), (9, 10))
LEFT_HAND_INDEX_FINGER_CONNECTIONS = ((11, 12), (12, 13), (13, 14))
LEFT_HAND_MIDDLE_FINGER_CONNECTIONS = ((15, 16), (16, 17), (17, 18))
LEFT_HAND_RING_FINGER_CONNECTIONS = ((19, 20), (20, 21), (21, 22))
LEFT_HAND_PINKY_FINGER_CONNECTIONS = ((23, 24), (24, 25), (25, 26))


#Right Hand
RIGHT_HAND_PALM_CONNECTIONS = ((27, 28), (27, 32), (36, 40), (40, 44), (32, 36), (27, 44))
RIGHT_HAND_THUMB_CONNECTIONS = ((28, 29), (29, 30), (30, 31))
RIGHT_HAND_INDEX_FINGER_CONNECTIONS = ((32, 33), (33, 34), (34, 35))
RIGHT_HAND_MIDDLE_FINGER_CONNECTIONS = ((36, 37), (37, 38), (38, 39))
RIGHT_HAND_RING_FINGER_CONNECTIONS = ((40, 41), (41, 42), (42, 43))
RIGHT_HAND_PINKY_FINGER_CONNECTIONS = ((44, 45), (45, 46), (46, 47))


UPPER_CONNECTIONS = frozenset().union(*[
    POSE_CONNECTIONS,
    LEFT_HAND_PALM_CONNECTIONS, LEFT_HAND_THUMB_CONNECTIONS,
    LEFT_HAND_INDEX_FINGER_CONNECTIONS, LEFT_HAND_MIDDLE_FINGER_CONNECTIONS,
    LEFT_HAND_RING_FINGER_CONNECTIONS, LEFT_HAND_PINKY_FINGER_CONNECTIONS,
    RIGHT_HAND_PALM_CONNECTIONS, RIGHT_HAND_THUMB_CONNECTIONS,
    RIGHT_HAND_INDEX_FINGER_CONNECTIONS, RIGHT_HAND_MIDDLE_FINGER_CONNECTIONS,
    RIGHT_HAND_RING_FINGER_CONNECTIONS, RIGHT_HAND_PINKY_FINGER_CONNECTIONS
])