# Generated by Django 4.2.10 on 2024-07-17 22:23

from django.db import migrations, models
import django.db.models.deletion
import django_lifecycle.mixins
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('saude_enfermagem', '0002_situacaomedicacaoatendimento_cancelado_and_more'),
        ('saude_cadastro', '0003_profissional_cofen'),
        ('saude_atendimento', '0010_alter_historicalpaciente_grau_de_instrucao_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='procedimentoatendimento',
            name='profissional',
        ),
        migrations.AddField(
            model_name='procedimentoatendimento',
            name='justificativa',
            field=models.TextField(blank=True, null=True, verbose_name='justificativa'),
        ),
        migrations.AddField(
            model_name='procedimentoatendimento',
            name='lista_chamada_solicitacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='saude_enfermagem.listachamadasolicitacaoatendimento'),
        ),
        migrations.AddField(
            model_name='procedimentoatendimento',
            name='medico_solicitante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='medico_solicitante_procedimento_atendimento_set', to='saude_cadastro.profissional'),
        ),
        migrations.AddField(
            model_name='procedimentoatendimento',
            name='profissional_responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='profissional_responsavel_procedimento_atendimento_set', to='saude_cadastro.profissional'),
        ),
        migrations.AddField(
            model_name='procedimentoatendimento',
            name='situacao',
            field=models.SmallIntegerField(choices=[(0, 'SOLICITADO'), (1, 'SUSPENSO'), (2, 'CONCLUÍDO')], default=0, verbose_name='Situação'),
        ),
        migrations.AddField(
            model_name='procedimentoatendimento',
            name='tipo_solicitacao',
            field=models.SmallIntegerField(choices=[(0, 'INTERNO'), (1, 'EXTERNO')], default=0, verbose_name='Tipo da Solicitação'),
        ),
        migrations.CreateModel(
            name='JustificativaProcedimentoAtendimento',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Registrado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),
                ('observacao', models.TextField(verbose_name='Observação')),
                ('atendimento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='saude_atendimento.atendimentomedico')),
                ('cid_10_causa_associada', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cid_10_causas_associada_justificativa_procedimento_set', to='saude_cadastro.cid')),
                ('cid_10_principal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cid_10_principal_justificativa_procedimento_set', to='saude_cadastro.cid')),
                ('cid_10_secundario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cid_10_secundario_justificativa_procedimento_set', to='saude_cadastro.cid')),
                ('diagnostico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnostico_justificativa_procedimento_set', to='saude_cadastro.cid')),
                ('procedimentos', models.ManyToManyField(blank=True, to='saude_atendimento.procedimentoatendimento')),
                ('profissional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='saude_cadastro.profissional')),
            ],
            options={
                'verbose_name': 'Justificativa Procedimento Atendimento',
                'verbose_name_plural': 'Justificativas Procedimentos Atendimentos',
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
