# 
# funcoes para calcular o calendario 
#
from datetime import datetime, timedelta
import pandas as pd


diasSemana ={"0":"segunda-feira", "1":"terça-feira", "2":"quarta-feira", "3":"quinta-feira", "4":"sexta-feira"}
DIAFIMSEMANA = 5
SESSOES_COMPLEMENTARES = 15


def gerar_calendario_completo(data_inicial, dia_semana_teorica, carga_horaria_total, carga_teorica_total,
                            horas_teoricas_semana, feriados, ferias, recessos, periodoContinuo,aulasComp, diaSemanaComp, ordemSemanaComp ):

    # Converter as datas iniciais e finais para objetos de data
    data_inicial = datetime.strptime(data_inicial, '%d-%m-%Y')
#    data_inicial = data_inicial
    calendario = []
    aulaTeoricaPendente= False
    teoricaSemana = False
    data_atual = data_inicial
    if aulasComp :
        saldoComplementares = SESSOES_COMPLEMENTARES # numero de sessoes complementares
    else :
        saldoComplementares = 0

    while carga_horaria_total > 0 or carga_teorica_total >0:
        ano_data = data_atual.year
        mes_data = data_atual.month
        dia_data = data_atual.day
        dia_semana = data_atual.weekday()
        data_str = datetime.strftime(data_atual, '%d-%m-%Y')

        teoricaSemana = False # controle de aula teorica na semana

        if not ehferias( data_atual, ferias ) and not ehrecesso( data_str, recessos ) :
          if dia_semana < DIAFIMSEMANA  : # segunda a sexta ?
            if ehferiado( data_str, feriados ) :
                tipo_aula = 'feriado'
            else :
                tipo_aula = ''
            # Verificar se o dia atual é um dia de aula teorica
            if ((dia_semana == dia_semana_teorica) or (dia_semana_teorica ==-1)) and (tipo_aula != 'feriado') :
                if (carga_teorica_total > 0) and (dia_semana < DIAFIMSEMANA) :
                    if not teoricaSemana and not aulaTeoricaPendente :
                        tipo_aula = 't'
                        teoricaSemana = True
                        aulaTeoricaPendente = False
                        carga_teorica_total -= horas_teoricas_semana
                elif dia_semana < DIAFIMSEMANA :
                    tipo_aula = 'p'
                    carga_horaria_total -= horas_teoricas_semana
                    #calendario.append({
                    #    'ano': ano_data,
                    #    'mes': str(mes_data),
                    #    'dia': dia_data,
                    #    'data': data_str,
                    #    'tipo_aula': tipo_aula,
                    #    'dia_semana': str(dia_semana)
                    #    })


                if periodoContinuo :
                    tipo_aula ='i'
            elif (dia_semana < DIAFIMSEMANA ) and (tipo_aula != 'feriado') and (tipo_aula != 't') :
                if carga_horaria_total > 0 :
                    if aulaTeoricaPendente and not teoricaSemana:
                        tipo_aula = 'T'
                        carga_teorica_total -= horas_teoricas_semana
                        aulaTeoricaPendente = False
                        teoricaSemana = True
                    else :
                        tipo_aula = 'p'
                        carga_horaria_total -= horas_teoricas_semana
                elif carga_teorica_total > 0 : # carga horarioa total ja concluiu. Mas ainda não as teoricas
                    tipo_aula = 'f'
                    carga_teorica_total -= horas_teoricas_semana

            if tipo_aula != 'feriado' :
                calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                  })

            if ((dia_semana==dia_semana_teorica or dia_semana_teorica ==-1)) and (tipo_aula == 'feriado' and not periodoContinuo and not aulasComp) :
                # anteceder um dia a aula teorica
                if ( dia_semana <= 2 ) : # se for uma segunda, terca ou quarta com feriado, marcar pendencia
                    if not teoricaSemana :
                        aulaTeoricaPendente = True
                elif ( carga_teorica_total > 0 ) :
                    if not teoricaSemana and not aulaTeoricaPendente : # se nao tem nenhuma hora teorica na semana
                        for i in range(len(calendario)-1, -1, -1):
                            if int(calendario[i]['dia_semana']) >= DIAFIMSEMANA : # se estiver voltando semana, interrompe
                                aulaTeoricaPendente = True
                                break;
                            if calendario[i]['tipo_aula'] == 'p' :
                                aulaTeoricaPendente = False
                                teoricaSemana = True
                                calendario[i]['tipo_aula'] ='T';
                                carga_teorica_total -= horas_teoricas_semana
                                carga_horaria_total += horas_teoricas_semana # incrementar as horas totais para compensar
                                break;

            if tipo_aula == 'feriado' :
                tipo_aula = 'X'
                calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                    })
          else : #final de semana
            tipo_aula ='x'
            teoricaSemana = False
            calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                    })

        else : # se eh ferias ou recesso
            if ehferias( data_atual, ferias ):
                    tipo_aula = 'F'
                    calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                  })
            elif ehrecesso( data_str, recessos ) :
                if dia_semana < DIAFIMSEMANA :
                    if ( dia_semana <= 2 and (dia_semana == dia_semana_teorica)) : # se for uma segunda com recesso, marcar pendencia
                        if not teoricaSemana :
                            aulaTeoricaPendente = True
                    if ((dia_semana==dia_semana_teorica)  and not periodoContinuo) :
                        # anteceder um dia a aula teorica
                        if ( carga_teorica_total > 0 and not aulaTeoricaPendente and not teoricaSemana ) :
                            for i in range(len(calendario)-1, -1, -1):
                                if int(calendario[i]['dia_semana']) >= DIAFIMSEMANA : # se estiver voltando na semana anterior, interromper
                                    aulaTeoricaPendente = True
                                    break;
                                if calendario[i]['tipo_aula'] == 'p' :
                                    aulaTeoricaPendente = False
                                    teoricaSemana = True
                                    calendario[i]['tipo_aula'] ='T';
                                    carga_teorica_total -= horas_teoricas_semana
                                    carga_horaria_total += horas_teoricas_semana # incrementar as horas totais para compensar
                                    break;
                    if carga_horaria_total > 0 :
                        tipo_aula = 'r' # recesso - dia de atividade pratica
                        carga_horaria_total -= horas_teoricas_semana
                        calendario.append({
                          'ano': ano_data,
                          'mes': str(mes_data),
                          'dia': dia_data,
                          'data': data_str,
                          'tipo_aula': tipo_aula,
                          'dia_semana': str(dia_semana)
                        })

                    elif periodoContinuo :
                        tipo_aula = 'X'
                        calendario.append({
                              'ano': ano_data,
                              'mes': str(mes_data),
                              'dia': dia_data,
                              'data': data_str,
                              'tipo_aula': tipo_aula,
                              'dia_semana': str(dia_semana)
                            })
                    else : # nao eh periodo continuo mas eh recesso e aulas totais ja terminaram
                        # carga_teorica_total -= horas_teoricas_semana
                        tipo_aula = 'r' # recesso - dia de atividade pratica
                        # carga_horaria_total += horas_teoricas_semana # incrementar as horas totais para compensar
                        calendario.append({
                            'ano': ano_data,
                            'mes': str(mes_data),
                            'dia': dia_data,
                            'data': data_str,
                            'tipo_aula': tipo_aula,
                            'dia_semana': str(dia_semana)
                            })

                else : # final de semana
                    tipo_aula ='x'
                    calendario.append({
                      'ano': ano_data,
                      'mes': str(mes_data),
                      'dia': dia_data,
                      'data': data_str,
                      'tipo_aula': tipo_aula,
                      'dia_semana': str(dia_semana)
                    })

        # verificar horas complementares
        if ehcomplementar( dia_semana, dia_data, saldoComplementares,diaSemanaComp, ordemSemanaComp) :
            if calendario[-1]["tipo_aula"] == 'p' :
                calendario[-1]["tipo_aula"] = 'c' # aula complementar
                carga_teorica_total -= horas_teoricas_semana
                carga_horaria_total -= horas_teoricas_semana
                saldoComplementares -= 1

        if dia_semana >= DIAFIMSEMANA : # tentativa correcao situacao recesso dezembro - 2/1
            aulaTeoricaPendente = False
            teoricaSemana = False

        # Avançar para o próximo dia
        data_atual += timedelta(days=1)
      #  data_atual = datetime.strptime(data_atual, '%d-%m-%Y')


    data_final = data_atual - timedelta(days=1)
    return calendario, data_final
