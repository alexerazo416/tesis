$(document).ready(function() {
    $('#frm_nuevo_cliente').parsley({
        // Opciones globales de Parsley
    });

    // Validaciones específicas
    $('#id_cli').parsley().addConstraint('required', true)
        .addConstraint('type', 'digits')
        .addConstraint('required-message', 'La cédula es requerida')
        .addConstraint('type-message', 'La cédula debe contener solo dígitos');

    $('#nombre_cli').parsley().addConstraint('required', true)
        .addConstraint('pattern', '^[a-zA-Z\s]+$')
        .addConstraint('required-message', 'El nombre es requerido')
        .addConstraint('pattern-message', 'El nombre solo puede contener letras y espacios');

    $('#correo_cli').parsley().addConstraint('required', true)
        .addConstraint('required-message', 'El correo es requerido');

    $('#direccion_cli').parsley().addConstraint('required', true)
        .addConstraint('required-message', 'La dirección es requerida');

    $('#fono').parsley().addConstraint('required', true)
        .addConstraint('type', 'digits')
        .addConstraint('required-message', 'El teléfono es requerido')
        .addConstraint('type-message', 'El teléfono debe contener solo dígitos');

    $('#estatura_cli').parsley().addConstraint('required', true)
        .addConstraint('min', 0)
        .addConstraint('required-message', 'La estatura es requerida')
        .addConstraint('min-message', 'La estatura debe ser un número positivo');
});
