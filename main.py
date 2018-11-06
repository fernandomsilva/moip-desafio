import operator, sys, os
import log_parsing_functions as log_parser

log_data = [] # Lista que sera preenchida com os dados do arquivo de log.
filename = "" # String com caminho e nome do arquivo de log, incluindo extensao.
field_name_list = ["request_to", "response_status"] # Lista de campos a serem lidos do arquivo de log.

# Se houver um argumento na execucao do script, use este como o nome do arquivo. Primeiro argumento eh sempre o nome do script.
if len(sys.argv) > 1:
	filename = sys.argv[1]
else:
	# Caso nao haja tal argumento, o usuario deve entrar com o caminho e nome do arquivo (com extensao)
	filename = input("Informe o nome do arquivo de log, com extensao e o caminho para o arquivo: ")
	print("\n")

# Preenchendo a lista com um dicionario para cada entrada do arquivo
if os.path.exists(filename): # Testando se o arquivo existe antes de tentar abrir	
	log_data = log_parser.parse_log_file_string_fields(filename, field_name_list) # Parseando o arquivo
	
	if len(log_data) == 0: # Encerrando a execucao se nao existir nenhuma entrada no arquivo.
		print("Nao ha nenhuma entrada no arquivo.")
		exit()
else: # Encerrando a execucao se o arquivo nao existir
	print("Arquivo", filename, "nao encontrado.")
	exit()

# Separando os dados de request e response em dicionarios individuais
request_dict = {}
response_dict = {}

for data_entry in log_data:
	request = data_entry['request_to']
	response = data_entry['response_status']
	
	# Se o elemento ainda nao existe no dicionario, ele eh criado
	if request not in request_dict:
		request_dict[request] = 1
	# Caso contrario, aumenta-se o contador
	else:
		request_dict[request] += 1
	
	if response not in response_dict:
		response_dict[response] = 1
	else:
		response_dict[response] += 1
	
# Criando uma lista (para cada campo) que representa os dados do dicionario ordenados pelo valor em questao (total de entradas para requests [valor no dicionario] e nome do response para as responses [chave no dicionario])
sorted_requests = sorted(request_dict.items(), key=operator.itemgetter(1), reverse=True)
sorted_responses = sorted(response_dict.items(), key=operator.itemgetter(0))

# Imprimindo as top 3 URLs e a tabela [responses X # de webhooks]
print("Top 3 URLs:\n")
for request_tuple in sorted_requests[:3]:
	print(request_tuple[0] + " - " + str(request_tuple[1]))
	
# Caso o haja candidatos empatados com o ultimo que foi impresso, continua-se a impressao ate encontrar o proximo elemento com valor inferior
# Isto assume que se ha, por exemplo, mais de um elemento empatado em terceiro lugar, que estes tambem pertencem ao top 3
for request_tuple in sorted_requests[3:]:
	if request_tuple[1] == sorted_requests[2][1]:
		print(request_tuple[0] + " - " + str(request_tuple[1]))
	else:
		break
	
print("\n==============")
print("==============\n")
	
print("Tabela de Quantidade de Webhooks por Status:\n")
print("| Status | # Webhooks |")
for response_tuple in sorted_responses:
	print("| " + response_tuple[0] + " | " + str(response_tuple[1]) + " |")