localStorage.removeItem("ticket-list");
var str_dt = function (e) {
        var t = new Date(e),
            a = "" + ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][t.getMonth()],
            e = "" + t.getDate(),
            t = t.getFullYear();
        return a.length < 2 && (a = "0" + a), [(e = e.length < 2 ? "0" + e : e) + " " + a, t].join(", ");
    },
    checkAll = document.getElementById("checkAll");
checkAll &&
    (checkAll.onclick = function () {
        for (var e = document.querySelectorAll('.form-check-all input[type="checkbox"]'), t = 0; t < e.length; t++)
            (e[t].checked = this.checked), e[t].checked ? e[t].closest("tr").classList.add("table-active") : e[t].closest("tr").classList.remove("table-active");
    });
var perPage = 8,
    options = { valueNames: ["id", "tasks_name", "client_name", "assignedto", "create_date", "due_date", "status", "priority"], page: perPage, pagination: !0, plugins: [ListPagination({ left: 2, right: 2 })] },
    ticketsList = new List("ticketsList", options).on("updated", function (e) {
        0 == e.matchingItems.length ? (document.getElementsByClassName("noresult")[0].style.display = "block") : (document.getElementsByClassName("noresult")[0].style.display = "none");
        var t = 1 == e.i,
            a = e.i > e.matchingItems.length - e.page;
        document.querySelector(".pagination-prev.disabled") && document.querySelector(".pagination-prev.disabled").classList.remove("disabled"),
            document.querySelector(".pagination-next.disabled") && document.querySelector(".pagination-next.disabled").classList.remove("disabled"),
            t && document.querySelector(".pagination-prev").classList.add("disabled"),
            a && document.querySelector(".pagination-next").classList.add("disabled"),
            e.matchingItems.length <= perPage ? (document.querySelector(".pagination-wrap").style.display = "none") : (document.querySelector(".pagination-wrap").style.display = "flex"),
            e.matchingItems.length == perPage && document.querySelector(".pagination.listjs-pagination").firstElementChild.children[0].click(),
            0 < e.matchingItems.length ? (document.getElementsByClassName("noresult")[0].style.display = "none") : (document.getElementsByClassName("noresult")[0].style.display = "block");
    });
const xhttp = new XMLHttpRequest();
(xhttp.onload = function () {
    JSON.parse(this.responseText).forEach(function (e) {
        ticketsList.add({
            id: '<a href="javascript:void(0);" onclick="ViewTickets(this)" data-id="' + e.id + '" class="fw-medium link-primary ticket-id">#VLZ' + e.id + "</a>",
            tasks_name: e.tasks_name,
            client_name: e.client_name,
            assignedto: e.assignedto,
            create_date: str_dt(e.create_date),
            due_date: str_dt(e.due_date),
            priority: isPriority(e.priority),
            status: isStatus(e.status),
        });
    }),
        ticketsList.remove("id", '<a href="javascript:void(0);" onclick="ViewTickets(this)" data-id="001" class="fw-medium link-primary">#VLZ001</a>');
}),
    xhttp.open("GET", "assets/json/support-tickets-list.json"),
    xhttp.send(),
    (isCount = new DOMParser().parseFromString(ticketsList.items.slice(-1)[0]._values.id, "text/html"));
var isValue = isCount.body.firstElementChild.innerHTML,
    idField = document.getElementById("orderId"),
    tasksTitleField = document.getElementById("tasksTitle-field"),
    client_nameNameField = document.getElementById("client_nameName-field"),
    assignedtoNameField = document.getElementById("assignedtoName-field"),
    dateField = document.getElementById("date-field"),
    dateDueField = document.getElementById("duedate-field"),
    priorityField = document.getElementById("priority-field"),
    statusField = document.getElementById("ticket-status"),
    addBtn = document.getElementById("add-btn"),
    editBtn = document.getElementById("edit-btn"),
    removeBtns = document.getElementsByClassName("remove-item-btn"),
    editBtns = document.getElementsByClassName("edit-item-btn");
