import requests
import os
import re
import datetime
from tqdm import tqdm
from timezonefinder import TimezoneFinder
from zoneinfo import ZoneInfo


class Pyranocam:
    def __init__(self, api_key):
        self.base_url = "http://wematics.cloud"
        self.api_key = api_key
        self.tf = TimezoneFinder()

    def _make_request(self, endpoint: str, params=None):
        """Makes a request to the API with error handling."""
        url = f"{self.base_url}{endpoint}"
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = requests.get(url, params=params)

        # Raise an exception for bad status codes
        response.raise_for_status()
        return response.json()

    def list_cameras(self):
        """Lists all available cameras."""
        return self._make_request("/cameras")

    def list_variables(self, camera):
        """Lists all available variables for a given camera."""
        return self._make_request(f"/{camera}/variables")

    def list_dates(self, camera, variable):
        """Lists all available dates for a given camera and variable."""
        return self._make_request(f"/{camera}/dates/{variable}")

    def _local_to_utc(self, local_dt, lat, lon):
        """Convert local datetime to UTC based on lat/lon."""
        timezone_str = self.tf.timezone_at(lat=lat, lng=lon)
        local_tz = ZoneInfo(timezone_str)
        utc_dt = local_dt.replace(tzinfo=local_tz).astimezone(ZoneInfo("UTC"))
        return utc_dt

    def _utc_to_local(self, utc_dt, lat, lon):
        """Convert UTC datetime to local time based on lat/lon."""
        timezone_str = self.tf.timezone_at(lat=lat, lng=lon)
        local_tz = ZoneInfo(timezone_str)
        local_dt = utc_dt.replace(tzinfo=ZoneInfo("UTC")).astimezone(local_tz)
        return local_dt
    
    def download_csv_file(self, camera, variable, file_name, download_path=""):
        """Downloads a single CSV file."""
        timestamp_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
        date = timestamp_pattern.search(file_name).group()
        url = f"{self.base_url}/{camera}/download/{variable}/{date}/{file_name}"
        print(url)
        self._download_file(url, os.path.basename(file_name), download_path)

    def _download_file(self, url, file_name, download_path=""):
        """Downloads a file from a given URL (helper function)."""
        params = {'api_key': self.api_key}
        response = requests.get(url, params=params, stream=True)

        if response.status_code == 200:
            file_path = os.path.join(download_path, file_name)
            total_size = int(response.headers.get('content-length', 0))

            with open(file_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=4096), 
                                total=total_size // 4096, 
                                unit='KB', 
                                desc=f"Downloading {file_name}"):
                    if chunk:
                        f.write(chunk)
        else:
            print(f"Error downloading {file_name}: {response.text}")

    def list_files(self, camera, variable, date, use_utc=False, lat=None, lon=None):
        """Lists all available files for a given camera, variable, and date."""
        if use_utc:
            if lat is None or lon is None:
                raise ValueError("Latitude and longitude are required for UTC conversion")
            
            # Convert UTC date to local date range
            utc_start = datetime.datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=ZoneInfo("UTC"))
            utc_end = utc_start + datetime.timedelta(days=1)
            
            timezone_str = self.tf.timezone_at(lat=lat, lng=lon)
            local_tz = ZoneInfo(timezone_str)
            
            local_start = utc_start.astimezone(local_tz)
            local_end = utc_end.astimezone(local_tz)

            all_files = []
            current_date = local_start.date()
            while current_date <= local_end.date():
                date_str = current_date.strftime("%Y-%m-%d")
                files = self._make_request(f"/{camera}/files/{variable}/{date_str}")['files']
                all_files.extend(files)
                current_date += datetime.timedelta(days=1)

            utc_files = []
            for file_name in all_files:
                timestamp_match = re.search(r"(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2})", file_name)
                if timestamp_match:
                    local_dt = datetime.datetime.strptime(timestamp_match.group(1), "%Y-%m-%d_%H_%M_%S")
                    local_dt = local_dt.replace(tzinfo=local_tz)
                    utc_dt = local_dt.astimezone(ZoneInfo("UTC"))
                    if utc_start <= utc_dt < utc_end:
                        utc_file_name = file_name.replace(timestamp_match.group(1), utc_dt.strftime("%Y-%m-%d_%H_%M_%S"))
                        utc_files.append(utc_file_name)
            return utc_files
        else:
            return self._make_request(f"/{camera}/files/{variable}/{date}")['files']

    def download_image(self, camera, variable, file_name, download_path="", use_utc=False, lat=None, lon=None):
        """Downloads a single JPG file."""
        if use_utc:
            if lat is None or lon is None:
                raise ValueError("Latitude and longitude are required for UTC conversion")
            
            # Extract datetime and suffix from the file name
            match = re.match(r"(\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2})(_[^.]+)?\.(\w+)", file_name)
            if not match:
                raise ValueError(f"Invalid file name format: {file_name}")
            
            datetime_str, suffix, extension = match.groups()
            suffix = suffix or ""  # If no suffix, use an empty string
            
            utc_dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%d_%H_%M_%S").replace(tzinfo=ZoneInfo("UTC"))
            timezone_str = self.tf.timezone_at(lat=lat, lng=lon)
            local_tz = ZoneInfo(timezone_str)
            local_dt = utc_dt.astimezone(local_tz)
            local_file_name = local_dt.strftime(f"%Y-%m-%d_%H_%M_%S{suffix}.{extension}")
            date = local_dt.strftime("%Y-%m-%d")
        else:
            local_file_name = file_name
            date = file_name.split('_')[0]

        url = f"{self.base_url}/{camera}/download/{variable}/{date}/{local_file_name}"
        self._download_file(url, file_name, download_path)

    def download_images_in_range(self, camera, variable, start_datetime, end_datetime, download_path=".", use_utc=False, lat=None, lon=None):
        """Downloads files for a camera and variable within a datetime range with a progress bar."""
        start_datetime = datetime.datetime.strptime(start_datetime, "%Y-%m-%d_%H_%M_%S")
        end_datetime = datetime.datetime.strptime(end_datetime, "%Y-%m-%d_%H_%M_%S")

        if use_utc:
            if lat is None or lon is None:
                raise ValueError("Latitude and longitude are required for UTC conversion")
            
            start_datetime = start_datetime.replace(tzinfo=ZoneInfo("UTC"))
            end_datetime = end_datetime.replace(tzinfo=ZoneInfo("UTC"))
            
            timezone_str = self.tf.timezone_at(lat=lat, lng=lon)
            local_tz = ZoneInfo(timezone_str)
            
            local_start = start_datetime.astimezone(local_tz)
            local_end = end_datetime.astimezone(local_tz)
        else:
            local_start, local_end = start_datetime, end_datetime

        all_files = []
        current_date = local_start.date()
        while current_date <= local_end.date():
            date_str = current_date.strftime("%Y-%m-%d")
            files = self.list_files(camera, variable, date_str, use_utc, lat, lon)
            all_files.extend(files)
            current_date += datetime.timedelta(days=1)

        filtered_files = []
        timestamp_pattern = re.compile(r"\d{4}-\d{2}-\d{2}_\d{2}_\d{2}_\d{2}")
        for file_name in all_files:
            match = timestamp_pattern.search(file_name)
            if match:
                file_timestamp = match.group()
                file_datetime = datetime.datetime.strptime(file_timestamp, "%Y-%m-%d_%H_%M_%S")
                if use_utc:
                    file_datetime = file_datetime.replace(tzinfo=ZoneInfo("UTC"))
                if start_datetime <= file_datetime < end_datetime:
                    filtered_files.append(file_name)

        for file_name in tqdm(filtered_files, desc="Downloading", unit="file"):
            self.download_image(camera, variable, file_name, download_path, use_utc, lat, lon)