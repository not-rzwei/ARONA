from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple


class DriverState(Enum):
    """Enum for driver state."""

    CONNECTED = 1
    DISCONNECTED = 0


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


class DriverResolutionError(DriverError):
    pass


class IDriver(ABC):
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
    def get_device_resolution(self, landscape: bool = True) -> Tuple[int, int]:
        """Get device resolution.

        Args:
            landscape (bool, optional): Get resolution in landscape mode. Defaults to True.

        Returns:
            Tuple[int, int]: Device resolution. Width, height.
        """
        raise NotImplementedError
