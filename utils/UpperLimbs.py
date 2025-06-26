import cv2
import mediapipe as mp
import numpy as np
from utils import upper_plot


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose


def take_coordinates_pose(coordinates):
    """
    function to extract 3d points from pose model
    :param coordinates: NamedTuple returned from mediapipe.solutions.pose.process
    :return: list of all 3d data of pose.
    """
    if coordinates == None:
        return 0
    keypoints = []
    for xyz in coordinates.landmark:
        X_value = xyz.x
        Y_value = xyz.y
        Z_value = xyz.z
        xy = [X_value, Y_value, Z_value]
        keypoints.append(xy)
    return keypoints

def take_coordinates_hands(coordinates):
    """
    this function extract 3d points data from hands model
    :param coordinates: NamedTuple returned from mediapipe.solutions.hands.process
    :return: list of all 3d data for all hand.
    """
    if coordinates == None:
        return 0
    keypoints = []
    for data_point in coordinates:
        xyz_datapoints = data_point.landmark
        for xyz in xyz_datapoints:
            X_value = xyz.x
            Y_value = xyz.y
            Z_value = xyz.z
            xy = [X_value,Y_value, Z_value]
            keypoints.append(xy)
    return keypoints

def equation_1(hand_points):
    """origin of hans_world_landmark is geometric center of hand.
    this function will change 0th point that is wrist to origin(0,0,0) And map all other points.
    This function will return new coordinates of hand with origin at wrist."""
    if len(hand_points) == 21:
        Translation_Vector_1 = -np.array(hand_points[0])
        New_points1 = [list(np.array(i) + Translation_Vector_1) for i in hand_points]
        return New_points1
    elif len(hand_points) == 42:
        Translation_Vector_1 = -np.array(hand_points[0])
        New_points1 = [list(np.array(i) + Translation_Vector_1) for i in hand_points[:21]]
        Translation_Vector_2 = -np.array(hand_points[21])
        New_points2 = [list(np.array(i) + Translation_Vector_2) for i in hand_points[21:]]
        return New_points1 + New_points2

def equation_1_5(pose_data):
    """
    This function will change origin of pose_data to center between two shoulder.
    With translation vector = -(center of two shoulder)
    :param pose_data: 33 points of pose_world_landmarks with origin in between two hips.
    :return: 33 points of pose_world_data with origin in between two shoulders.
    """
    Translation_Vector = -(np.array(pose_data[11])+np.array(pose_data[12]))/2
    New_Pose_Data = [list(np.array(i) + Translation_Vector) for i in pose_data]
    return New_Pose_Data

def equation_2(pose_data, hand_data, hand_list):
    """This function will take three arguments i.e. new hand coordinates,
    pose coordinates and hand list(max 2).
    And join hand's coordinates with pose's coordinates.
     Wrist of left hand of pose coordinate is 15th point and right hand of
    pose is 16th point of pose coordinates.
     Connect 15th point with 0th oh left hand and connect 16th point with
     0th of right hand by mapping with translation vector = 15th point for left hand
     and translation vector = 16th point for right hand.
    Using 11th to 16th points from pose. That is why 16th point = 5th, 15th point = 4th
     This function will return all joined data of two hand and pose.
     returned data: list, 0~5=pose, 6~26=left hand, 27~47=right hand.
    """
    pose_data = pose_data[11:17]
    pose_data = [pose_data[1], pose_data[0], pose_data[3], pose_data[2], pose_data[5], pose_data[4]]
    #print("Pose Data:", pose_data)
    if len(hand_list) == 0:
        Right_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]
        Left_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]
    elif len(hand_list) == 1:
        if hand_list[0] == "Left":
            Left_Hand_Data = hand_data[:21]
            Right_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]
        if hand_list[0] == "Right":
            Right_Hand_Data = hand_data[:21]
            Left_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]
    else:# len(hand_list) == 2:
        if hand_list[0] == "Left":
            if hand_data is not None:
                Left_Hand_Data = hand_data[:21]
                Right_Hand_Data = hand_data[21:]
            else:
                Right_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]
                Left_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]
        elif hand_list[0] == "Right":
            if hand_data is not None:
                Right_Hand_Data = hand_data[:21]
                Left_Hand_Data = hand_data[21:]
            else:
                Right_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]
                Left_Hand_Data = [[0.0, 0.0, 0.0] for _ in range(21)]

    Translation_Vector_Left = np.array(pose_data[4])
    Translation_Vector_Right = np.array(pose_data[5])
    New_Left_Hand = [list(np.array(i)+Translation_Vector_Left) for i in Left_Hand_Data]
    New_Right_Hand = [list(np.array(i)+Translation_Vector_Right) for i in Right_Hand_Data]
    Upper_Body = pose_data + New_Left_Hand + New_Right_Hand

    return Upper_Body

def main_process(results_pose, results_hands):
    """
    This function will execute all three functions i.e. 1, 1.5, 2.
    :param results_pose: Estimation result by mediapipe for pose
    :param results_hands: Estimation by mediapipe for hands
    :return:
    """
    hand_world = take_coordinates_hands(results_hands.multi_hand_world_landmarks)
    pose_world = take_coordinates_pose(results_pose.pose_world_landmarks)
    new_hand = []
    hand_list = []
    if results_hands.multi_hand_landmarks:
        new_hand = equation_1(hand_world)
        #print(f"Before::{hand_world}")
        #print(f"After::{new_hand}")
        hand_list = []
        for hand_class in results_hands.multi_handedness:
            for abc in hand_class.classification:
                hand_list.append(abc.label)
        #print(hand_list)
    new_pose = equation_1_5(pose_world)
    combined = equation_2(new_pose, new_hand, hand_list)

    upper_plot.plot_connections(np.array(combined))


    print(len(combined), combined)
    return combined



# For webcam input or video input:
video = ''
cap = cv2.VideoCapture(0)
counter = 0
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break
            counter += 1
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)#for video
            image.flags.writeable = False
            results_hands = hands.process(image)

            # Then process the same image with the MediaPipe Pose Estimation.
            results_pose = pose.process(image)

            # this function will run all required functions
            if results_hands.multi_hand_landmarks or results_pose.pose_landmarks:
                main_process(results_pose, results_hands)

            # Draw the hand tracking annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Draw the pose estimation annotations on the image.
            if results_pose.pose_landmarks:
                mp_drawing.draw_landmarks(image, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.imshow('MediaPipe Hands and Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
cap.release()


