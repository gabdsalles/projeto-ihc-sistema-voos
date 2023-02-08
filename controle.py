from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import mysql.connector
import sys

banco = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123456",
    database = "teste"
)

def chama_menu_aviao():
    telaMenuAviao.show()
    telaInicial.close()
    tabela_aviao()

def chama_menu_voo():
    telaMenuVoo.show()
    telaInicial.close()
    tabela_voos()

def tabela_aviao():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM avioes"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    telaMenuAviao.tableWidget.setRowCount(len(dados_lidos))
    telaMenuAviao.tableWidget.setColumnCount(5)
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            telaMenuAviao.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
def tabela_voos():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM voos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    telaMenuVoo.tableWidget.setRowCount(len(dados_lidos))
    telaMenuVoo.tableWidget.setColumnCount(7)
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 7):
            telaMenuVoo.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j+1])))

def chama_tela_aviao():
    telaAviao.show()
    telaMenuAviao.close()

def chama_tela_voos():
    telaVoo.show()
    telaMenuVoo.close()

def voltar_voo():
    telaMenuVoo.show()
    telaVoo.close()
    tabela_voos()

def voltar_aviao():
    telaMenuAviao.show()
    telaAviao.close()
    tabela_aviao()

def voltar_aviao_inicial():
    telaInicial.show()
    tabela_aviao()
    telaMenuAviao.close()

def voltar_voo_inicial():
    telaInicial.show()
    telaMenuVoo.close()

def obter_dados_aviao():
  
    numeroRegistro = telaAviao.lineEdit.text()
    modelo = telaAviao.lineEdit_2.text()
    qtdAssentos = telaAviao.lineEdit_3.text()
    qtdAssentosEsp = telaAviao.lineEdit_4.text()

    if numeroRegistro == "" and modelo == "" and qtdAssentos == "" and qtdAssentosEsp == "":
        QMessageBox.about(telaAviao, "Cadastro", "Preencha todos os dados!!")
        telaAviao.show()
        
    else:
        cursor = banco.cursor()
        comando_SQL = "INSERT INTO avioes (numeroRegistro, modelo, qtdAssentos, qtdAssentosEspeciais) VALUES (%s,%s,%s,%s)"

        dados = (str(numeroRegistro), str(modelo), str(qtdAssentos), str(qtdAssentosEsp))
        cursor.execute(comando_SQL,dados)
        banco.commit()

        QMessageBox.about(telaAviao, "Cadastro", "Cadastro realizado com sucesso!")


    telaAviao.lineEdit.setText("")
    telaAviao.lineEdit_2.setText("")
    telaAviao.lineEdit_3.setText("")
    telaAviao.lineEdit_4.setText("")

def obter_dados_voo():
    numeroVoo = telaVoo.lineEdit.text()
    temp_var = telaVoo.dateEdit.date() 
    data = temp_var.toPyDate()
    temp_var2 = telaVoo.timeEdit.time()
    horario = temp_var2.toPyTime()
    origem = telaVoo.lineEdit_3.text()
    destino = telaVoo.lineEdit_4.text()
    valorNormal = telaVoo.lineEdit_2.text()
    valorEsp = telaVoo.lineEdit_5.text()

    if numeroVoo == "" and origem == "" and destino == "" and valorNormal == "" and valorEsp == "":
        QMessageBox.about(telaVoo, "Cadastro", "Preencha todos os dados!!")

    else:
        cursor = banco.cursor()
        comando_SQL = "INSERT INTO voos (numeroVoo, data, horario, origem, destino, valorNormal, valorEspecial) VALUES (%s,%s,%s,%s,%s,%s,%s)"

        dados = (str(numeroVoo), str(data), str(horario), str(origem), str(destino), str(valorNormal), str(valorEsp))
        cursor.execute(comando_SQL,dados)
        banco.commit()

        QMessageBox.about(telaVoo, "Cadastro", "Cadastro realizado com sucesso!")

        telaVoo.lineEdit.setText("")
        telaVoo.lineEdit_2.setText("")
        telaVoo.lineEdit_3.setText("")
        telaVoo.lineEdit_4.setText("")
        telaVoo.lineEdit_5.setText("")

def excluir_dados_aviao():
    linha_atual = telaMenuAviao.tableWidget.currentRow()
    telaMenuAviao.tableWidget.removeRow(linha_atual)

    cursor = banco.cursor()
    cursor.execute("select id from avioes")
    dados_lidos = cursor.fetchall()
       
    valor_id = dados_lidos[linha_atual][0]
    cursor.execute("delete from avioes where id = " + str(valor_id))
    banco.commit()
    telaExcluirAviao.close()

def excluir_aviao():
    
    telaExcluirAviao.show()
    telaExcluirAviao.pushButton.clicked.connect(excluir_dados_aviao)
    telaExcluirAviao.pushButton_2.clicked.connect(fechar_tela_aviao)

def fechar_tela_aviao():
    telaExcluirAviao.close()

def excluir_dados_voo():
    linha_atual = telaMenuVoo.tableWidget.currentRow()
    telaMenuVoo.tableWidget.removeRow(linha_atual)

    cursor = banco.cursor()
    cursor.execute("select id from voos")
    dados_lidos = cursor.fetchall()

    valor_id = dados_lidos[linha_atual][0]

    cursor.execute("delete from voos where id = " + str(valor_id))
    valor_id = 0
    banco.commit()
    telaExcluirVoo.close()

def excluir_voo():
    
    telaExcluirVoo.show()
    telaExcluirVoo.pushButton.clicked.connect(excluir_dados_voo)
    telaExcluirVoo.pushButton_2.clicked.connect(fechar_tela_voo)

