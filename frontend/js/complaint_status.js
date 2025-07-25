// complaint_status.js

const complaintInfoDiv = document.getElementById('complaint-info');
const backBtn = document.getElementById('back-btn');

const origin = window.location.origin;
const apiBaseUrl = origin.split(':').slice(0, 2).join(':');
const token = localStorage.getItem('token');
const role = localStorage.getItem('role');

if (!token || role !== 'citizen') {
  alert("Unauthorized. Please log in as a citizen.");
  window.location.href = '/auth.html';
}

const urlParams = new URLSearchParams(window.location.search);
const complaintId = urlParams.get('id');

if (!complaintId) {
  complaintInfoDiv.innerHTML = '<p>Invalid complaint ID.</p>';
  throw new Error('Missing complaint ID in URL');
}

function loadComplaintDetails() {
  fetch(`${apiBaseUrl}:5000/api/complaints/${complaintId}`, {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(res => res.json())
    .then(complaint => {
      complaintInfoDiv.innerHTML = `
        <h2>Complaint Description</h2>
        <p>${complaint.description}</p>

        <h3>Category</h3>
        <p>${complaint.category}</p>

        <h3>Location</h3>
        <p>${complaint.location}</p>

        <h3>Status</h3>
        <p>${complaint.status}</p>

        <h3>Submitted Image</h3>
        <img src="${complaint.image_url}" alt="Complaint Image"
             style="max-width:100%; border-radius:5px;" 
             onerror="this.style.display='none'">
      `;
    })
    .catch(err => {
      console.error('Error loading complaint details:', err);
      complaintInfoDiv.innerHTML = '<p>Error loading complaint details.</p>';
    });
}

backBtn.addEventListener('click', () => {
  window.location.href = 'citizen_dashboard.html';
});

// Initialize
loadComplaintDetails();