function filterOrder(e) {
    var t = e;
    ticketsList.filter(function (e) {
        matchData = new DOMParser().parseFromString(e.values().status, "text/html");
        e = matchData.body.firstElementChild.innerHTML;
        return "All" == e || "All" == t || e == t;
    }),
        ticketsList.update();
}
function updateList() {
    var t = document.querySelector("input[name=status]:checked").value;
    (data = userList.filter(function (e) {
        return "All" == t || e.values().sts == t;
    })),
        userList.update();
}
refreshCallbacks(),
    document.getElementById("showModal").addEventListener("show.bs.modal", function (e) {
        e.relatedTarget.classList.contains("edit-item-btn")
            ? ((document.getElementById("exampleModalLabel").innerHTML = "Edit Ticket"),
              (document.getElementById("showModal").querySelector(".modal-footer").style.display = "block"),
              (document.getElementById("add-btn").style.display = "none"),
              (document.getElementById("edit-btn").style.display = "block"))
            : e.relatedTarget.classList.contains("add-btn")
            ? ((document.getElementById("modal-id").style.display = "none"),
              (document.getElementById("exampleModalLabel").innerHTML = "Add Ticket"),
              (document.getElementById("showModal").querySelector(".modal-footer").style.display = "block"),
              (document.getElementById("edit-btn").style.display = "none"),
              (document.getElementById("add-btn").style.display = "block"))
            : ((document.getElementById("exampleModalLabel").innerHTML = "List Ticket"), (document.getElementById("showModal").querySelector(".modal-footer").style.display = "none"));
    }),
    ischeckboxcheck(),
    document.getElementById("showModal").addEventListener("hidden.bs.modal", function () {
        clearFields();
    }),
    document.querySelector("#ticketsList").addEventListener("click", function () {
        refreshCallbacks(), ischeckboxcheck();
    });
var table = document.getElementById("ticketTable"),
    tr = table.getElementsByTagName("tr"),
    trlist = table.querySelectorAll(".list tr");
function SearchData() {
    var l = document.getElementById("idStatus").value,
        s = document.getElementById("demo-datepicker").value,
        n = s.split(" to ")[0],
        d = s.split(" to ")[1];
    ticketsList.filter(function (e) {
        matchData = new DOMParser().parseFromString(e.values().status, "text/html");
        var t = matchData.body.firstElementChild.innerHTML,
            a = !1,
            i = !1,
            a = "all" == t || "all" == l || t == l,
            i = new Date(e.values().create_date.slice(0, 12)) >= new Date(n) && new Date(e.values().create_date.slice(0, 12)) <= new Date(d);
        return (a && i) || (a && "" == s ? a : i && "" == s ? i : void 0);
    }),
        ticketsList.update();
}
var count = Number(isValue.replace(/[^0-9]/g, "")) + 1;
addBtn.addEventListener("click", function (e) {
    "" !== tasksTitleField.value &&
        "" !== client_nameNameField.value &&
        "" !== assignedtoNameField.value &&
        "" !== dateField.value &&
        "" !== dateDueField.value &&
        "" !== statusField.value &&
        "" !== priorityField.value &&
        (ticketsList.add({
            id: '<a href="javascript:void(0);" onclick="ViewTickets(this)" data-id="' + count + '" class="fw-medium link-primary ticket-id">#VLZ' + count + "</a>",
            tasks_name: tasksTitleField.value,
            client_name: client_nameNameField.value,
            assignedto: assignedtoNameField.value,
            create_date: dateField.value,
            due_date: dateDueField.value,
            priority: isPriority(priorityField.value),
            status: isStatus(statusField.value),
        }),
        document.getElementById("close-modal").click(),
        clearFields(),
        refreshCallbacks(),
        filterOrder("All"),
        count++);
}),
    editBtn.addEventListener("click", function (e) {
        (document.getElementById("exampleModalLabel").innerHTML = "Edit Order"),
            ticketsList.get({ id: idField.value }).forEach(function (e) {
                (isid = new DOMParser().parseFromString(e._values.id, "text/html")),
                    isid.body.firstElementChild.innerHTML == itemId &&
                        e.values({
                            id: '<a href="javascript:void(0);" onclick="ViewTickets(this)" data-id="' + idField.value + '" class="fw-medium link-primary">' + idField.value + "</a>",
                            tasks_name: tasksTitleField.value,
                            client_name: client_nameNameField.value,
                            create_date: str_dt(dateField.value),
                            due_date: str_dt(dateDueField.value),
                            priority: isPriority(priorityField.value),
                            status: isStatus(statusField.value),
                        });
            }),
            document.getElementById("close-modal").click(),
            clearFields();
    });
var example = new Choices(priorityField, { searchEnabled: !1 }),
    statusVal = new Choices(statusField, { searchEnabled: !1 });
