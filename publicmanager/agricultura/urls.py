from django.urls import path

from .views import TipoProdutorListView, TipoProdutorCreateView, TipoProdutorUpdateView, TipoProdutorDeleteView

app_name = 'agricultura'

urlpatterns = [

    ## TipoProdutor
    path('tipoprodutor/', TipoProdutorListView.as_view(), name='tipoprodutor_list'),
    path('tipoprodutor/add/', TipoProdutorCreateView.as_view(), name='tipoprodutor_add'),
    path('tipoprodutor/update/<pk>', TipoProdutorUpdateView.as_view(), name='tipoprodutor_update'),
    path('tipoprodutor/delete/<pk>', TipoProdutorDeleteView.as_view(), name='tipoprodutor_delete'),

]
