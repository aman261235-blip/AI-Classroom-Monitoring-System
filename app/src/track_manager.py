import time


class TrackManager:

    def __init__(self):
        self.tracks = {}

    def has_track(self, track_id):
        return track_id in self.tracks

    def add_track(self, track_id, name="Unknown", recognized=False):

        self.tracks[track_id] = {
            "name": name,
            "recognized": recognized,
            "last_seen": time.time()
        }

    def update_track(self, track_id):

        if track_id in self.tracks:
            self.tracks[track_id]["last_seen"] = time.time()

    def recognize_track(self, track_id, name):

        if track_id in self.tracks:

            self.tracks[track_id]["name"] = name
            self.tracks[track_id]["recognized"] = True
            self.tracks[track_id]["last_seen"] = time.time()

    def is_recognized(self, track_id):

        if track_id not in self.tracks:
            return False

        return self.tracks[track_id]["recognized"]

    def get_name(self, track_id):

        if track_id not in self.tracks:
            return "Unknown"

        return self.tracks[track_id]["name"]

    def cleanup(self, timeout=5):

        current = time.time()

        remove = []

        for track_id, data in self.tracks.items():

            if current - data["last_seen"] > timeout:
                remove.append(track_id)

        for track_id in remove:
            del self.tracks[track_id]