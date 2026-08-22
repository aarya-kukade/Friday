

"""
Audio specific exceptions.
"""


class AudioError(Exception):
    """Base audio exception."""


class MicrophoneInitializationError(AudioError):
    """Raised when microphone initialization fails."""


class AudioStreamError(AudioError):
    """Raised when audio stream fails."""