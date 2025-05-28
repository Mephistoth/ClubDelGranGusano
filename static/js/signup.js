document.addEventListener('DOMContentLoaded', function () {
  const firstNameInput = document.getElementById('id_first_name');

  if (firstNameInput) {
    firstNameInput.addEventListener('input', function () {
      this.value = this.value.replace(/[^a-zA-Z0-9]/g, '');
    });
  }
});
