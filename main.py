import operator, sys, os

log_data = []
filename = ""

if len(sys.argv) > 1: # Se houver um argumento na execucao do script, use este como o nome do arquivo. Primeiro argumento eh sempre o nome do script.
	filename = sys.argv[1]
else:
	filename = input("Informe o nome do arquivo de log, com extensao e o caminho para o arquivo: ")
	print("\n")

# Preenchendo a lista com um dicionario para cada entrada do arquivo
if os.path.exists(filename): # Testando se o arquivo existe antes de abrir
	file_data = open(filename, 'r')
	for data_row in file_data:
		if "request_to=" in data_row and "response_status=" in data_row:
			data_row_list_request = data_row.split("request_to=")
			data_row_list_request = data_row_list_request[1].split(" ")
			data_row_list_request = data_row_list_request[0].split('"') #Para remover as aspas da string (o item na posicao 1 da lista eh o que queremos)

			data_row_list_response = data_row.split("response_status=")
			data_row_list_response = data_row_list_response[1].split(" ")
			data_row_list_response = data_row_list_response[0].split('"') #Para remover as aspas da string (o item na posicao 1 da lista eh o que queremos)
			log_data.append({'request': data_row_list_request[1], 'response': data_row_list_response[1]})

	file_data.close()
	
	if len(log_data) == 0: # Encerrando a execucao se nao exister nenhuma entrada no arquivo.
		print("Nao ha nenhuma entrada no arquivo.")
		exit()
else: # Encerrando a execucao se o arquivo nao existir
	print("Arquivo", filename, "nao encontrado.")
	exit()

# Separando os dados de request e response em dicionarios individuais
request_dict = {}
response_dict = {}

for data_entry in log_data:
	request = data_entry['request']
	response = data_entry['response']
	
	if request not in request_dict:
		request_dict[request] = 1
	else:
		request_dict[request] += 1
	
	if response not in response_dict:
		response_dict[response] = 1
	else:
		response_dict[response] += 1
	
# Criando uma lista que representa os dados do dicionario ordenados pelo valor em questao (total de entradas para requests [valor no dicionario] e nome do response para as responses [chave no dicionario])
sorted_requests = sorted(request_dict.items(), key=operator.itemgetter(1), reverse=True)
sorted_responses = sorted(response_dict.items(), key=operator.itemgetter(0))

# Imprimindo as top 3 URLs e a tabela [responses X # de webhooks]
print("Top 3 URLs:\n")
for request_tuple in sorted_requests[:3]:
	print(request_tuple[0] + " - " + str(request_tuple[1]))
	
print("\n==============")
print("==============\n")
	
print("Tabela de Quantidade de Webhooks por Status:\n")
print("| Status | # Webhooks |")
for response_tuple in sorted_responses:
	print("| " + response_tuple[0] + " | " + str(response_tuple[1]) + " |")