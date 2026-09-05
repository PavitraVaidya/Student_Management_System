document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll(".delete-btn");

    buttons.forEach(button => {

        button.addEventListener("click", function () {

            const id = this.dataset.id;

            Swal.fire({

                title: "Delete Student?",

                text: "You cannot undo this action.",

                icon: "warning",

                showCancelButton: true,

                confirmButtonText: "Delete"

            }).then((result) => {

                if (result.isConfirmed) {

                    window.location.href =
                        "/students/delete/" + id + "/";

                }

            });

        });

    });

});