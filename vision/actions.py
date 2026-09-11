import math
import time
from collections import deque

class ActionClassifier:
    """
    Classifies human actions from MediaPipe Pose landmarks (33 normalized landmarks).
    Expanded library of 10 distinct, highly accurate cinematic actions:
    1. ENTRY
    2. BOTH_HANDS_UP
    3. RAISING_HAND
    4. HANDS_ON_HEAD
    5. THINKING
    6. DRINKING_WATER
    7. HAND_ON_HEART
    8. STANDING_UP
    9. SITTING_DOWN
    10. EXIT
    """

    def __init__(self):
        self.has_entered = False
        self.entry_locked_until = 0.0
        self.last_seen_time = 0.0
        self.absence_start_time = 0.0
        self.history = deque(maxlen=20)

    def _calc_dist(self, p1, p2):
        return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)

    def _calc_angle(self, a, b, c):
        """Calculates angle in degrees at vertex point b."""
        radians = math.atan2(c['y'] - b['y'], c['x'] - b['x']) - math.atan2(a['y'] - b['y'], a['x'] - b['x'])
        angle = abs(radians * 180.0 / math.pi)
        if angle > 180.0:
            angle = 360.0 - angle
        return angle

    def classify(self, landmarks):
        now = time.time()

        # -------------------------------------------------------------
        # 1. NO POSE DETECTED (Nobody in frame -> EXIT)
        # -------------------------------------------------------------
        if not landmarks or len(landmarks) < 33:
            if self.absence_start_time == 0.0:
                self.absence_start_time = now

            absence_duration = now - self.absence_start_time

            # When nobody is in frame: immediate EXIT!
            if absence_duration >= 0.25:
                return "EXIT", 0.98, {"reason": "nobody_in_frame", "absence": round(absence_duration, 2)}
            else:
                return "EXIT", 0.90, {"status": "frame_absent"}

        # -------------------------------------------------------------
        # 2. POSE DETECTED
        # -------------------------------------------------------------
        was_absent = (self.absence_start_time > 0.0) and ((now - self.absence_start_time) >= 0.25)
        self.absence_start_time = 0.0
        self.last_seen_time = now

        # Extract landmarks
        nose = landmarks[0]
        mouth_l = landmarks[9]
        mouth_r = landmarks[10]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_elbow = landmarks[13]
        right_elbow = landmarks[14]
        left_wrist = landmarks[15]
        right_wrist = landmarks[16]

        mouth_center_x = (mouth_l['x'] + mouth_r['x']) / 2.0
        mouth_center_y = (mouth_l['y'] + mouth_r['y']) / 2.0
        mouth_center = {'x': mouth_center_x, 'y': mouth_center_y}

        mid_shoulder_x = (left_shoulder['x'] + right_shoulder['x']) / 2.0
        mid_shoulder_y = (left_shoulder['y'] + right_shoulder['y']) / 2.0
        shoulder_width = max(0.12, self._calc_dist(left_shoulder, right_shoulder))

        # Check boundary cutoff (walking off camera sides)
        if mid_shoulder_x < 0.05 or mid_shoulder_x > 0.95 or mid_shoulder_y > 0.95:
            return "EXIT", 0.92, {"reason": "boundary_cutoff"}

        # -------------------------------------------------------------
        # 3. INITIAL ENTRY & RE-ENTRY
        # -------------------------------------------------------------
        if not self.has_entered:
            self.has_entered = True
            self.entry_locked_until = now + 6.0
            return "ENTRY", 0.99, {"reason": "initial_movie_entry"}

        if was_absent:
            self.entry_locked_until = now + 6.0
            return "ENTRY", 0.95, {"reason": "re_entry"}

        # Geometry metrics
        dist_l_mouth = self._calc_dist(left_wrist, mouth_center)
        dist_r_mouth = self._calc_dist(right_wrist, mouth_center)
        left_elbow_angle = self._calc_angle(left_shoulder, left_elbow, left_wrist)
        right_elbow_angle = self._calc_angle(right_shoulder, right_elbow, right_wrist)

        # Hand elevation check (wrist higher than elbow and above shoulder or top of frame)
        r_hand_up = (right_wrist['y'] < right_shoulder['y'] - 0.04 and right_wrist['y'] < right_elbow['y'] - 0.03) or (right_wrist['y'] < 0.14)
        l_hand_up = (left_wrist['y'] < left_shoulder['y'] - 0.04 and left_wrist['y'] < left_elbow['y'] - 0.03) or (left_wrist['y'] < 0.14)

        # -------------------------------------------------------------
        # 4. BOTH HANDS UP vs HANDS ON HEAD
        # -------------------------------------------------------------
        if r_hand_up and l_hand_up:
            l_on_head = (abs(left_wrist['x'] - nose['x']) < 0.22) and (abs(left_wrist['y'] - nose['y']) < 0.16)
            r_on_head = (abs(right_wrist['x'] - nose['x']) < 0.22) and (abs(right_wrist['y'] - nose['y']) < 0.16)
            if l_on_head and r_on_head:
                return "HANDS_ON_HEAD", 0.95, {"gesture": "shock"}
            return "BOTH_HANDS_UP", 0.96, {"gesture": "victory"}

        # -------------------------------------------------------------
        # 5. DRINKING WATER (Direct mouth contact, bent elbow)
        # -------------------------------------------------------------
        r_drinking = (
            (mouth_center_y - 0.06 <= right_wrist['y'] <= mouth_center_y + 0.035) and
            (abs(right_wrist['x'] - mouth_center_x) < 0.08) and
            (right_elbow_angle < 115)
        )
        l_drinking = (
            (mouth_center_y - 0.06 <= left_wrist['y'] <= mouth_center_y + 0.035) and
            (abs(left_wrist['x'] - mouth_center_x) < 0.08) and
            (left_elbow_angle < 115)
        )
        if r_drinking or l_drinking:
            return "DRINKING_WATER", 0.94, {"dist_to_mouth": round(min(dist_l_mouth, dist_r_mouth), 3)}

        # -------------------------------------------------------------
        # 6. THINKING (Hand resting on chin / jawline / cheek)
        # -------------------------------------------------------------
        r_thinking = (
            (not r_drinking) and
            (abs(right_wrist['x'] - mouth_center_x) < 0.18) and
            (mouth_center_y - 0.03 <= right_wrist['y'] <= mouth_center_y + 0.08) and
            (right_wrist['y'] < right_elbow['y'] - 0.03) and
            (right_elbow_angle < 130) and
            (dist_r_mouth < 0.15)
        )
        l_thinking = (
            (not l_drinking) and
            (abs(left_wrist['x'] - mouth_center_x) < 0.18) and
            (mouth_center_y - 0.03 <= left_wrist['y'] <= mouth_center_y + 0.08) and
            (left_wrist['y'] < left_elbow['y'] - 0.03) and
            (left_elbow_angle < 130) and
            (dist_l_mouth < 0.15)
        )
        if r_thinking or l_thinking:
            return "THINKING", 0.94, {"gesture": "the_thinker"}

        # -------------------------------------------------------------
        # 7. RAISING HAND (Single hand reach - Spider-Man)
        # -------------------------------------------------------------
        if (r_hand_up and not l_hand_up) or (l_hand_up and not r_hand_up):
            return "RAISING_HAND", 0.95, {"hand": "right" if r_hand_up else "left"}

        # -------------------------------------------------------------
        # 8. GUARANTEED ENTRY LOCK
        # Preserves ENTRY during entrance unless user performs an active gesture
        # -------------------------------------------------------------
        if now < self.entry_locked_until:
            return "ENTRY", 0.96, {"remaining_entry": round(self.entry_locked_until - now, 1)}

        # -------------------------------------------------------------
        # 9. HAND ON HEART (Hand placed deliberately over upper chest)
        # -------------------------------------------------------------
        r_heart = (
            (right_wrist['y'] > mouth_center_y + 0.12) and
            (right_wrist['y'] < right_elbow['y'] - 0.03) and
            (left_shoulder['y'] <= right_wrist['y'] <= left_shoulder['y'] + 0.22) and
            (abs(right_wrist['x'] - mid_shoulder_x) < 0.12) and
            (right_elbow_angle < 100)
        )
        l_heart = (
            (left_wrist['y'] > mouth_center_y + 0.12) and
            (left_wrist['y'] < left_elbow['y'] - 0.03) and
            (left_shoulder['y'] <= left_wrist['y'] <= left_shoulder['y'] + 0.22) and
            (abs(left_wrist['x'] - mid_shoulder_x) < 0.12) and
            (left_elbow_angle < 100)
        )
        if r_heart or l_heart:
            return "HAND_ON_HEART", 0.91, {"gesture": "allegiance"}

        # -------------------------------------------------------------
        # 10. STANDING UP (Tall vertical posture in camera)
        # -------------------------------------------------------------
        if mid_shoulder_y < 0.40 and nose['y'] < 0.27:
            return "STANDING_UP", 0.90, {"posture": "standing"}

        # -------------------------------------------------------------
        # 11. SITTING DOWN (Default relaxed seated posture)
        # -------------------------------------------------------------
        return "SITTING_DOWN", 0.88, {
            "shoulder_y": round(mid_shoulder_y, 2),
            "nose_y": round(nose['y'], 2),
            "posture": "seated"
        }
