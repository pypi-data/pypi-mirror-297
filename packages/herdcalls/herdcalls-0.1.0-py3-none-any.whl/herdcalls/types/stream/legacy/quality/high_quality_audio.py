from deprecation import deprecated

from .... import AudioQuality
from ....raw import AudioParameters


@deprecated(
    deprecated_in='1.0.0.dev6',
    details='Use herdcalls.types.AudioParameters.from_quality instead.',
)
class HighQualityAudio(AudioParameters):
    def __init__(self):
        super().__init__(*AudioQuality.HIGH.value)
