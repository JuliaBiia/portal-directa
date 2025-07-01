{% load static %}


const ModalMensagemErro = Swal.mixin({
    {% comment %} imageUrl: "{% static 'img/icons/icone_atencao.svg' %}",
    imageWidth: 125,
    imageHeight: 125,
    imageAlt: "Custom image", {% endcomment %}
    icon: "warning",
    title: 'Atenção!',
    showConfirmButton: true,
    confirmButtonColor: "#0459A1",
    confirmButtonText: "Ok",
    customClass: {container: 'modal-sweetalert-notificao-usuario'},
});

const ModalConfirmacaoRemocao = Swal.mixin({
    icon: "warning",
    title: 'Atenção!',
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "<i class='fa-solid fa-trash mr-2'></i> Deletar",
    cancelButtonText: "<i class='fa-solid fa-xmark mr-2'></i> Cancelar",
    customClass: {container: 'modal-sweetalert-notificao-usuario', actions: 'swal2-actions-delete', title: 'swal2-title-delete'},
})
