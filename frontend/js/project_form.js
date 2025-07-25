// project_form.js

const projectForm = document.getElementById('project-form');
const backBtn = document.getElementById('back-btn');
const origin = window.location.origin;
const apiBaseUrl = origin.split(':').slice(0, 2).join(':');
const token = localStorage.getItem('token');
const role = localStorage.getItem('role');

if (!token || role !== 'forest_dept') {
  alert("Unauthorized. Please log in as Forest Department.");
  window.location.href = '/auth.html';
}

const urlParams = new URLSearchParams(window.location.search);
const projectId = urlParams.get('id');

// Load existing project (edit mode)
if (projectId) {
  fetch(`${apiBaseUrl}:5000/api/projects/${projectId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(project => {
      const inputs = projectForm.querySelectorAll('input, select');
      inputs[0].value = project.name;
      inputs[1].value = project.region;
      inputs[2].value = project.status;
      inputs[3].value = project.start_date;
      inputs[4].value = project.trees_target;
      inputs[5].value = project.trees_planted;
    })
    .catch(err => {
      console.error('Error loading project data:', err);
      alert('Failed to load project');
    });
}

projectForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const payload = {
    name: projectForm.querySelector('input:nth-of-type(1)').value,
    region: projectForm.querySelector('input:nth-of-type(2)').value,
    status: projectForm.querySelector('select').value,
    start_date: projectForm.querySelector('input:nth-of-type(3)').value,
    trees_target: parseInt(projectForm.querySelector('input:nth-of-type(4)').value),
    trees_planted: parseInt(projectForm.querySelector('input:nth-of-type(5)').value)
  };

  const method = projectId ? 'PUT' : 'POST';
  const url = projectId
    ? `${apiBaseUrl}:5000/api/projects/${projectId}`
    : `${apiBaseUrl}:5000/api/projects`;

  fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(() => {
      alert('Project saved successfully!');
      window.location.href = 'forest_dashboard.html';
    })
    .catch(err => {
      console.error('Error saving project:', err);
      alert('Failed to save project');
    });
});

backBtn.addEventListener('click', () => {
  window.location.href = 'forest_dashboard.html';
});
