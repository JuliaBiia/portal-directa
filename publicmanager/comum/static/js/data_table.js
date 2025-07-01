$(document).ready(function() {
    $('.myTable').DataTable({
        searching: false,
        lengthChange: false,
        language: {
            info: 'Página _PAGE_ de _PAGES_',
            infoEmpty: 'Nenhum registro encontrado',
            infoFiltered: '(Filtrado de _MAX_ registro no total)',
            zeroRecords: '',
            emptyTable: ''
        },

        layout: {
            bottomEnd: {
                paging: {
                    numbers: 3
                }
            }
        }
    });
});