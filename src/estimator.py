def estimator(data):
    def get_days():
        periodType = data["periodType"]
        assert periodType in ["days", "weeks", "months"]

        if periodType == "days":
            return data["timeToElapse"]
        elif periodType == "weeks":
            return data["timeToElapse"] * 7
        else:
            return data["timeToElapse"] * 30

    def get_estimation_factor():
        days = get_days()
        return int(days / 3)

    def get_infections_cases(estimate_type="impact"):
        assert estimate_type in ["impact", "severe"]
        multiplier = 10 if estimate_type == "impact" else 50

        currently_infected = data["reportedCases"] * multiplier
        factor = get_estimation_factor()
        return currently_infected * pow(2, factor)

    convid_cases = get_infections_cases()
    severe_cases = get_infections_cases("severe")

    def get_severe_cases(estimate_type="impact"):
        cases = convid_cases if estimate_type == "impact" else severe_cases
        return float(int(cases * 0.15))

    def get_hospital_beds(estimate_type="impact"):
        available_beds = data["totalHospitalBeds"] * 0.35
        available_beds = float(int(available_beds))
        return available_beds - get_severe_cases(estimate_type)

    def get_icu_cases(estimate_type="impact"):
        cases = convid_cases if estimate_type == "impact" else severe_cases
        return int(0.05 * cases)

    def get_ventilators_cases(estimate_type="impact"):
        cases = convid_cases if estimate_type == "impact" else severe_cases
        return int(0.02 * cases)

    def get_dollars_in_flight(estimate_type="impact"):
        avg_income = data["region"]["avgDailyIncomeInUSD"]
        cases = convid_cases if estimate_type == "impact" else severe_cases
        return float(int((cases * 0.65 * avg_income * get_days())))

    data_to_return = {
        "data": data,
        "impact":   {
            "currentlyInfected": data["reportedCases"] * 10,
            "infectionsByRequestedTime": get_infections_cases(),
            "severeCasesByRequestedTime": get_severe_cases(),
            "hospitalBedsByRequestedTime": get_hospital_beds(),
            "casesForICUByRequestedTime": get_icu_cases(),
            "casesForVentilatorsByRequestedTime": get_ventilators_cases(),
            "dollarsInFlight": get_dollars_in_flight(),
        },
        "severeImpact": {
            "currentlyInfected": data["reportedCases"] * 50,
            "infectionsByRequestedTime": get_infections_cases("severe"),
            "severeCasesByRequestedTime": get_severe_cases("severe"),
            "hospitalBedsByRequestedTime": get_hospital_beds("severe"),
            "casesForICUByRequestedTime": get_icu_cases("severe"),
            "casesForVentilatorsByRequestedTime": get_ventilators_cases(
                "severe"),
            "dollarsInFlight": get_dollars_in_flight("severe")
        }
    }
    return data_to_return
