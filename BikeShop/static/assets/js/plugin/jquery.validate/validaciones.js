
    $.validator.addMethod("lettersAndSpaces", function (value, element) {
        return this.optional(element) || /^[a-zA-Z\s]+$/.test(value);
    }, "Solo se permiten letras y espacios");

    $(document).ready(function () {
        $("#frm_nuevo_cliente").validate({
            rules: {
                "nombre_cli": {
                    required: true,
                    lettersAndSpaces: true,
                    minlength: 2
                },
                "correo_cli": {
                    required: true,
                    email: true
                },
                "direccion_cli": {
                    required: true,
                    minlength: 5
                },
                "fono": {
                    required: true,
                    number: true,
                    minlength: 7,
                    maxlength: 15
                },
                "estatura_cli": {
                    required: true,
                    number: true,
                    min: 0.5, // Estatura mínima (en metros)
                    max: 2.5  // Estatura máxima (en metros)
                },
                "id_cli": {
                    required: true,
                    validEcuadorianId: true
                }
            },
            messages: {
                "nombre_cli": {
                    required: "Por favor ingrese el nombre del cliente",
                    lettersAndSpaces: "Solo se permiten letras y espacios",
                    minlength: "El nombre debe tener al menos 2 caracteres"
                },
                "correo_cli": {
                    required: "Por favor ingrese el correo del cliente",
                    email: "Ingrese un correo electrónico válido"
                },
                "direccion_cli": {
                    required: "Por favor ingrese la dirección del cliente",
                    minlength: "La dirección debe tener al menos 5 caracteres"
                },
                "fono": {
                    required: "Por favor ingrese el teléfono",
                    number: "Ingrese un número válido",
                    minlength: "El teléfono debe tener al menos 7 dígitos",
                    maxlength: "El teléfono no puede tener más de 15 dígitos"
                },
                "estatura_cli": {
                    required: "Por favor ingrese la estatura del cliente",
                    number: "Ingrese un número válido",
                    min: "La estatura debe ser al menos 0.5 metros",
                    max: "La estatura no puede ser más de 2.5 metros"
                },
                "id_cli": {
                    required: "Por favor ingrese la cédula del cliente",
                    validEcuadorianId: "Por favor ingrese una cédula ecuatoriana válida"
                }
            },
            errorClass: "text-danger"
        });

        $("#frm_nuevo_cliente").submit(function (event) {
            event.preventDefault();
            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'),
                data: $(this).serialize(),
                success: function (response) {
                    if (response.success) {
                        window.location.href = "/clientes"; // Redirigir a la lista de clientes
                    } else {
                        alert("Error al guardar el cliente.");
                    }
                },
                error: function () {
                    alert("Error en la comunicación con el servidor.");
                }
            });
        });
    });
