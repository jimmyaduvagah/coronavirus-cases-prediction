def get_days(data):
    periodType = data["periodType"]
    assert periodType in ["days", "weeks", "months"]

    if periodType == "days":
        return data["timeToElapse"]
    elif periodType == "weeks":
        return data["timeToElapse"] * 7
    else:
        return data["timeToElapse"] * 30


def get_estimation_factor(data):
    days = get_days(data)
    return int(days / 3)


def get_infections_by_requested_time(data, estimate_type="impact"):
    assert estimate_type in ["impact", "severe"]
    multiplier = 10 if estimate_type == "impact" else 50

    currently_infected = data["reportedCases"] * multiplier
    factor = get_estimation_factor(data)
    infections_by_requested_time = currently_infected * pow(2, factor)
    return infections_by_requested_time


def get_severe_cases_by_requested_time(data, estimate_type="impact"):
    infections = get_infections_by_requested_time(data, estimate_type)
    severe_cases_by_requested_time = int(infections * 0.15)
    return severe_cases_by_requested_time


def get_hospital_beds_by_requested_time(data, estimate_type="impact"):
    total_hospital_beds = data["totalHospitalBeds"]
    severe_cases_by_requested_time = get_severe_cases_by_requested_time(
        data, estimate_type)
    available_beds = int(total_hospital_beds * 0.35)
    hospital_beds = available_beds - severe_cases_by_requested_time
    return hospital_beds


def get_cases_for_icu(data, estimate_type="impact"):
    infections = get_infections_by_requested_time(data, estimate_type)
    cases_for_icu_by_requested_time = 0.05 * infections
    return cases_for_icu_by_requested_time


def get_cases_for_ventilators(data, estimate_type="impact"):
    infections = get_infections_by_requested_time(data, estimate_type)
    cases_for_ventilators_by_requested_time = 0.02 * infections
    return cases_for_ventilators_by_requested_time


def get_dollars_in_flight(data, estimate_type="impact"):
    infections = get_infections_by_requested_time(data, estimate_type)
    dollars_in_flight = infections * 0.65 * 1.5 * get_days(data)
    return dollars_in_flight


def estimator(data):
    data_to_return = {
        "impact":
        {
            "currentlyInfected": data["reportedCases"] * 10,
            "infectionsByRequestedTime": get_infections_by_requested_ime(data),
            "severeCasesByRequestedTime": get_severe_cases_by_requested_time(data),
            "hospitalBedsByRequestedTime": get_hospital_beds_by_requested_time(data),
            "casesForICUByRequestedTime": get_cases_for_icu(data),
            "casesForVentilatorsByRequestedTime": get_cases_for_ventilators(data),
            "dollarsInFlight": get_dollars_in_flight(data),
        },
        "severeImpact": {
            "currentlyInfected": data["reportedCases"] * 10,
            "infectionsByRequestedTime": get_infections_by_requested_time(data),
            "severeCasesByRequestedTime": get_severe_cases_by_requested_time(data),
            "hospitalBedsByRequestedTime": get_hospital_beds_by_requested_time(data),
            "casesForICUByRequestedTime": get_cases_for_icu(data),
            "casesForVentilatorsByRequestedTime": get_cases_for_ventilators(data),
            "dollarsInFlight": get_dollars_in_flight(data)
        }
    }
    return data_to_return
