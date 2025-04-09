from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes.client import GetModule, CreateObject

# Initialize the required COM interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,  # Use the correct interface ID
    1, None
)

volume = interface.QueryInterface(IAudioEndpointVolume)
# To increase the volume by 10% (scaled)
def increase_volume(increment=0.1):
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + increment, 1.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

# To decrease the volume by 10% (scaled)
def decrease_volume(decrement=0.1):
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(current_volume - decrement, 0.0)
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def set_volume(set=0):
    volume.SetMasterVolumeLevelScalar(set, None)

def get_volume():
    return volume.GetMasterVolumeLevelScalar()
