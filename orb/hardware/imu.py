"""
MPU6050 IMU for orientation sensing.
Used to detect if the ball is upright, tilted, or being picked up.
"""
import logging
import math
from ..utils.config import get

logger = logging.getLogger("orb.hardware")

try:
    import smbus2
    HAS_SMBUS = True
except ImportError:
    HAS_SMBUS = False


class IMU:
    # MPU6050 registers
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT_H = 0x3B

    def __init__(self):
        self.address = get("imu.i2c_address", 0x68)
        self._bus = None

    def setup(self):
        if not HAS_SMBUS:
            logger.info("IMU: simulation mode")
            return
        try:
            self._bus = smbus2.SMBus(1)
            self._bus.write_byte_data(self.address, self.PWR_MGMT_1, 0)  # Wake up
            logger.info(f"IMU initialized at 0x{self.address:02X}")
        except Exception as e:
            logger.warning(f"IMU init failed: {e}")
            self._bus = None

    def read_accel(self) -> tuple:
        """Read accelerometer (x, y, z) in g units."""
        if not self._bus:
            return (0.0, 0.0, 1.0)  # Simulated: upright

        try:
            data = self._bus.read_i2c_block_data(self.address, self.ACCEL_XOUT_H, 6)
            ax = self._to_signed(data[0] << 8 | data[1]) / 16384.0
            ay = self._to_signed(data[2] << 8 | data[3]) / 16384.0
            az = self._to_signed(data[4] << 8 | data[5]) / 16384.0
            return (ax, ay, az)
        except Exception as e:
            logger.error(f"IMU read error: {e}")
            return (0.0, 0.0, 1.0)

    def get_tilt_angle(self) -> float:
        """Get tilt angle from vertical in degrees."""
        ax, ay, az = self.read_accel()
        # Angle from vertical (z-axis)
        magnitude = math.sqrt(ax**2 + ay**2 + az**2)
        if magnitude == 0:
            return 0.0
        return math.degrees(math.acos(min(abs(az) / magnitude, 1.0)))

    def is_picked_up(self) -> bool:
        """Detect if the ball is being held (sudden acceleration change)."""
        ax, ay, az = self.read_accel()
        magnitude = math.sqrt(ax**2 + ay**2 + az**2)
        # Normal gravity ≈ 1.0g; if significantly different, being moved
        return abs(magnitude - 1.0) > 0.5

    @staticmethod
    def _to_signed(val: int) -> int:
        return val - 65536 if val > 32767 else val

    def cleanup(self):
        if self._bus:
            self._bus.close()
