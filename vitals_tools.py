"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return a list of the systolic value from every encounter, repeat visits included."""
    readings = []
    for encounter in encounters:
        readings.append(encounter["systolic"])
    return readings


def mean_systolic(readings):
    """Return the mean of the readings, or None if the list is empty."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return how many distinct patient IDs appear in the encounters."""
    patient_ids = set()
    for encounter in encounters:
        patient_ids.add(encounter["patient_id"])
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return the sorted patient IDs with at least one reading at or above cutoff, each listed once."""
    patient_ids = set()
    for encounter in encounters:
        if encounter["systolic"] >= cutoff:
            patient_ids.add(encounter["patient_id"])
    return sorted(patient_ids)