function isStatus(e) {
    switch (e) {
        case "Open":
            return '<span class="badge badge-soft-success text-uppercase">' + e + "</span>";
        case "Inprogress":
            return '<span class="badge badge-soft-warning text-uppercase">' + e + "</span>";
        case "Closed":
            return '<span class="badge badge-soft-danger text-uppercase">' + e + "</span>";
        case "New":
            return '<span class="badge badge-soft-info text-uppercase">' + e + "</span>";
    }
}
function isPriority(e) {
    switch (e) {
        case "High":
            return '<span class="badge bg-danger text-uppercase">' + e + "</span>";
        case "Low":
            return '<span class="badge bg-success text-uppercase">' + e + "</span>";
        case "Medium":
            return '<span class="badge bg-warning text-uppercase">' + e + "</span>";
    }
}
function ischeckboxcheck() {
    document.getElementsByName("checkAll").forEach(function (e) {
        e.addEventListener("click", function (e) {
            e.target.checked ? e.target.closest("tr").classList.add("table-active") : e.target.closest("tr").classList.remove("table-active");
        });
    });
}
function refreshCallbacks() {
    removeBtns.forEach(function (e) {
        e.addEventListener("click", function (e) {
            e.target.closest("tr").children[1].innerText,
                (itemId = e.target.closest("tr").children[1].innerText),
                ticketsList.get({ id: itemId }).forEach(function (e) {
                    deleteid = new DOMParser().parseFromString(e._values.id, "text/html");
                    var t = deleteid.body.firstElementChild;
                    deleteid.body.firstElementChild.innerHTML == itemId &&
                        document.getElementById("delete-record").addEventListener("click", function () {
                            ticketsList.remove("id", t.outerHTML), document.getElementById("deleteOrder").click();
                        });
                });
        });
    }),
        editBtns.forEach(function (e) {
            e.addEventListener("click", function (e) {
                e.target.closest("tr").children[1].innerText,
                    (itemId = e.target.closest("tr").children[1].innerText),
                    ticketsList.get({ id: itemId }).forEach(function (e) {
                        isid = new DOMParser().parseFromString(e._values.id, "text/html");
                        var t = isid.body.firstElementChild.innerHTML;
                        t == itemId &&
                            ((idField.value = t),
                            (tasksTitleField.value = e._values.tasks_name),
                            (client_nameNameField.value = e._values.client_name),
                            (assignedtoNameField.value = e._values.assignedto),
                            (dateField.value = e._values.create_date),
                            (dateDueField.value = e._values.due_date),
                            example && example.destroy(),
                            (example = new Choices(priorityField, { searchEnabled: !1 })),
                            (val = new DOMParser().parseFromString(e._values.priority, "text/html")),
                            (t = val.body.firstElementChild.innerHTML),
                            example.setChoiceByValue(t),
                            statusVal && statusVal.destroy(),
                            (statusVal = new Choices(statusField, { searchEnabled: !1 })),
                            (val = new DOMParser().parseFromString(e._values.status, "text/html")),
                            (t = val.body.firstElementChild.innerHTML),
                            statusVal.setChoiceByValue(t),
                            flatpickr("#date-field", { dateFormat: "d M, Y", defaultDate: e._values.create_date }),
                            flatpickr("#duedate-field", { dateFormat: "d M, Y", defaultDate: e._values.due_date }));
                    });
            });
        });
}
function clearFields() {
    (tasksTitleField.value = ""),
        (client_nameNameField.value = ""),
        (assignedtoNameField.value = ""),
        (dateField.value = ""),
        (dateDueField.value = ""),
        example && example.destroy(),
        (example = new Choices(priorityField)),
        statusVal && statusVal.destroy(),
        (statusVal = new Choices(statusField));
}
function deleteMultiple() {
    ids_array = [];
    for (var e, t = document.querySelectorAll(".form-check [value=option1]"), a = 0; a < t.length; a++)
        1 == t[a].checked && ((e = t[a].parentNode.parentNode.parentNode.querySelector("td [data-id]").getAttribute("data-id")), ids_array.push(e));
    if ("undefined" != typeof ids_array && 0 < ids_array.length) {
        if (!confirm("Are you sure you want to delete this?")) return !1;
        ids_array.forEach(function (e) {
            console.log("id", e), ticketsList.remove("id", `<a href="javascript:void(0);" onclick="ViewTickets(this)" data-id="${e}" class="fw-medium link-primary ticket-id">#VLZ${e}</a>`);
        }),
            (document.getElementById("checkAll").checked = !1);
    } else alert("Please Select Atleast One Checkbox");
}
function ViewTickets(e) {
    console.log();
    var t = e.getAttribute("data-id"),
        a = ticketsList.get("id", '<a href="javascript:void(0);" onclick="ViewTickets(this)" data-id="' + t + '" class="fw-medium link-primary ticket-id">#VLZ' + t + "</a>"),
        e = a[0]._values.id,
        t = document.createElement("div");
    t.innerHTML = e;
    t = t.innerText.slice(4);
    console.log("item", t), localStorage.setItem("ticket-list", JSON.stringify(a[0]._values)), localStorage.setItem("option", "view-ticket"), localStorage.setItem("ticket_no", t), window.location.assign("apps-tickets-details.html");
}
document.querySelector(".pagination-next").addEventListener("click", function () {
    !document.querySelector(".pagination.listjs-pagination") ||
        (document.querySelector(".pagination.listjs-pagination").querySelector(".active") && document.querySelector(".pagination.listjs-pagination").querySelector(".active").nextElementSibling.children[0].click());
}),
    document.querySelector(".pagination-prev").addEventListener("click", function () {
        !document.querySelector(".pagination.listjs-pagination") ||
            (document.querySelector(".pagination.listjs-pagination").querySelector(".active") && document.querySelector(".pagination.listjs-pagination").querySelector(".active").previousSibling.children[0].click());
    });