# -----------------------------------------------------------------------------------
def mostrar_calendario(calendario, chdia):
    meses = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
        ]

    dia_semanaExtenso=['seg','ter','qua','qui','sex','sab','dom']
    dias = len(calendario)
    posicao = 0
    totalTeoricas = 0
    totalPraticas = 0
    resultados = []

    while posicao < dias:
        data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
        mes_atual = data_atual.month
        mudames = False
        teoricas, praticas = 0, 0
        resultado = f"{meses[mes_atual-1]};{data_atual.year};"

        while mudames == False and posicao < dias:
            data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
            dia_semana = dia_semanaExtenso[int(calendario[posicao]['dia_semana'])]
            tipo_aula = calendario[posicao]['tipo_aula']

            if posicao >= dias or data_atual.month != mes_atual:
                mudames = True
                break

            if tipo_aula == 't':
                teoricas += 1
                tipo_aula = 't'
            else:
                praticas += 1
                tipo_aula = 'p'

            resultado += f"{str(data_atual.day)}-{str(dia_semana)}-{str(tipo_aula)};"

            posicao += 1

        #resultado += f"Teoricas {meses[mes_atual-1]};{str(teoricas)};Praticas {meses[mes_atual-1]};{str(praticas)};Total;{(teoricas+praticas)*chdia}"
        resultado += f"{(teoricas+praticas)*chdia}"

        resultados.append(resultado)

        totalTeoricas += teoricas * chdia
        totalPraticas += praticas * chdia

    return totalTeoricas, totalPraticas, resultados
