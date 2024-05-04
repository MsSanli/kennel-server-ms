from .animal_requests import (
    get_all_animals,
    create_animal,
    delete_animal,
    update_animal,
    get_single_animal,
    get_animals_by_location,
    get_animals_by_status
)
from .location_requests import (
    get_all_locations,
    get_single_location,
    delete_location,
    update_location
)
from .employee_requests import (
    get_all_employees,
    get_single_employee,
    create_employee,
    delete_employee,
    update_employee
)
from .customer_requests import (
    create_customer,
    delete_customer,
    update_customer,
    get_single_customer,
    get_all_customers,
    get_customer_by_email
)
