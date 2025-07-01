const getProdutoMedico = produtoID => {
    return new Promise (async (resolve, reject) => {
        try{
            const resp = await fetch(url_produto_medico_detalhes.replace("00000000-0000-0000-0000-000000000000", produtoID))

            if (resp.status === 200){
                const data = await resp.json();

                resolve(data)
            } else if (resp.status === 404){
                reject({'status-code': 404, 'status-message': "Não foi possível encontrar o produto médico. Entre em contato com o suporte para eles verificarem o motivo do problema."});
            }
        } catch(err){
            reject({'status-code': 400, 'status-message': `Erro ao obter dados do produto médico de id ${produtoID}: ${err}`});
        }
    })
};

const getMedicamento = medicamentoID => {
    return new Promise (async (resolve, reject) => {
        try{
            const resp = await fetch(url_medicamento_detalhes.replace("00000000-0000-0000-0000-000000000000", medicamentoID))

            if (resp.status === 200){
                const data = await resp.json();

                resolve(data)
            } else if (resp.status === 404){
                reject({'status-code': 404, 'status-message': "Não foi possível encontrar o medicamento. Entre em contato com o suporte para eles verificarem o motivo do problema."});
            }
        } catch(err){
            reject({'status-code': 400, 'status-message': `Erro ao obter dados do medicamento de id ${medicamentoID}: ${err}`});
        }
    })
};

const getInsumo = insumoID => {
    return new Promise (async (resolve, reject) => {
        try{
            const resp = await fetch(url_insumo_detalhes.replace("00000000-0000-0000-0000-000000000000", insumoID))

            if (resp.status === 200){
                const data = await resp.json();

                resolve(data)
            } else if (resp.status === 404){
                reject({'status-code': 404, 'status-message': "Não foi possível encontrar o insumo. Entre em contato com o suporte para eles verificarem o motivo do problema."});
            }
        } catch(err){
            reject({'status-code': 400, 'status-message': `Erro ao obter dados do insumo de id ${insumoID}: ${err}`});
        }
    })
};