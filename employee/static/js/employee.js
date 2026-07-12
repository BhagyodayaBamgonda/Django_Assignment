const api = "/api/employees/";

function handleApiResponse(res) {
    return res.json().then(data => {
        if (!res.ok) {
            throw data;
        }
        return data;
    });
}

function showApiError(error) {
    let message = "Something went wrong";

    if (typeof error === "string") {
        message = error;
    } else if (error && typeof error === "object") {
        message = Object.entries(error)
            .map(([field, value]) => `${field}: ${Array.isArray(value) ? value.join(", ") : value}`)
            .join("\n");
    }

    alert(message);
}

// Load Employees
function loadEmployees() {

    let search = document.getElementById("search").value;

    fetch(api + "?search=" + search)
    .then(res => res.json())
    .then(data => {

        let rows = "";

        data.forEach(emp => {

            rows += `
            <tr>
                <td>${emp.id}</td>
                <td>${emp.employee_id}</td>
                <td>${emp.name}</td>
                <td>${emp.email}</td>
                <td>${emp.department}</td>
                <td>${emp.mobile_number}</td>
                <td>${emp.date_of_joining}</td>

                <td>

                <button class="btn btn-warning btn-sm"
                onclick="editEmployee(${emp.id})">
                Edit
                </button>

                <button class="btn btn-danger btn-sm"
                onclick="deleteEmployee(${emp.id})">
                Delete
                </button>

                </td>

            </tr>
            `;

        });

        document.getElementById("employeeTable").innerHTML = rows;

    });

}

// Save Employee
function saveEmployee() {

    let employee = {

        employee_id: document.getElementById("employee_id").value,

        name: document.getElementById("name").value,

        email: document.getElementById("email").value,

        department: document.getElementById("department").value,

        mobile_number: document.getElementById("mobile_number").value,

        date_of_joining: document.getElementById("date_of_joining").value

    };

    fetch(api, {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(employee)

    })

    .then(handleApiResponse)

    .then(data => {

        alert("Employee Added Successfully");

        clearForm();

        loadEmployees();

    })

    .catch(showApiError);

}

// Edit Employee
function editEmployee(id) {

    fetch(api + id + "/")

    .then(res => res.json())

    .then(emp => {

        document.getElementById("id").value = emp.id;

        document.getElementById("employee_id").value = emp.employee_id;

        document.getElementById("name").value = emp.name;

        document.getElementById("email").value = emp.email;

        document.getElementById("department").value = emp.department;

        document.getElementById("mobile_number").value = emp.mobile_number;

        document.getElementById("date_of_joining").value = emp.date_of_joining;

    });

}

// Update Employee
function updateEmployee() {

    let id = document.getElementById("id").value;

    let employee = {

        employee_id: document.getElementById("employee_id").value,

        name: document.getElementById("name").value,

        email: document.getElementById("email").value,

        department: document.getElementById("department").value,

        mobile_number: document.getElementById("mobile_number").value,

        date_of_joining: document.getElementById("date_of_joining").value

    };

    fetch(api + id + "/", {

        method: "PUT",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify(employee)

    })

    .then(handleApiResponse)

    .then(data => {

        alert("Employee Updated Successfully");

        clearForm();

        loadEmployees();

    })

    .catch(showApiError);

}

// Delete Employee
function deleteEmployee(id) {

    if(confirm("Are you sure?")) {

        fetch(api + id + "/", {

            method: "DELETE"

        })

        .then(() => {

            alert("Employee Deleted");

            loadEmployees();

        });

    }

}

// Clear Form
function clearForm(){

    document.getElementById("id").value="";

    document.getElementById("employee_id").value="";

    document.getElementById("name").value="";

    document.getElementById("email").value="";

    document.getElementById("department").value="";

    document.getElementById("mobile_number").value="";

    document.getElementById("date_of_joining").value="";
}

// Load Employees when page opens
loadEmployees();
