from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple


class DriverState(Enum):
    """Enum for driver state."""

    CONNECTED = 1
    DISCONNECTED = 0


class DriverDeviceOrientation(Enum):
    """Enum for screen orientation."""

    PORTRAIT = 0
    LANDSCAPE = 1
    REVERSE_PORTRAIT = 2
    REVERSE_LANDSCAPE = 3


class DriverError(Exception):
    pass


class DriverConnectionError(DriverError):
    pass


class DriverRetryError(DriverError):
    pass


class DriverCommandError(DriverError):
    pass


class DriverServerError(DriverError):
    pass


class DriverPushError(DriverError):
    pass


class DriverForwardError(DriverError):
    pass


class DriverReleasePortError(DriverError):
    pass


class DriverResolutionError(DriverError):
    pass


class DriverAdapter(ABC):
    """Interface for driver to interact with Android device."""

    state = DriverState.DISCONNECTED
    serial: str

    @abstractmethod
    def connect(self) -> None:
        """Connect to Android device."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from Android device."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, command: str) -> Tuple[str, int]:
        """Execute shell command on Android device.

        Args:
            command (str): Command to execute.

        Returns:
            Output of command and exit code.
        """
        raise NotImplementedError

    @abstractmethod
    def run_daemon(self, command: str) -> int:
        """Run daemon on Android device.

        Args:
            command (str): Command to execute as daemon.

        Returns:
            int: pid of daemon.
        """
        raise NotImplementedError

    @abstractmethod
    def push(self, src: str, dst: str) -> None:
        """Push file to Android device.

        Args:
            src (str): Path to file on local machine.
            dst (str): Path to file on Android device.
        """
        raise NotImplementedError

    @abstractmethod
    def forward(self, remote: int, local: Optional[int] = None) -> int:
        """Forward port from Android device to local machine.
        Reuse existing local port if specified.

        Args:
            remote (int): Port to forward from Android device.
            local (Optional[int], optional): Port to forward to on local machine. Defaults to None.

        Returns:
            int: Port on local machine.
        """
        raise NotImplementedError

    @abstractmethod
    def release_port(self, local: int) -> bool:
        """Release forwarded port on local machine.

        Args:
            local (int): Port on local machine.
        """
        raise NotImplementedError

    @abstractmethod
    def get_device_resolution(self) -> Tuple[int, int]:
        """Get device resolution.

        Returns:
            Tuple[int, int]: Device resolution. Width, height.
        """
        raise NotImplementedError

    @abstractmethod
    def get_device_orientation(self) -> DriverDeviceOrientation:
        raise NotImplementedError
