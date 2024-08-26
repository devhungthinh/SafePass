/* SweetAlert2 Toast */
const Toast = Swal.mixin({
  toast: true,
  position: "top-start",
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.onmouseenter = Swal.stopTimer;
    toast.onmouseleave = Swal.resumeTimer;
  }
});

/* Remove all query paramters when pressing CTRL+R. */
window.addEventListener('beforeunload', (evt) => {
  // evt.preventDefault();
  const url = window.location.origin + window.location.pathname;
  window.location.href = url;
  window.history.replaceState({}, document.title, url);
  return '';
});

window.onload = () => {
  document.body.addEventListener('htmx:configRequest', (evt) => {
    evt.detail.headers['X-CSRFToken'] = document.querySelector('meta[name="csrf-token"').getAttribute('content');
  });

  document.body.addEventListener('htmx:confirm', (evt) => {
    const target = evt.target;

    if (target.matches("[confirm-with-sweet-alert='true']")) {
      evt.preventDefault();
      evt.stopPropagation();
      Swal.fire({
        title: "Are you sure?",
        text: "Are you sure you want to remove this password entry from the vault?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: 'Delete it!',
        cancelButtonText: 'Cancel'
      }).then((result) => {
        if (result.isConfirmed) {
          evt.detail.issueRequest(true);
          Toast.fire({
            icon: "success",
            title: "You have been deleted "
          });
        }
      });
    } else if (target.matches(".row-select")) {
      evt.preventDefault();
      evt.stopPropagation();
      logInfo("input.row-select");
    }
  });

  document.body.addEventListener('htmx:beforeRequest', (evt) => {
    const elt = evt.detail.elt;
    const target = evt.detail.target;
  });

  document.body.addEventListener('htmx:afterRequest', (evt) => {
    if (evt.detail.requestConfig.verb === 'post') {
      const response = evt.detail.xhr.response;
      try {
        const data = JSON.parse(response);
        if (data.success) {
          Toast.fire({
            icon: "success",
            title: 'Selected Vault Deletion',
            text: data.message,
          });
        } else {
          Toast.fire({
            icon: "error",
            title: 'Selected Vault Deletion',
            text: data.message,
          });
        }
      } catch (e) {
        console.log('Error parsing JSON response:', e);
        Toast.fire({
          icon: "error",
          title: "System Error",
          text: 'Unable to process json response.',
        });
      }
    } else if (evt.detail.requestConfig.verb === 'delete') {
      const response = evt.detail.xhr.response;
      try {
        var data = JSON.parse(response);
        if (data.success) {
          Toast.fire({
            icon: "success",
            title: 'Vault Deletion',
            text: data.message,
          });
        } else {
          Toast.fire({
            icon: "error",
            title: 'Vault Deletion',
            text: data.message,
          });
        }
      } catch (e) {
        toastr.error('Unable to process json response.');
        Toast.fire({
          icon: "error",
          title: "System Error",
          text: 'Unable to process json response.',
        });
      }
    }
  });

  document.body.addEventListener('htmx:afterSwap', (evt) => {
    // logInfo('htmx:afterSwap');
    const target = evt.target;

    if (target.matches("tr")) {
      console.log(target);
    } else if (target.matches("li")) {
      // Display a dialog box to confirm whether user want to delete the password in the vault.
      const response = JSON.parse(evt.detail.xhr.responseText);
      if (response.success) {
        Toast.fire({
          icon: "success",
          title: "Password Deletion Success",
          text: "You have successfully removed the password.",
        });
        target.remove();
      } else {
        Toast.fire({
          icon: "error",
          title: "Password Deletion Fail",
          text: "Sorry, there's a problem appeared in the system. Please try again!",
        });
      }
    } else if (target.classList.contains('offcanvas-body')) {
      // Show details about instance on offcanvas.
      // logInfo('inside offcanvas-body');
      const offcanvasElement = document.querySelector('.offcanvas');
      const offcanvas = new bootstrap.Offcanvas(offcanvasElement);
      offcanvas.show();
    }
  });

  document.addEventListener('click', (evt) => {
    const offcanvasElement = document.getElementById('offcanvasVaultDetail')
    const offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
    if (offcanvasElement && !offcanvasElement.contains(evt.target) && offcanvasElement.classList.contains('show')) {
      logInfo('clicked outside offcanvas!');
      // Hide the offcanvas
      offcanvas.hide();

      // Optionally remove the backdrop manually if needed
      var backdrop = document.querySelector('.offcanvas-backdrop');
      if (backdrop) {
        backdrop.remove();
      }
    }
  });
};



// 5 custom logging functions with different severity levels
function logDebug(message) {
  console.log('%cDEBUG: %s', 'color: blue; font-weight: bold;', message);
}

function logInfo(message, ...args) {
  console.log('%cINFO: %s', 'color: green; font-weight: bold;', message, args);
}

function logWarn(message, ...args) {
  console.log('%cWARN: %s', 'color: orange; font-weight: bold;', message, ...args);
}

function logError(message, ...args) {
  console.log('%cERROR: %s', 'color: red; font-weight: bold;', message, ...args);
}

function logFatal(message, ...args) {
  console.log('%cFATAL: %s', 'color: purple; font-weight: bold;', message, ...args);
}

function toastConfig() {
  toastr.options = {
    "closeButton": true,
    "closeMethod": 'fadeOut',
    "closeDuration": "300",
    "closeEasing": "swing",
    "onShown": function () { logInfo('toastr showed!') },
    "onHidden": function () { logInfo('toastr hidden!'); },
    "onclick": function () { logInfo('toastr clicked!'); },
    "onCloseClick": function () { logInfo('toastr close button clicked!'); },
    "timeOut": 3000,
    "extendedTimeOut": 60,
    "progressBar": true,
    "positionClass": "toast-top-left",
  };
}
toastConfig();


class ToastNotification {
  static parse(evt, title = "") {
    const response = evt.detail.xhr.response;
    try {
      const data = JSON.parse(response);
      ToastNotification._displayToast(data, title);
    } catch (err) {
      console.error('Error parsing JSON response:', err);
      Toast.fire({
        icon: "error",
        title: "System Error",
        text: 'Unable to process json response.',
      });
    }
  }

  static _displayToast(data, title = "") {
    if (data.success) {
      Toast.fire({
        icon: 'success',
        title: title,
        text: data.message,
      });
    } else {
      Toast.fire({
        icon: 'success',
        title: title,
        text: data.message,
      })
    }
  }

  static display(evt, title = "") {
    ToastNotification.parse(evt, title);
  }
}