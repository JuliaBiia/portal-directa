$(
    function(){
        $('.mask-cpf').mask('ZZZ.ZZZ.ZZZ-ZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-data').mask('ZZ/ZZ/ZZZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-cnpj').mask('ZZ.ZZZ.ZZZ/ZZZZ-ZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-rg').mask('ZZ.ZZZ.ZZZ-Z', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-tituloeleitor').mask('ZZ.ZZZ.ZZZ-ZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-cnh').mask('ZZZ.ZZZ.ZZZ-ZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-cargahoraria').mask('Z', {
            translation: {
              'Z': {
                pattern: /[1-8]/
              }
            }
        });

        $('.mask-cep').mask('ZZZZZ-ZZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-telefone').mask('(ZZ) ZZZZZ-ZZZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-codigodeficiencia').mask('ZZZZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-codigogrupodeficiencia').mask('ZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-codigoibge').mask('ZZZZZZZ', {
            translation: {
              'Z': {
                pattern: /[0-9]/
              }
            }
        });

        $('.mask-hora').mask('AZ:BZ', {
          translation: {
            'A': {
              pattern: /[0-2]/
            },
            'B': {
              pattern: /[0-6]/
            },
            'Z': {
              pattern: /[0-9]/
            }
          }
      });

      $('.mask-telefoneresidencial').mask('(ZZ) ZZZZ-ZZZZ', {
        translation: {
          'Z': {
            pattern: /[0-9]/
          }
        }
      });
      $('.mask-pressao-arterial').on('input', function() {
        let val = $(this).val().replace(/\D/g, '');
        if (val.length > 6) {
            val = val.substring(0, 6);
        }
        if (val.length === 4) {
            val = val.substring(0, 2) + '/' + val.substring(2);
        } else if (val.length === 5) {
            const first3 = parseInt(val.substring(0, 3), 10);
            if (first3 >= 100) {
                val = val.substring(0, 3) + '/' + val.substring(3);
            } else {
                val = val.substring(0, 2) + '/' + val.substring(2);
            }
        } else if (val.length === 6) {
            val = val.substring(0, 3) + '/' + val.substring(3);
        }
        $(this).val(val);
      });
      $('.mask-frequecia-cardiaca').mask('ZZZ', {
        translation: {
            'Z': {
                pattern: /[0-9]/, optional: true
            }
        }
      });
      $('.mask-temperatura').on('input', function() {
        var v = this.value,

        v = v.replace(/\D/, "");
        v = v.replace(/^[0]+/, "");

        if (v.length > 3) {
          v = v[0] + v[1] + '.' + v[2]
        } else {

          if(v.length === 1){
            v = v[0]
          }else if(v.length === 2){
            v = v[0] + v[1]
          }else if(v.length === 3){
            v = v[0] + v[1] + '.' + v[2]
          }else{
            return
          }
        }
        this.value = v;
      });
      $('.mask-altura').on('input', function() {
        let v = this.value.replace(/[^\d]/g, '');
        if (v.length === 1) {
          // Apenas um dígito, não faz nada.
        } else if (v.length === 2) {
          v = v[0] + '.' + v[1];
        } else if (v.length >= 3) {
          v = v.slice(0, v.length - 2) + '.' + v.slice(v.length - 2);
        }
        this.value = v;
      });
      $('.mask-peso').on('input', function() {
        var v = this.value;
    
        // Remove todos os caracteres não numéricos, exceto a vírgula
        v = v.replace(/[^0-9,]/g, '');
    
        // Separa a parte inteira da parte decimal
        var parts = v.split(',');
    
        // Limita a parte decimal a 3 dígitos
        if (parts[1] && parts[1].length > 3) {
            parts[1] = parts[1].substring(0, 3);
        }
    
        // Adiciona a vírgula de volta se houver parte decimal
        if (parts.length > 1) {
            v = parts[0] + ',' + parts[1];
        } else {
            v = parts[0];
        }
    
        // Formata a parte inteira com pontos a cada 3 dígitos
        v = v.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    
        this.value = v;
    });
      $('.mask-data').mask('00/00/0000');

      $('.mask-duracao').mask('00:AB:AB', {
        translation: {
            'A': {
                pattern: /[0-5]/
            },
            'B': {
              pattern: /[0-9]/
          }
        }
      });
    }
);
