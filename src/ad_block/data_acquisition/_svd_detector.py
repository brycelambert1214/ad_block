
import numpy as np
import cv2

class SVDChangeDetector:

    def __init__(self, history_size=30, threshold=0.075, max_dimension: int = 128,
        gaussian_kernel: tuple[int, int] = (5, 5),
        sigma: float = 0,
    ):
        self._max_dimension = max_dimension
        self._gaussian_kernel = gaussian_kernel
        self._sigma = sigma
        self._history = []
        self._history_size = history_size
        self._threshold = threshold

    def reset_history(self):
        self._history = []

    def detect(self, frame: np.ndarray) -> bool:
        spectrum = self._norm_spectrum(frame)

        if not self._history:
            self._history.append(spectrum)
            return False

        score = self._spectrum_distance(self._history[-1], spectrum)
        print(score)
        self._history.append(spectrum)

        if len(self._history) > self._history_size:
            self._history.pop(0)

        return score > self._threshold

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Convert a frame to a small, blurred grayscale image."""

        # Convert RGB/BGR image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Remove high-frequency detail/noise
        blurred = cv2.GaussianBlur(
            gray,
            self._gaussian_kernel,
            self._sigma,
        )

        # Preserve aspect ratio while reducing image size
        height, width = blurred.shape

        scale = self._max_dimension / max(height, width)

        if scale < 1:
            new_width = int(width * scale)
            new_height = int(height * scale)

            blurred = cv2.resize(
                blurred,
                (new_width, new_height),
                interpolation=cv2.INTER_AREA,
            )

        return blurred

    def _spectrum(self, frame: np.ndarray) -> np.ndarray:
        """Calculate the singular-value spectrum of a frame."""

        image = self._preprocess(frame)

        return np.linalg.svd(
            image,
            full_matrices=False,
            compute_uv=False,
        )

    def _norm_spectrum(self, frame: np.ndarray) -> np.ndarray:
        spec  = self._spectrum(frame)
        norm = np.linalg.norm(spec)
        return spec/norm

    def _spectrum_distance(
                    self,
                    previous: np.ndarray,
                    current: np.ndarray,
                ) -> float:

        return float(np.linalg.norm(current - previous))