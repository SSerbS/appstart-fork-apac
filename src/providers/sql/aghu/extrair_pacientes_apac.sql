SELECT 
    cns_paciente, 
    nome_paciente, 
    data_atendimento, 
    texto_evolucao 
FROM agh.evolucoes_alta_complexidade 
WHERE data_atendimento = :data_alvo;
