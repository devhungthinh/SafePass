const deleteVaultBtns = document.querySelectorAll('button.delete-vault');
deleteVaultBtns.forEach((deleteVaultBtn) => {
  deleteVaultBtn.addEventListener('htmx:confirm', (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    Swal.fire({
      title: "Are you sure?",
      text: "Are you sure you want to remove this password entry from the vault?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel'
    }).then((result) => {
      if (result.isConfirmed) {
        evt.detail.issueRequest(true);
      }
    });
  });

  deleteVaultBtn.addEventListener('htmx:afterRequest', (evt) => {
    ToastNotification.display(evt, 'Delete Vault');
  });
});

document.querySelectorAll('button.restore-password-entry').forEach((restorePasswordBtn) => {
  restorePasswordBtn.addEventListener('htmx:afterRequest', (evt) => {
    ToastNotification.display(evt, "Restore password");
  });
});

document.querySelectorAll('button.delete-password-entry').forEach((deletePasswordBtn) => {
  deletePasswordBtn.addEventListener('htmx:confirm', (evt) => {
    evt.preventDefault();
    evt.stopPropagation();
    Swal.fire({
      title: 'Are you sure?',
      text: 'Are you sure you want to delete this password? You cannot recover it later.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Delete',
      cancelButtonText: 'Cancel',
    }).then((result) => {
      if (result.isConfirmed) {
        // evt.detail.issueRequest();
        trashedPasswordCount -= 1;
        if (trashedPasswordCount == 0) {

        }
      }
    });
  });

  deletePasswordBtn.addEventListener('htmx:afterRequest', (evt) => {
    ToastNotification.display(evt, 'Delete password');
  })
});
