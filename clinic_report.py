#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")

LOWEST_VALID = 60
HIGHEST_VALID = 250

CUTOFF = 140
REASON = (
    "140 mmHg is the stage 2 hypertension threshold, so the limited call-back "
    "slots go to patients most likely to need a treatment change."
)

def read_encounters(data_path):
    """Read the CSV and return (usable encounters, number of skipped rows).

    One usable encounter is a dictionary with "patient_id", "visit_date",
    and "systolic" (an int from 60 to 250 mmHg).
    """
    lines = data_path.read_text(encoding="utf-8").splitlines()
    encounters = []
    skipped = 0

    for line in lines[1:]:  # skip the header line
        if line.strip() == "":
            print("Skipping a blank row.")
            skipped += 1
            continue

        fields = line.split(",")
        if len(fields) != 3:
            print(f"Skipping {line!r}: expected 3 fields, found {len(fields)}.")
            skipped += 1
            continue

        patient_id, visit_date, reading = fields
        try:
            systolic = int(reading)
        except ValueError:
            print(f"Skipping {line!r}: systolic is not a whole number.")
            skipped += 1
            continue

        if systolic < LOWEST_VALID or systolic > HIGHEST_VALID:
            print(f"Skipping {line!r}: {systolic} is outside 60-250 mmHg.")
            skipped += 1
            continue

        encounters.append(
            {"patient_id": patient_id, "visit_date": visit_date, "systolic": systolic}
        )

    return encounters, skipped



def main():
    """Write output/vitals_report.txt (six summary lines) and
    output/followup_list.txt (cutoff, reason, and patient IDs to call back)."""
    encounters, skipped = read_encounters(DATA_PATH)
    readings = systolic_readings(encounters)
    OUTPUT_DIR.mkdir(exist_ok=True)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.2f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]
    report_path = OUTPUT_DIR / "vitals_report.txt"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print("\nSaved vitals_report.txt:")
    print(report_path.read_text(encoding="utf-8"))

    followup_lines = [f"Cutoff: {CUTOFF} mmHg", f"Reason: {REASON}"]
    followup_lines += patients_at_or_above(encounters, CUTOFF)
    followup_path = OUTPUT_DIR / "followup_list.txt"
    followup_path.write_text("\n".join(followup_lines) + "\n", encoding="utf-8")

    print("Saved followup_list.txt:")
    print(followup_path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