def fechar_tela_voo():
    telaExcluirVoo.close()

def editar_aviao():
    
    global numero_id
    linha = telaMenuAviao.tableWidget.currentRow()
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM avioes")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM avioes WHERE id="+ str(valor_id))
    aviao = cursor.fetchall()
    telaEditarAviao.show()


    telaEditarAviao.lineEdit.setText(str(aviao[0][1]))
    telaEditarAviao.lineEdit_2.setText(str(aviao[0][2]))
    telaEditarAviao.lineEdit_3.setText(str(aviao[0][3]))
    telaEditarAviao.lineEdit_4.setText(str(aviao[0][4]))

    numero_id = valor_id

def salvar_aviao():

    numRegistro = telaEditarAviao.lineEdit.text()
    modelo = telaEditarAviao.lineEdit_2.text()
    qtdAssentos = telaEditarAviao.lineEdit_3.text()
    qtdAssentosEsp = telaEditarAviao.lineEdit_4.text()

    cursor = banco.cursor()
    cursor.execute("UPDATE avioes SET numeroRegistro = '{}', modelo = '{}', qtdAssentos = '{}', qtdAssentosEspeciais ='{}' WHERE id = {}".format(numRegistro, modelo, qtdAssentos, qtdAssentosEsp , numero_id))
    banco.commit()

    QMessageBox.about(telaEditarAviao, "Editar", "Edição concluída com sucesso!")

    telaEditarAviao.close()
    telaMenuAviao.close()
    chama_menu_aviao()

def editar_voo():

    global numero_id2
    linha = telaMenuVoo.tableWidget.currentRow()
    cursor = banco.cursor()
    cursor.execute("SELECT id FROM voos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM voos WHERE id="+ str(valor_id))
    voo = cursor.fetchall()


    telaEditarVoo.show()

    telaEditarVoo.lineEdit.setText(str(voo[0][1]))
    telaEditarVoo.lineEdit_2.setText(str(voo[0][2]))
    telaEditarVoo.lineEdit_7.setText(str(voo[0][3]))
    telaEditarVoo.lineEdit_3.setText(str(voo[0][4]))
    telaEditarVoo.lineEdit_4.setText(str(voo[0][5]))
    telaEditarVoo.lineEdit_5.setText(str(voo[0][6]))
    telaEditarVoo.lineEdit_6.setText(str(voo[0][7]))

    numero_id2 = valor_id

def salvar_voo():
    numVoo = telaEditarVoo.lineEdit.text()
    data = telaEditarVoo.lineEdit_2.text()
    horario = telaEditarVoo.lineEdit_7.text()
    origem = telaEditarVoo.lineEdit_3.text()
    destino = telaEditarVoo.lineEdit_4.text()
    valorNormal = telaEditarVoo.lineEdit_5.text()
    valorEspecial = telaEditarVoo.lineEdit_6.text()

    cursor = banco.cursor()
    cursor.execute("UPDATE voos SET numeroVoo = '{}', data = '{}', horario = '{}', origem ='{}', destino = '{}', valorNormal = '{}', valorEspecial = '{}' WHERE id = {}".format(numVoo, data, horario, origem, destino, valorNormal, valorEspecial, numero_id2))
    banco.commit()

    QMessageBox.about(telaEditarVoo, "Editar", "Edição concluída com sucesso!")

    telaEditarVoo.close()
    telaMenuVoo.close()
    chama_menu_voo()


app=QtWidgets.QApplication([])
telaInicial = uic.loadUi("telainicial.ui")
telaMenuAviao = uic.loadUi("menu_aviao.ui")
telaMenuVoo = uic.loadUi("menu_voo.ui")
telaAviao = uic.loadUi("tela_cadastrar_aviao.ui")
telaVoo = uic.loadUi("tela_cadastrar_voos.ui")
telaExcluirAviao = uic.loadUi("aviso_excluir_aviao.ui")
telaExcluirVoo = uic.loadUi("aviso_excluir_voo.ui")
telaEditarAviao = uic.loadUi ("editar_aviao.ui")
telaEditarVoo = uic.loadUi("editar_voo.ui")

telaInicial.botao_aviao.clicked.connect(chama_menu_aviao)
telaInicial.botao_voo.clicked.connect(chama_menu_voo)

telaMenuAviao.botao_cadastrar_aviao.clicked.connect(chama_tela_aviao)
telaMenuAviao.botao_excluir.clicked.connect(excluir_aviao)
telaMenuAviao.botao_editar.clicked.connect(editar_aviao)
telaEditarAviao.pushButton.clicked.connect(salvar_aviao)
telaMenuAviao.botao_voltar.clicked.connect(voltar_aviao_inicial)

telaMenuVoo.botao_cadastrar_voo.clicked.connect(chama_tela_voos)
telaMenuVoo.botao_excluir.clicked.connect(excluir_voo)
telaMenuVoo.botao_editar.clicked.connect(editar_voo)
telaEditarVoo.pushButton.clicked.connect(salvar_voo)
telaMenuVoo.botao_voltar.clicked.connect(voltar_voo_inicial)

telaAviao.botao_voltar.clicked.connect(voltar_aviao)
telaVoo.botao_voltar.clicked.connect(voltar_voo)

telaAviao.botao_cadastrar_aviao.clicked.connect(obter_dados_aviao)
telaVoo.botao_cadastrar_voo.clicked.connect(obter_dados_voo)

telaInicial.show()
app.exec()