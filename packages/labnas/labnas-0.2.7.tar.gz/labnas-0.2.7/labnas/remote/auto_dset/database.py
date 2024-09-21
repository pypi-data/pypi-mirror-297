"""
Automatically create and maintain recording database.

TODO:
In separate script:
- find metadata for each tif
- extract tif metadata

In this script:
- get timestamps of tif and stim
- associate tif with stim

In eyetracking:
- get pupil positions, motion energy
"""

import os
from pathlib import Path

import pandas as pd

from labnas.remote.imaging import ImagingNas
from labnas.remote.auto_dset.utils import scan_multipage_tiffs, check_file_name_for_disqualifiers, check_file_name_with_list

ALLOWED_SESSIONS = [
    "flashes",
    "cfs",
    "conflict",
    "alternations",
    "ori",
]

LOCAL_DIR = Path("/home/mathis/Code/gitlab/labnas/data/temp")

class TwophotonDatabase:
    """Create and maintain recording database."""

    def __init__(
            self,
            raw_base: Path,
            processed_base: Path,
            target_base: Path,
            raw_nas: ImagingNas,
            processed_nas: ImagingNas,
    ) -> None:
        # params
        self.raw_base = raw_base
        self.processed_base = processed_base
        self.dset_base = target_base

        self.raw_nas = raw_nas
        self.processed_nas = processed_nas

        # other
        self.tif_files = []
        self.stim_types = []
        self.dset_names = []
        self.df = None

        #
        self.current = {}

    def run(self) -> None:
        """Main method to call."""
        self.find_recording_tifs()
        self.load_table()
        self.process_recordings()

    def find_recording_tifs(self) -> None:
        """Look for 2p recording tifs that could be the basis of a dataset"""
        print("Looking for multipage tiffs")
        tif_candidates = scan_multipage_tiffs(self.raw_base, self.raw_nas)
        print(f"TIFFs in multipage folders: {len(tif_candidates)}")
        selected = []
        stim_types = []
        for file in tif_candidates:
            file_name = file.name
            is_ok = check_file_name_for_disqualifiers(file_name)
            is_relevant, stim_type = check_file_name_with_list(file_name, ALLOWED_SESSIONS)
            if is_ok & is_relevant:
                selected.append(file)
                stim_types.append(stim_type)
        print(f"Selected TIFFs for auto-dset: {len(selected)}")
        self.tif_files = selected
        self.stim_types = stim_types

    def load_table(self) -> None:
        """Load the old database file."""
        csv_file = self.dset_base / "database.csv"
        if self.processed_nas.is_file(csv_file):
            local_copy = LOCAL_DIR / csv_file.name
            self.processed_nas.download_file(csv_file, local_copy, overwrite=True)
            self.df = pd.read_csv(local_copy)
            os.remove(local_copy)
            print(f"Entries in database: {self.df.shape[0]}")
        else:
            print("Could not load database file.")

    def process_recordings(self) -> None:
        """Iterate over all tifs."""
        for file, stim_type in zip(self.tif_files, self.stim_types):
            dset_name = self.get_recording_name(file, stim_type)
            print(f"---{dset_name}---")
            if self.df is not None:
                if dset_name in self.df["dset_name"].values:
                    print(f"{dset_name}: already in database")
            self.gather_recording_files(dset_name)

    def get_recording_name(self, tif_file: Path, stim_type: str) -> str:
        """Get a unique name for a recording."""
        count = 0
        mouse_name = tif_file.parts[3]
        date_string = tif_file.parts[4]
        short_date = date_string.replace("-", "")


        self.current["mouse"] = mouse_name
        self.current["date"] = date_string
        self.current["tif_stem"] = tif_file.stem

        dset_name = f"{short_date}_{mouse_name}_{stim_type}_{count}"
        if dset_name in self.dset_names:
            while dset_name in self.dset_names:
                count += 1
                dset_name = f"{short_date}_{mouse_name}_{stim_type}_{count}"
        self.dset_names.append(dset_name)
        self.current["dset_name"] = dset_name
        return dset_name

    def gather_recording_files(self, dset_name: str) -> None:
        """Check what files exist for a recording."""
        self.check_dset_folder(dset_name)
        self.gather_processed_files()
        self.check_raw_files()

    def check_dset_folder(self, dset_name: str) -> None:
        """Check whether dataset in database folder."""
        dset_folder = self.dset_base / dset_name
        if not self.processed_nas.is_dir(dset_folder):
            self.processed_nas.create_empty_folder(dset_folder)
        self.current["dset_folder"] = dset_folder

    def gather_processed_files(self) -> None:
        """Check whether database contains processed files for this recording."""
        try:
            self.gather_suite2p_files()
        except FileNotFoundError as e:
            print(f"Suite2p: {e}")

        try:
            self.check_stim()
        except FileNotFoundError as e:
            print(f"Stim: {e}")

    def gather_suite2p_files(self) -> None:
        """Check whether files related to ROI extraction exist."""
        # find files in source
        date_folder = self.processed_base / "suite2p" / self.current["mouse"] / self.current["date"]
        if not self.processed_nas.is_dir(date_folder):
            raise FileNotFoundError(f"{date_folder}")
        source_folder = date_folder / self.current["tif_stem"]
        if not self.processed_nas.is_dir(source_folder):
            raise FileNotFoundError(f"{source_folder}")
        print(f"Suite2p data found: {source_folder}")

        # check whether files are in database
        target_folder = self.current["dset_folder"] / "suite2p"
        if self.processed_nas.is_dir(target_folder):
            print(f"Suite2p data already in database: {target_folder}")
        else:
            print("Suite2p not in database yet.")
            self.processed_nas.copy



    def check_stim(self) -> None:
        """Check whether a table with stimulus information per 2p frame has been created."""
        date_folder = self.processed_base / "stim" / self.current_mouse / self.current_date
        if not self.processed_nas.is_dir(date_folder):
            raise FileNotFoundError(f"{date_folder}")

        target_folder = date_folder / self.current_tif_stem
        if not self.processed_nas.is_dir(target_folder):
            raise FileNotFoundError(f"{target_folder}")
        print(f"Stim: {target_folder}")

    def check_raw_files(self) -> None:
        pass