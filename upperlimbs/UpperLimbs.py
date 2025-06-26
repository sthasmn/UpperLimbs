import cv2
import mediapipe as mp
import numpy as np
from . import upper_plot

class UpperLimbs:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.latest_coordinates = None
        self.results_pose = None
        self.results_hands = None

    # --- Your Original Functions (now internal methods) ---
    def _take_coordinates_pose(self, coordinates):
        if coordinates == None: return []
        keypoints = [[xyz.x, xyz.y, xyz.z] for xyz in coordinates.landmark]
        return keypoints

    def _take_coordinates_hands(self, coordinates):
        if coordinates == None: return []
        keypoints = []
        for data_point in coordinates:
            for xyz in data_point.landmark:
                keypoints.append([xyz.x, xyz.y, xyz.z])
        return keypoints

    def _equation_1(self, hand_points):
        if len(hand_points) == 21:
            Translation_Vector_1 = -np.array(hand_points[0])
            return [list(np.array(i) + Translation_Vector_1) for i in hand_points]
        elif len(hand_points) == 42:
            Translation_Vector_1 = -np.array(hand_points[0])
            New_points1 = [list(np.array(i) + Translation_Vector_1) for i in hand_points[:21]]
            Translation_Vector_2 = -np.array(hand_points[21])
            New_points2 = [list(np.array(i) + Translation_Vector_2) for i in hand_points[21:]]
            return New_points1 + New_points2
        return []

    def _equation_1_5(self, pose_data):
        Translation_Vector = -(np.array(pose_data[11]) + np.array(pose_data[12])) / 2
        return [list(np.array(i) + Translation_Vector) for i in pose_data]

    def _equation_2(self, pose_data, hand_data, hand_list):
        pose_data = pose_data[11:17]
        pose_data = [pose_data[1], pose_data[0], pose_data[3], pose_data[2], pose_data[5], pose_data[4]]
        Right_Hand_Data, Left_Hand_Data = ([[0.0]*3]*21, [[0.0]*3]*21)
        if len(hand_list) == 1:
            if hand_list[0] == "Left": Left_Hand_Data = hand_data[:21]
            if hand_list[0] == "Right": Right_Hand_Data = hand_data[:21]
        elif len(hand_list) == 2:
            if hand_data is not None:
                if hand_list[0] == "Left":
                    Left_Hand_Data, Right_Hand_Data = hand_data[:21], hand_data[21:]
                elif hand_list[0] == "Right":
                    Right_Hand_Data, Left_Hand_Data = hand_data[:21], hand_data[21:]
        Translation_Vector_Left = np.array(pose_data[4])
        Translation_Vector_Right = np.array(pose_data[5])
        New_Left_Hand = [list(np.array(i) + Translation_Vector_Left) for i in Left_Hand_Data]
        New_Right_Hand = [list(np.array(i) + Translation_Vector_Right) for i in Right_Hand_Data]
        return pose_data + New_Left_Hand + New_Right_Hand

    def _calculate_coordinates(self):
        hand_world = self._take_coordinates_hands(self.results_hands.multi_hand_world_landmarks)
        pose_world = self._take_coordinates_pose(self.results_pose.pose_world_landmarks)
        new_hand, hand_list = [], []
        if self.results_hands.multi_hand_landmarks:
            new_hand = self._equation_1(hand_world)
            hand_list = [c.classification[0].label for c in self.results_hands.multi_handedness]
        new_pose = self._equation_1_5(pose_world)
        combined = self._equation_2(new_pose, new_hand, hand_list)
        return combined

    # --- Public API Methods ---
    def process_frame(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_to_process = np.copy(image_rgb)
        self.results_hands = self.hands.process(image_to_process)
        self.results_pose = self.pose.process(image_to_process)
        if self.results_hands.multi_hand_landmarks or self.results_pose.pose_landmarks:
            self.latest_coordinates = self._calculate_coordinates()
        else:
            self.latest_coordinates = None
        return self.latest_coordinates

    def get_coordinates(self):
        return self.latest_coordinates

    def visualize(self):
        if self.latest_coordinates:
            upper_plot.plot_connections(np.array(self.latest_coordinates))

    def draw_landmarks(self, image):
        if self.results_hands and self.results_hands.multi_hand_landmarks:
            for hand_landmarks in self.results_hands.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        if self.results_pose and self.results_pose.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, self.results_pose.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        return image

    def close(self):
        self.hands.close()
        self.pose.close()