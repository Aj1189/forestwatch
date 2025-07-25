// citizen_dashboard.js

const projectsList = document.getElementById('projects-list');
const complaintsList = document.getElementById('complaints-list');
const newComplaintBtn = document.getElementById('new-complaint-btn');
const logoutBtn = document.getElementById('logout-btn');

const origin = window.location.origin;
const apiBaseUrl = origin.split(':').slice(0, 2).join(':');
const token = localStorage.getItem('token');

if (!token) {
  alert("Unauthorized. Please log in.");
  window.location.href = '/auth.html';
}

// Load projects from API
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
        `;
        projectsList.appendChild(card);
      });
    })
    .catch(err => {
      console.error('Error loading projects:', err);
      alert('Failed to load projects');
    });
}

// Load complaints from API
function loadComplaints() {
  fetch(`${apiBaseUrl}:5000/api/complaints/user`, {
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
          <img src="${c.image_url}" alt="Complaint Image" style="max-width: 100%; border-radius: 5px;" onerror="this.style.display='none'">
        `;
        complaintsList.appendChild(card);
      });
    })
    .catch(err => {
      console.error('Error loading complaints:', err);
      alert('Failed to load complaints');
    });
}

// Handle new complaint button
newComplaintBtn.addEventListener('click', () => {
  window.location.href = 'submit_complaint.html';
});

// Handle logout
logoutBtn.addEventListener('click', () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.location.href = '/auth.html';
});

// Initialize
loadProjects();
loadComplaints();
