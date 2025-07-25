// forest_dashboard.js

const projectsList = document.getElementById('projects-list');
const complaintsList = document.getElementById('complaints-list');
const newProjectBtn = document.getElementById('new-project-btn');
const reportBtn = document.getElementById('report-btn');
const logoutBtn = document.getElementById('logout-btn');

const origin = window.location.origin;
const apiBaseUrl = origin.split(':').slice(0, 2).join(':');
const token = localStorage.getItem('token');
const role = localStorage.getItem('role');

if (!token || role !== 'forest_dept') {
  alert("Unauthorized. Please log in with Forest Dept credentials.");
  window.location.href = '/auth.html';
}

// Load projects
function loadProjects() {
  fetch(`${apiBaseUrl}:5000/api/projects`, {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(projects => {
      projectsList.innerHTML = '';
      projects.forEach(project => {
        const card = document.createElement('div');
        const percent = Math.min(100, Math.round((project.trees_planted / project.trees_target) * 100));
        card.className = 'project-card';
        card.innerHTML = `
          <h3>${project.name}</h3>
          <p><strong>Region:</strong> ${project.region}</p>
          <p><strong>Status:</strong> ${project.status}</p>
          <p><strong>Start Date:</strong> ${project.start_date}</p>
          <p><strong>Trees Planted:</strong> ${project.trees_planted} / ${project.trees_target}</p>
          <div style="background: #ddd; border-radius: 4px; overflow: hidden; height: 10px; margin-bottom: 0.5rem;">
            <div style="width: ${percent}%; background: #4caf50; height: 100%;"></div>
          </div>
          <div>
            <button onclick="editProject(${project.id})">Edit</button>
            <button onclick="deleteProject(${project.id})">Delete</button>
          </div>
        `;
        projectsList.appendChild(card);
      });
    })
    .catch(err => {
      console.error('Error loading projects:', err);
      alert('Failed to load projects');
    });
}

// Load complaints
function loadComplaints() {
  fetch(`${apiBaseUrl}:5000/api/complaints`, {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(complaints => {
      complaintsList.innerHTML = '';
      complaints.forEach(c => {
        const card = document.createElement('div');
        card.className = 'complaint-card';
        card.innerHTML = `
          <p><strong>Description:</strong> ${c.description}</p>
          <p><strong>Category:</strong> ${c.category}</p>
          <p><strong>Location:</strong> ${c.location}</p>
          <p><strong>Status:</strong> ${c.status}</p>
          <p><strong>Rejection Reason:</strong> ${c.rejection_reason}</p>
          <p><strong>Created At:</strong> ${c.created_at}</p>
          <img src="${c.image_url}" alt="Complaint Image" style="max-width: 100%; border-radius: 5px; margin-top: 0.5rem;" onerror="this.style.display='none'">
          <div style="margin-top: 0.5rem;">
            <button onclick="updateComplaintStatus(${c.id}, 'In Progress')">Mark In Progress</button>
            <button onclick="updateComplaintStatus(${c.id}, 'Resolved')">Mark Resolved</button>
          </div>
        `;
        complaintsList.appendChild(card);
      });
    })
    .catch(err => {
      console.error('Error loading complaints:', err);
      alert('Failed to load complaints');
    });
}

// Project actions
function editProject(id) {
  alert(`Edit project ${id} (future: redirect to edit form)`);
  window.location.href = `project_form.html?id=${id}`;
}

function deleteProject(id) {
  if (confirm('Are you sure you want to delete this project?')) {
    fetch(`${apiBaseUrl}:5000/api/projects/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(() => {
        alert('Project deleted');
        loadProjects();
      })
      .catch(err => {
        console.error('Error deleting project:', err);
        alert('Failed to delete project');
      });
  }
}

// Complaint status update
function updateComplaintStatus(id, status) {
  fetch(`${apiBaseUrl}:5000/api/complaints/${id}/status`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ status })
  })
    .then(res => res.json())
    .then(() => {
      alert(`Complaint marked as ${status}`);
      loadComplaints();
    })
    .catch(err => {
      console.error('Error updating complaint:', err);
      alert('Failed to update complaint status');
    });
}

// Add new project
newProjectBtn.addEventListener('click', () => {
  alert('Redirecting to add new project form');
  window.location.href = 'project_form.html';
});

// Report page
reportBtn.addEventListener('click', () => {
  window.location.href = 'report.html';
});

// Logout
logoutBtn.addEventListener('click', () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.location.href = '/auth.html';
});

// Initialize
loadProjects();
loadComplaints();
