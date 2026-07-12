const leaveApi = "/api/leaves/";
const empApi = "/api/employees/";

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

// Load Employee Dropdown
function loadEmployees(){

    fetch(empApi)
    .then(res=>res.json())
    .then(data=>{

        let options="";

        data.forEach(emp=>{

            options+=`<option value="${emp.id}">
                        ${emp.name}
                      </option>`;

        });

        document.getElementById("employee").innerHTML=options;

    });

}

// Load Leave Table
function loadLeaves(){

    let status=document.getElementById("filterStatus").value;
    let type=document.getElementById("filterType").value;

    let url=leaveApi;

    let params=[];

    if(status!="")
        params.push("status="+status);

    if(type!="")
        params.push("leave_type="+type);

    if(params.length>0)
        url+="?"+params.join("&");

    fetch(url)
    .then(res=>res.json())
    .then(data=>{

        let rows="";

        data.forEach(l=>{

            rows+=`
            <tr>

            <td>${l.id}</td>

            <td>${l.employee_name || l.employee}</td>

            <td>${l.leave_type}</td>

            <td>${l.from_date}</td>

            <td>${l.to_date}</td>

            <td>${l.reason}</td>

            <td>${l.status}</td>

            <td>

            <button class="btn btn-warning btn-sm"
            onclick="editLeave(${l.id})">

            Edit

            </button>

            <button class="btn btn-danger btn-sm"
            onclick="deleteLeave(${l.id})">

            Delete

            </button>

            </td>

            </tr>
            `;

        });

        document.getElementById("leaveTable").innerHTML=rows;

    });

}

// Save Leave
function saveLeave(){

    let leave={

        employee:document.getElementById("employee").value,

        leave_type:document.getElementById("leave_type").value,

        from_date:document.getElementById("from_date").value,

        to_date:document.getElementById("to_date").value,

        reason:document.getElementById("reason").value

    };

    fetch(leaveApi,{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(leave)

    })

    .then(handleApiResponse)

    .then(data=>{

        alert("Leave Added Successfully");

        loadLeaves();

    })

    .catch(showApiError);

}

// Edit Leave
function editLeave(id){

    fetch(leaveApi+id+"/")
    .then(res=>res.json())
    .then(l=>{

        document.getElementById("leave_id").value=l.id;
        document.getElementById("employee").value=l.employee;
        document.getElementById("leave_type").value=l.leave_type;
        document.getElementById("from_date").value=l.from_date;
        document.getElementById("to_date").value=l.to_date;
        document.getElementById("reason").value=l.reason;

    });

}

// Update Leave
function updateLeave(){

    let id=document.getElementById("leave_id").value;

    let leave={

        employee:document.getElementById("employee").value,

        leave_type:document.getElementById("leave_type").value,

        from_date:document.getElementById("from_date").value,

        to_date:document.getElementById("to_date").value,

        reason:document.getElementById("reason").value

    };

    fetch(leaveApi+id+"/",{

        method:"PUT",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify(leave)

    })

    .then(handleApiResponse)

    .then(data=>{

        alert("Leave Updated Successfully");

        loadLeaves();

    })

    .catch(showApiError);

}

// Delete Leave
function deleteLeave(id){

    if(confirm("Delete Leave?")){

        fetch(leaveApi+id+"/",{

            method:"DELETE"

        })

        .then(()=>{

            alert("Leave Deleted");

            loadLeaves();

        });

    }

}

loadEmployees();
loadLeaves();
