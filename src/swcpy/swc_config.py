import os 
from dotenv import load_dotenv

load_dotenv()

class SWCConfig:
    """Configuration class containing arguments for the SWC client."""

    swc_base_url: str
    swc_backoff: bool
    swc_backoff_max_time: int
    swc_bulk_file_format: str

    def __init__(self,swc_base_url:str = None,
                 backoff: bool = True,
                 backoff_max_time: int = 30,
                 bulk_file_format:str = "csv",
    ):
        """Constructor for config class."""
        self.swc_base_url = swc_base_url
        self.swc_backoff = backoff
        self.swc_backoff_max_time = backoff_max_time
        self.swc_bulk_file_format = bulk_file_format

    def __str__(self):
        """String representation of the config object."""
        return f"{self.swc_base_url} {self.swc_backoff} {self.swc_backoff_max_time} {self.swc_bulk_file_format}"
    
