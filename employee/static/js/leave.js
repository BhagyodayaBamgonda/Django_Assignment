const leaveApi = "/api/leaves/";
const empApi = "/api/employees/";
const leavePage = document.getElementById("leavePage");
const isAdmin = leavePage.dataset.isAdmin === "true";

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);

    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }

    return "";
}

function csrfHeaders() {
    const csrfInput = document.querySelector("[name=csrfmiddlewaretoken]");
    const csrfMeta = document.querySelector("meta[name=csrf-token]");
    const token = csrfInput?.value || csrfMeta?.content || getCookie("csrftoken");

    if (!token) {
        alert("CSRF token not found. Please login again and reload the page.");
    }

    return {
        "Content-Type": "application/json",
        "X-CSRFToken": token
    };
}

function handleApiResponse(res) {
    if (res.status === 204) {
        if (!res.ok) {
            throw "Request failed";
        }

        return Promise.resolve({});
    }

    return res.text().then(text => {
        let data = {};

        if (text) {
            try {
                data = JSON.parse(text);
            } catch (error) {
                data = text;
            }
        }

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
            let actions = "";

            if (isAdmin) {
                actions = `
                <select id="status_${l.id}" class="form-control form-control-sm mb-2">
                    <option ${l.status === "Pending" ? "selected" : ""}>Pending</option>
                    <option ${l.status === "Approved" ? "selected" : ""}>Approved</option>
                    <option ${l.status === "Rejected" ? "selected" : ""}>Rejected</option>
                </select>
                <button class="btn btn-primary btn-sm" onclick="updateStatus(${l.id})">
                    Update Status
                </button>
                `;
            } else if (l.status === "Pending") {
                actions = `
                <button class="btn btn-warning btn-sm" onclick="editLeave(${l.id})">
                    Edit
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteLeave(${l.id})">
                    Delete
                </button>
                `;
            } else {
                actions = "-";
            }

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

            ${actions}

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

        leave_type:document.getElementById("leave_type").value,

        from_date:document.getElementById("from_date").value,

        to_date:document.getElementById("to_date").value,

        reason:document.getElementById("reason").value

    };

    fetch(leaveApi,{
        method:"POST",
        credentials:"same-origin",
        headers: csrfHeaders(),
        body:JSON.stringify(leave)
    })

    .then(handleApiResponse)

    .then(data=>{

        alert("Leave Added Successfully");

        clearLeaveForm();

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

        leave_type:document.getElementById("leave_type").value,

        from_date:document.getElementById("from_date").value,

        to_date:document.getElementById("to_date").value,

        reason:document.getElementById("reason").value

    };

    fetch(leaveApi+id+"/",{
        method:"PUT",
        credentials:"same-origin",
        headers: csrfHeaders(),
        body:JSON.stringify(leave)
    })

    .then(handleApiResponse)

    .then(data=>{

        alert("Leave Updated Successfully");

        clearLeaveForm();

        loadLeaves();

    })

    .catch(showApiError);

}

function updateStatus(id){

    let statusValue=document.getElementById("status_"+id).value;

    fetch(leaveApi+id+"/",{
        method:"PUT",
        credentials:"same-origin",
        headers: csrfHeaders(),
        body:JSON.stringify({status:statusValue})
    })

    .then(handleApiResponse)

    .then(data=>{

        alert("Leave Status Updated");

        loadLeaves();

    })

    .catch(showApiError);

}

// Delete Leave
function deleteLeave(id){

    if(confirm("Delete Leave?")){

        fetch(leaveApi+id+"/",{
            method:"DELETE",
            credentials:"same-origin",
            headers:{
                "X-CSRFToken": csrfHeaders()["X-CSRFToken"]
            }
        })

        .then(handleApiResponse)

        .then(()=>{

            alert("Leave Deleted");

            clearLeaveForm();

            loadLeaves();

        })

        .catch(showApiError);

    }

}

function clearLeaveForm(){
    document.getElementById("leave_id").value="";
    document.getElementById("leave_type").value="Casual";
    document.getElementById("from_date").value="";
    document.getElementById("to_date").value="";
    document.getElementById("reason").value="";
}

loadLeaves();