# -----------------------------------------------------------------------------------
def mostrar_calendarioCompleto(calendario, chdia):
    meses = [
        'Janeiro',
        'Fevereiro',
        'Março',
        'Abril',
        'Maio',
        'Junho',
        'Julho',
        'Agosto',
        'Setembro',
        'Outubro',
        'Novembro',
        'Dezembro'
        ]

    dia_semanaExtenso=['2ª','3ª','4ª','5ª','6ª','s','d']
    dias = len(calendario)
    posicao = 0
    totalTeoricas = 0
    totalPraticas = 0
    resultados = []

    while posicao < dias:
        data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
        mes_atual = data_atual.month
        mudames = False
        teoricas, praticas = 0, 0
        resultado = f"{meses[mes_atual-1]};{data_atual.year};"

        while mudames == False and posicao < dias:
            data_atual = datetime.strptime(calendario[posicao]['data'], '%d-%m-%Y')
            dia_semana = dia_semanaExtenso[int(calendario[posicao]['dia_semana'])]
            tipo_aula = calendario[posicao]['tipo_aula']

            if posicao >= dias or data_atual.month != mes_atual:
                mudames = True
                break

            if tipo_aula == 't':    # aulas teoricas
                teoricas += 1
            if tipo_aula == 'c':    # aulas complementares
                teoricas += 1
            if tipo_aula == 'T' :   # aulas de reposicao praticas
                teoricas += 1
            if tipo_aula == 'i' :   # aulas teoricas iniciais
                teoricas += 1
            if tipo_aula == 'f' :   # aulas teoricas finais
                teoricas += 1
            if tipo_aula == 'p':    # aulas praticas na empresa
                praticas += 1
            if tipo_aula == 'r' :   # recesso
                praticas += 1

            resultado += f"{str(data_atual.day)}-{str(dia_semana)}-{str(tipo_aula)};"

            posicao += 1

        resultado += f"{str(teoricas)};{str(praticas)};{(teoricas+praticas)*chdia}"
        # resultado += f"{(teoricas+praticas)*chdia}"

        resultados.append(resultado)

        totalTeoricas += teoricas * chdia
        totalPraticas += praticas * chdia

    return totalTeoricas, totalPraticas, resultados
# ------------------------------------------------------------
def listaFeriados( df,  nacional, estadual, municipal):
    df_nacional=df.loc[df['local'] == nacional ].reset_index()
    df_estadual=df.loc[df['local'] == estadual ].reset_index()
    df_municipal=df.loc[df['local'] == municipal ].reset_index()
    feriados =[]

    if not df_nacional.empty:
        for i in range(len(df_nacional)):
            if isinstance(df_nacional['feriados'][i], str):  # Verifica se o valor não é NaN
                feriados.extend(df_nacional['feriados'][i].split(','))
    if not df_estadual.empty:
        for i in range(len(df_estadual)):
            if isinstance(df_estadual['feriados'][i], str):  # Verifica se o valor não é NaN
                feriados.extend(df_estadual['feriados'][i].split(','))
    if not df_municipal.empty:
        for i in range(len(df_municipal)):
            if isinstance(df_municipal['feriados'][i], str):  # Verifica se o valor não é NaN
                feriados.extend(df_municipal['feriados'][i].split(','))
    return feriados



# ------------------------------------------------------------
def listaRecessos( df,  recesso):
  df_recesso=df.loc[df['local'] == recesso ].reset_index()
  recessos =[]
  for i in range( len(df_recesso)) :
    recessos.extend( df_recesso['feriados'][i].split(','))
  return recessos
# ------------------------------------
def ehferias ( data, ferias):
  if len(ferias[0]) == 0 :
      return False
  if data >= datetime.strptime(ferias[0], '%d-%m-%Y') and data <= datetime.strptime(ferias[1], '%d-%m-%Y'):
      return True
  else :
      return False
# ----------------------------------
def ehferiado( data, feriados ):
  for i in range( len(feriados)):
 #   if datetime.strptime(data,"%d-%m-%Y") == datetime.strptime(feriados[i],"%d-%m-%Y") :
    if datetime.strptime(data,"%d-%m-%Y") == datetime.strptime(feriados[i],"%d-%m-%Y") :
      return True
  return False
# ------------------------------------
def ehrecesso ( data, recesso):
  for i in range(len(recesso)) :
#    if datetime.strptime(data, "%d-%m-%Y") == datetime.strptime(recesso[i],"%d-%m-%Y") :
    if datetime.strptime(data,"%d-%m-%Y") == datetime.strptime(recesso[i],"%d-%m-%Y") :
      return True
  return False
# -----------------------------------------
def ehcomplementar( semana, dia, saldoComplementares,diaSemanaComp, ordemSemanaComp) :
    if saldoComplementares > 0:
       calculoSemana = int(dia / 7) +1 # calculando a semana
       if calculoSemana == ordemSemanaComp :
           if semana == diaSemanaComp :
               return True
    return False
