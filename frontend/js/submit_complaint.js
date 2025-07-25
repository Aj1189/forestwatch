// submit_complaint.js

const complaintForm = document.getElementById('complaint-form');
const backBtn = document.getElementById('back-btn');
const origin = window.location.origin;
const apiBaseUrl = origin.split(':').slice(0, 2).join(':');
const token = localStorage.getItem('token');

if (!token) {
  alert("Unauthorized. Please log in.");
  window.location.href = '/auth.html';
}

complaintForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const description = complaintForm.querySelector('textarea').value.trim();
  const category = complaintForm.querySelector('select').value;
  const location = complaintForm.querySelector('input[type="text"]').value.trim();
  const imageFile = complaintForm.querySelector('input[type="file"]').files[0];

  if (!description || !category || !location || !imageFile) {
    alert('All fields including image are required.');
    return;
  }

  const formData = new FormData();
  formData.append('description', description);
  formData.append('category', category);
  formData.append('location', location);
  formData.append('image', imageFile);

  fetch(`${apiBaseUrl}:5000/api/complaints`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    },
    body: formData
  })
    .then(res => res.json())
    .then(data => {
      console.log('Complaint submitted:', data);
      alert('Complaint submitted successfully!');
      window.location.href = 'citizen_dashboard.html';
    })
    .catch(err => {
      console.error('Error submitting complaint:', err);
      alert('Failed to submit complaint');
    });
});

backBtn.addEventListener('click', () => {
  window.location.href = 'citizen_dashboard.html';
});
