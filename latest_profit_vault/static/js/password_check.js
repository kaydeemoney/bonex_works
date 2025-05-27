// static/js/password_check.js
document.addEventListener("DOMContentLoaded", () => {
  const passwordField = document.querySelector('input[name="password"]');
  const confirmPasswordField = document.querySelector('input[name="confirmPassword"]');

  const checkMatch = () => {
    if (passwordField.value && confirmPasswordField.value) {
      if (passwordField.value === confirmPasswordField.value) {
        confirmPasswordField.style.border = "2px solid green";
        confirmPasswordField.setCustomValidity("");
      } else {
        confirmPasswordField.style.border = "2px solid red";
        confirmPasswordField.setCustomValidity("Passwords do not match!");
      }
    } else {
      confirmPasswordField.style.border = "";
      confirmPasswordField.setCustomValidity("");
    }
  };

  passwordField.addEventListener("input", checkMatch);
  confirmPasswordField.addEventListener("input", checkMatch);

  
});



