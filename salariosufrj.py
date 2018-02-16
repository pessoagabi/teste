#PARA GRAVAR NUM ARQUIVO, EM VEZ DE IMPRIMIR NOME E SALÁRIO NA TELA. TROCO O PRINT (NOME) E PRINT (VALOR) POR nome = a.string e valor = valor.string; além da função f.write(f'...)

import requests
from bs4 import BeautifulSoup as bs

for k in range (9,1003):
    f = open('ufrj.txt', 'a')
#o f=open cria um arquivo para salvar a raspagem. tenho que abrir o arquivo antes de acessar a página e fechar logo depois da página.
#o a, acima, é o append: se cair a conexão, não perco as páginas anteriores que eu gravei    
    url1 = "http://www.portaldatransparencia.gov.br/servidores/OrgaoLotacao-ListaServidores.asp?CodOS=15000&DescOS=MINISTERIO%20DA%20EDUCACAO&CodOrg=26245&DescOrg=UNIVERSIDADE%20FEDERAL%20DO%20RIO%20DE%20JANEIRO&Pagina="+str(k)
    #Acima, o +str(k) serve para pegar várias páginas ao mesmo tempo
    html = requests.get(url1)
    sopa = bs(html.content, "html.parser")
    print ('Página', k)
#o print acima irá me avisar em qual página está a raspagem
    salarios = sopa.findAll("table")

    itens = salarios[1].findAll('tr')

    for s in itens[1:]:
        a = s.find('a')
        nome = a.string
#em vez de dar nome do servidor, agora eu vou salvar. crio uma variável ///
        
        link = a['href']
        inicio = link.find("=") + 1
        final = link.find("&")
        cod = link[inicio:final]
#mudei cod, variável para enfiar na string da url
        url = "http://www.portaldatransparencia.gov.br/servidores/Servidor-DetalhaRemuneracao.asp?Op=3&IdServidor="+cod+"&CodOS15000&CodOrgao=26245&bInformacaoFinanceira=True&Ano=2017&Mes=9"
#substituí o codigo do servidor no link acima pela variável cod
        p = requests.get(url)
        sopa = bs(p.content, 'html.parser')
#coloco o if na linha abaixo pq já tenho todo o conteudo raspado e mastigado
        if 'Total da Remuneração Após Deduções' in str(sopa):
            tabelas = sopa.findAll('table')
            itens = tabelas[1].findAll('tr', {'class':'remuneracaodetalhe'})
            valor = itens[2].find('td', {'class':'colunaValor'})
            #coloco chave porque tinha vários tr, sempre dicionários para class ou span
            valor = valor.string
            #sempre que coloco o string, ele despreza a tag
            f.write(f'{cod}, {nome}, {valor}\n')
        else:
            f.write(f'{cod}, {nome}, 0.00\n')
            print ('Funcionário', cod, 'sem remuneração disponível')
    f.close()
