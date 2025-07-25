const token = localStorage.getItem('token');
const role = localStorage.getItem('role');
const origin = window.location.origin;
const apiBaseUrl = origin.split(':').slice(0, 2).join(':');

if (!token || role !== 'forest_dept') {
  alert("Unauthorized. Please log in with Forest Dept credentials.");
  window.location.href = '/auth.html';
}

document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.location.href = "/auth.html";
});

function renderList(sectionId, data, labelKey = "type") {
  const container = document.getElementById(sectionId);
  container.innerHTML = "";
  if (data.length === 0) {
    container.innerHTML = "<p>No data available.</p>";
    return;
  }

  const ul = document.createElement("ul");
  data.forEach(item => {
    const li = document.createElement("li");
    const label = item[labelKey] || item.region || item.month;
    li.textContent = `${label.toUpperCase()} — ${item.count}`;
    ul.appendChild(li);
  });
  container.appendChild(ul);
}

function loadReport() {
  fetch(`${apiBaseUrl}:5000/api/reports`, {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(data => {
      renderList("report-category", data.by_category, "type");
      renderList("report-region", data.by_region, "region");
      renderList("report-month", data.by_month, "month");
      renderList("report-hotzones", data.hot_zones, "region");
    })
    .catch(err => {
      console.error("Error fetching report:", err);
      alert("Failed to load report data.");
    });
}

loadReport();
