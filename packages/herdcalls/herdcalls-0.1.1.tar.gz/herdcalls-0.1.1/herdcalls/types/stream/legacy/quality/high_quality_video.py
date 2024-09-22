from deprecation import deprecated

from .... import VideoQuality
from ....raw import VideoParameters


@deprecated(
    deprecated_in='1.0.0.dev6',
    details='Use herdcalls.types.VideoParameters.from_quality instead.',
)
class HighQualityVideo(VideoParameters):
    def __init__(self):
        super().__init__(*VideoQuality.HD_720p.value)
