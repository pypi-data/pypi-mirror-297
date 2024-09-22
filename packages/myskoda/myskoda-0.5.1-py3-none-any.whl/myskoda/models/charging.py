"""Models for responses of api/v1/charging endpoint."""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field

from .common import ActiveState, EnabledState


class ChargingErrorType(StrEnum):
    CARE_MODE_IS_NOT_AVAILABLE = "CARE_MODE_IS_NOT_AVAILABLE"
    AUTO_UNLOCK_IS_NOT_AVAILABLE = "AUTO_UNLOCK_IS_NOT_AVAILABLE"
    MAX_CHARGE_CURRENT_IS_NOT_AVAILABLE = "MAX_CHARGE_CURRENT_IS_NOT_AVAILABLE"
    CHARGE_LIMIT_IS_NOT_AVAILABLE = "CHARGE_LIMIT_IS_NOT_AVAILABLE"
    STATUS_OF_CHARGING_NOT_AVAILABLE = "STATUS_OF_CHARGING_NOT_AVAILABLE"
    STATUS_OF_CONNECTION_NOT_AVAILABLE = "STATUS_OF_CONNECTION_NOT_AVAILABLE"


class ChargingError(BaseModel):
    type: ChargingErrorType
    description: str


class ChargeMode(StrEnum):
    HOME_STORAGE_CHARGING = "HOME_STORAGE_CHARGING"
    IMMEDIATE_DISCHARGING = "IMMEDIATE_DISCHARGING"
    ONLY_OWN_CURRENT = "ONLY_OWN_CURRENT"
    PREFERRED_CHARGING_TIMES = "PREFERRED_CHARGING_TIMES"
    TIMER_CHARGING_WITH_CLIMATISATION = "TIMER_CHARGING_WITH_CLIMATISATION"
    TIMER = "TIMER"
    MANUAL = "MANUAL"
    OFF = "OFF"


class MaxChargeCurrent(StrEnum):
    MAXIMUM = "MAXIMUM"
    REDUCED = "REDUCED"


class ChargingState(StrEnum):
    READY_FOR_CHARGING = "READY_FOR_CHARGING"
    CONNECT_CABLE = "CONNECT_CABLE"
    CONSERVING = "CONSERVING"
    CHARGING = "CHARGING"


class ChargeType(StrEnum):
    AC = "AC"
    DC = "DC"


class PlugUnlockMode(StrEnum):
    PERMANENT = "PERMANENT"
    ON = "ON"
    OFF = "OFF"


class Settings(BaseModel):
    available_charge_modes: list[ChargeMode] = Field(None, alias="availableChargeModes")
    battery_support: EnabledState = Field(None, alias="batterySupport")
    charging_care_mode: ActiveState = Field(None, alias="chargingCareMode")
    max_charge_current_ac: MaxChargeCurrent = Field(None, alias="maxChargeCurrentAc")
    preferred_charge_mode: ChargeMode = Field(None, alias="preferredChargeMode")
    target_state_of_charge_in_percent: int = Field(None, alias="targetStateOfChargeInPercent")
    auto_unlock_plug_when_charged: PlugUnlockMode = Field(None, alias="autoUnlockPlugWhenCharged")


class Battery(BaseModel):
    remaining_cruising_range_in_meters: int = Field(None, alias="remainingCruisingRangeInMeters")
    state_of_charge_in_percent: int = Field(None, alias="stateOfChargeInPercent")


class ChargingStatus(BaseModel):
    battery: Battery
    charge_power_in_kw: float | None = Field(None, alias="chargePowerInKw")
    charging_rate_in_kilometers_per_hour: float = Field(
        None, alias="chargingRateInKilometersPerHour"
    )
    remaining_time_to_fully_charged_in_minutes: int = Field(
        None, alias="remainingTimeToFullyChargedInMinutes"
    )
    charge_type: ChargeType | None = Field(None, alias="chargeType")
    state: ChargingState


class Charging(BaseModel):
    """Information related to charging an EV."""

    car_captured_timestamp: datetime = Field(None, alias="carCapturedTimestamp")
    errors: list[ChargingError]
    is_vehicle_in_saved_location: bool = Field(None, alias="isVehicleInSavedLocation")
    settings: Settings
    status: ChargingStatus | None
