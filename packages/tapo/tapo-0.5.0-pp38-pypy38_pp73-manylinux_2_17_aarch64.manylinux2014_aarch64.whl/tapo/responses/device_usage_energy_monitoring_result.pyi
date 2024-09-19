from tapo.responses import UsageByPeriodResult

class DeviceUsageEnergyMonitoringResult:
    """Contains the time usage, the power consumption, and the energy savings of the device."""

    time_usage: UsageByPeriodResult
    """Time usage in minutes."""
    power_usage: UsageByPeriodResult
    """Power usage in watt-hour (Wh)."""
    saved_power: UsageByPeriodResult
    """Saved power in watt-hour (Wh)."""

    def to_dict(self) -> dict:
        """Gets all the properties of this result as a dictionary.

        Returns:
            dict: The result as a dictionary.
        """
