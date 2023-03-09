"""A utility class for managing audio files."""
# pylint: disable=import-error

import logging
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
from scipy.io import wavfile

logger = logging.getLogger(__name__)


class AudioManager:
    """A utility class for managing audio files."""

    def __init__(
        self,
        sample_rate: int = 44100,
        output_audio_path: str = "",
        soft_clip: bool = False,
    ):
        """Initialize the AudioManager instance."""
        self.audios_to_save: Dict[str, np.adarray] = {}
        self.sample_rate = sample_rate
        self.soft_clip = soft_clip
        self.output_audio_path = Path(output_audio_path)
        self.output_audio_path.mkdir(exist_ok=True, parents=True)

    def add_audios_to_save(self, file_name: str, waveform: np.ndarray) -> None:
        """Add a waveform to the list of audios to save.

        Args:
            file_name (str): The name of the track.
            waveform (np.ndarray): The track to save.
        """
        self.audios_to_save[file_name] = waveform.copy()

    def save_audios(self) -> None:
        """Save the audios to the given path.

        Args:
            output_audio_path (str): The path to save the audios to.
        """
        for file_name, waveform in self.audios_to_save.items():
            self._save_audio(file_name, waveform)

    def _save_audio(self, file_name: str, waveform: np.ndarray) -> None:
        """Save the audio to the given path.
        It always save in Int16 format.

        Args:
            file_name (str): The name of the track.
            waveform (np.ndarray): The track to save.
            output_audio_path (str): The path to save the audio to.
            sample_rate (int): The sample rate of the audio.
        """
        logger.info(f"Saving {file_name}.wav to {self.output_audio_path}")
        waveform = waveform.T if waveform.shape[0] == 2 else waveform

        n_clipped, waveform = self.clip_audio(-1.0, 1.0, waveform)
        if n_clipped > 0:
            logger.warning(f"Writing {file_name}: {n_clipped} samples clipped")

        waveform = (32768.0 * waveform).astype(np.int16)

        wavfile.write(
            self.output_audio_path / f"{file_name}.wav",
            self.sample_rate,
            waveform,
        )

    def clip_audio(
        self, min_val: float, max_val: float, signal: np.ndarray
    ) -> Tuple[int, np.ndarray]:
        """Clip a WAV file to the given range.

        Args:
            min_val (float): The minimum value to clip to.
            max_val (float): The maximum value to clip to.
            signal (np.ndarray): The WAV file to clip.

        Returns:
            Tuple[int, np.ndarray]: The number of samples clipped and the clipped signal.
        """
        if self.soft_clip:
            signal = np.tanh(signal)
        n_clipped = np.sum(np.abs(signal) > 1.0)
        return int(n_clipped), np.clip(signal, min_val, max_val)
