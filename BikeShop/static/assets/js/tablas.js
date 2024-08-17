
$(document).ready(function () {
  // Inicializa la tabla básica con textos en español
  $("#tbl_clientes").DataTable({
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar Cliente:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });

  // Inicializa la tabla con filtros múltiples
  $("#multi-filter-select").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    },
    initComplete: function () {
      this.api().columns().every(function () {
        var column = this;
        var select = $('<select class="form-select"><option value=""></option></select>')
          .appendTo($(column.footer()).empty())
          .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? "^" + val + "$" : "", true, false).draw();
          });

        column.data().unique().sort().each(function (d, j) {
          select.append('<option value="' + d + '">' + d + "</option>");
        });
      });
    }
  });

  // Inicializa la tabla para agregar filas
  $("#add-row").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });
});




$(document).ready(function () {
  // Inicializa la tabla básica con textos en español
  $("#tbl_bicicletas").DataTable({
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar Bicicleta:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });

  // Inicializa la tabla con filtros múltiples
  $("#multi-filter-select").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    },
    initComplete: function () {
      this.api().columns().every(function () {
        var column = this;
        var select = $('<select class="form-select"><option value=""></option></select>')
          .appendTo($(column.footer()).empty())
          .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? "^" + val + "$" : "", true, false).draw();
          });

        column.data().unique().sort().each(function (d, j) {
          select.append('<option value="' + d + '">' + d + "</option>");
        });
      });
    }
  });

  // Inicializa la tabla para agregar filas
  $("#add-row").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });
});




$(document).ready(function () {
  // Inicializa la tabla básica con textos en español
  $("#tbl_mecanicos").DataTable({
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar Mecanico:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });

  // Inicializa la tabla con filtros múltiples
  $("#multi-filter-select").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    },
    initComplete: function () {
      this.api().columns().every(function () {
        var column = this;
        var select = $('<select class="form-select"><option value=""></option></select>')
          .appendTo($(column.footer()).empty())
          .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? "^" + val + "$" : "", true, false).draw();
          });

        column.data().unique().sort().each(function (d, j) {
          select.append('<option value="' + d + '">' + d + "</option>");
        });
      });
    }
  });

  // Inicializa la tabla para agregar filas
  $("#add-row").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });
});





$(document).ready(function () {
  // Inicializa la tabla básica con textos en español
  $("#tbl_detalles").DataTable({
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar Detalles:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });

  // Inicializa la tabla con filtros múltiples
  $("#multi-filter-select").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    },
    initComplete: function () {
      this.api().columns().every(function () {
        var column = this;
        var select = $('<select class="form-select"><option value=""></option></select>')
          .appendTo($(column.footer()).empty())
          .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? "^" + val + "$" : "", true, false).draw();
          });

        column.data().unique().sort().each(function (d, j) {
          select.append('<option value="' + d + '">' + d + "</option>");
        });
      });
    }
  });

  // Inicializa la tabla para agregar filas
  $("#add-row").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });
});









$(document).ready(function () {
  // Inicializa la tabla básica con textos en español
  $("#tbl_repuestos").DataTable({
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar Repuesto:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });

  // Inicializa la tabla con filtros múltiples
  $("#multi-filter-select").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    },
    initComplete: function () {
      this.api().columns().every(function () {
        var column = this;
        var select = $('<select class="form-select"><option value=""></option></select>')
          .appendTo($(column.footer()).empty())
          .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? "^" + val + "$" : "", true, false).draw();
          });

        column.data().unique().sort().each(function (d, j) {
          select.append('<option value="' + d + '">' + d + "</option>");
        });
      });
    }
  });

  // Inicializa la tabla para agregar filas
  $("#add-row").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });
});


















$(document).ready(function () {
  // Inicializa la tabla básica con textos en español
  $("#tbl_categorias").DataTable({
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar Categoria:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });

  // Inicializa la tabla con filtros múltiples
  $("#multi-filter-select").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    },
    initComplete: function () {
      this.api().columns().every(function () {
        var column = this;
        var select = $('<select class="form-select"><option value=""></option></select>')
          .appendTo($(column.footer()).empty())
          .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? "^" + val + "$" : "", true, false).draw();
          });

        column.data().unique().sort().each(function (d, j) {
          select.append('<option value="' + d + '">' + d + "</option>");
        });
      });
    }
  });

  // Inicializa la tabla para agregar filas
  $("#add-row").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });
});












$(document).ready(function () {
  // Inicializa la tabla básica con textos en español
  $("#tbl_productos").DataTable({
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar Productos:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });

  // Inicializa la tabla con filtros múltiples
  $("#multi-filter-select").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    },
    initComplete: function () {
      this.api().columns().every(function () {
        var column = this;
        var select = $('<select class="form-select"><option value=""></option></select>')
          .appendTo($(column.footer()).empty())
          .on("change", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val ? "^" + val + "$" : "", true, false).draw();
          });

        column.data().unique().sort().each(function (d, j) {
          select.append('<option value="' + d + '">' + d + "</option>");
        });
      });
    }
  });

  // Inicializa la tabla para agregar filas
  $("#add-row").DataTable({
    pageLength: 5,
    language: {
      lengthMenu: "Mostrar _MENU_ registros",
      search: "Buscar:",
      info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
      infoEmpty: "Mostrando 0 a 0 de 0 registros",
      infoFiltered: "(filtrado de _MAX_ registros totales)",
      paginate: {
        first: "Primero",
        last: "Último",
        next: "Siguiente",
        previous: "Anterior"
      },
      zeroRecords: "No se encontraron registros coincidentes",
      emptyTable: "No hay datos disponibles en la tabla"
    }
  });
});
