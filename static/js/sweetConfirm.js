/* static/js/sweetConfirm.js */

function sweetConfirm(elt, config) {
      Swal.fire(config)
          .then((result) => {
                  if (result.isConfirmed) {
                      elt.dispatchEvent(new Event('confirmed')); /* adaptation of Swal to output a event to a more HTML centric behaviour */
                  }
          });
}
