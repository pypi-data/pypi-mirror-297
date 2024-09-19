from policyengine_us.model_api import *


class is_child_dependent(Variable):
    value_type = bool
    entity = Person
    label = "Is a child dependent based on the IRS definition"
    reference = "https://www.law.cornell.edu/uscode/text/26/152#c_3_A_ii"
    definition_period = YEAR

    def formula(person, period, parameters):
        is_dependent = person("is_tax_unit_dependent", period)
        age = person("age", period)
        p = parameters(period).gov.irs.dependent.ineligible_age
        student = person("is_full_time_student", period)
        age_limit = where(student, p.student, p.non_student)
        age_eligible = age < age_limit
        return is_dependent & age_eligible
