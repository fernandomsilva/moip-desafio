# Funcao parse_log_file_string_fields
# Esta funcao recebe uma string com o caminho para o arquivo de log e uma lista com os nomes dos campos a serem parseados e retorna 
# uma lista de dicionarios, aonde cada dicionario tem os valores dos campos em questao para cada entrada no arquivo de log.
#
# Campos:
#	filename -> string com o caminho para o arquivo de log, incluindo extensao (ex: log/log.txt)
#	field_name_list -> lista com os nomes dos campos a serem parseados
#
# Retorno:
#	Lista de dicionarios. Cada elemento da lista eh um dicionario aonde as chaves serao os nomes dos campos (dado field_name_list)
# e os valores sao os dados parseados de um entrada (linha) do arquivo de log.
#
# ============================================
#
# OBS: Esta funcao parseia apenas campos que estao representados por strings no arquivo de log (notado pelo uso das aspas [""]).
# Como os campos necessarios para o desafio eram do mesmo tipo (string), nao implementei funcionalidade para parsear outro tipo de dado.
# Caso o campo seja de outro tipo que nao string, ele eh ignorado

def parse_log_file_string_fields(filename, field_name_list):
	log_data = []

	file_data = open(filename, 'r')
	for data_row in file_data:
		if all(field + "=" in data_row for field in field_name_list):
			log_data_entry = {}
			for field_name in field_name_list:
				data_row_list_field_parser = data_row.split(field_name + "=")
				data_row_list_field_parser = data_row_list_field_parser[1].split(" ")
				data_row_list_field_parser = data_row_list_field_parser[0].split('"') # Para remover as aspas da string (o item na posicao 1 da lista eh o que queremos)

				if len(data_row_list_field_parser) > 1:
					log_data_entry[field_name] = data_row_list_field_parser[1]
			log_data.append(log_data_entry)

	file_data.close()
	
	return log_data
