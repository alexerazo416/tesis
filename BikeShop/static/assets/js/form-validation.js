

<script>
    $.validator.addMethod("lettersAndSpaces", function (value, element) {
        return this.optional(element) || /^[a-zA-Z\s]+$/.test(value);
    }, "Solo se permiten letras y espacios");

    $.validator.addMethod("number", function (value, element) {
        return this.optional(element) || /^-?\d+(\.\d{1,2})?$/.test(value);
    }, "Por favor ingrese un número válido");

    $(document).ready(function () {
        $("#frm_nuevo_repuesto").validate({
            rules: {
                "nombre_rep": {
                    required: true,
                    minlength: 2
                },
                "precio_rep": {
                    required: true,
                    number: true
                },
                "marca_rep": {
                    required: true,
                    lettersAndSpaces: true,
                    minlength: 2
                },
                "descripcion_rep": {
                    minlength: 5,
                    required: true,
                }
            },
            messages: {
                "nombre_rep": {
                    required: "Por favor ingrese el nombre del repuesto",
                    minlength: "El nombre debe tener al menos 2 caracteres"
                },
                "precio_rep": {
                    required: "Por favor ingrese el precio del repuesto",
                    number: "Por favor ingrese un número válido"
                },
                "marca_rep": {
                    required: "Por favor ingrese la marca del repuesto",
                    lettersAndSpaces: "Solo se permiten letras y espacios",
                    minlength: "La marca debe tener al menos 2 caracteres"
                },
                "descripcion_rep": {
                    minlength: "La descripción debe tener al menos 5 caracteres",
                    required: "Por favor ingrese la descripción repuesto",
                }
            },
            errorClass: "text-danger"
        });
    });
</script>
