  document.querySelectorAll(".form-steps").forEach(function (n) {
      n.querySelectorAll(".nexttab").forEach(function (t) {
          n.querySelectorAll('button[data-bs-toggle="pill"]').forEach(function (e) {
              e.addEventListener("show.bs.tab", function (e) {
                  e.target.classList.add("done");
              });
          }),
              t.addEventListener("click", function () {
                  var e = t.getAttribute("data-nexttab");
                  document.getElementById(e).click();
              });
      }),
          n.querySelectorAll(".previestab").forEach(function (r) {
              r.addEventListener("click", function () {
                  for (var e = r.getAttribute("data-previous"), t = r.closest("form").querySelectorAll(".custom-nav .done").length, o = t - 1; o < t; o++)
                      r.closest("form").querySelectorAll(".custom-nav .done")[o] && r.closest("form").querySelectorAll(".custom-nav .done")[o].classList.remove("done");
                  document.getElementById(e).click();
              });
          });
      var l = n.querySelectorAll('button[data-bs-toggle="pill"]');
      l.forEach(function (o, r) {
          o.setAttribute("data-position", r),
              o.addEventListener("click", function () {
                  var e;
                  o.getAttribute("data-progressbar") &&
                      ((e = document.getElementById("custom-progress-bar").querySelectorAll("li").length - 1), (e = (r / e) * 100), (document.getElementById("custom-progress-bar").querySelector(".progress-bar").style.width = e + "%")),
                      0 < n.querySelectorAll(".custom-nav .done").length &&
                          n.querySelectorAll(".custom-nav .done").forEach(function (e) {
                              e.classList.remove("done");
                          });
                  for (var t = 0; t <= r; t++) l[t].classList.contains("active") ? l[t].classList.remove("done") : l[t].classList.add("done");
              });
      });
  });
