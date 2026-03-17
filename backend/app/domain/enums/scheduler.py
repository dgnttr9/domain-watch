from enum import StrEnum


class SchedulerPreset(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class SchedulerType(StrEnum):
    PRESET = "preset"
    CUSTOM = "custom"
