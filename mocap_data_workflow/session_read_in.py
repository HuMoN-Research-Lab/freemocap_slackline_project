from pathlib import Path

class FreemocapSession:
    def __init__(self, session_id: str, freemocap_data_folder_path: Path) -> dict:
        self.session_id = session_id
        self.freemocap_data_folder_path = freemocap_data_folder_path

        # check if dictionary exists in session folder
        # if dictionary exists, load it and set it to self.path_dict
        # if dictionary doesn't exist, run construct_path_dict

    def construct_path_dict(self,):    
        self.path_dict = {}
        self.path_dict["session_id"] = self.session_id
        self.path_dict["freemocap_data_folder"] = self.freemocap_data_folder_path
        self.path_dict["session_folder"] = self.freemocap_data_folder_path / self.session_id
        self.path_dict["data_arrays_folder"] = self.path_dict["session_folder"] / "DataArrays"
        self.path_dict["synced_videos_folder"] = self.path_dict["session_folder"] / "SyncedVideos"
        self.path_dict["mediapipe_blender_rotated"] = self.path_dict["data_arrays_folder"] / "mediaPipeSkel_3d_filtered.npy"
        self.path_dict["total_body_COM_frame_xyz"] = self.path_dict["data_arrays_folder"] / "totalBodyCOM_frame_XYZ.npy"
        self.path_dict["segment_COM_frame_xyz"] = self.path_dict["data_arrays_folder"] / "segmentedCOM_frame_joint_XYZ.npy"


def main():
    session_id = "4stepsequence_session5_10_5_22"
    freemocap_data_folder_path = Path("/Users/philipqueen/Documents/Humon Research Lab/FreeMocap_Data")
    session_info = FreemocapSession(session_id, freemocap_data_folder_path)
    print(type(session_info.dict["data_arrays"]))

if __name__ == "__main__":
    main()