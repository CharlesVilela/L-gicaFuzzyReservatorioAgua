import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Declarando as variaveis
nivel_agua = ctrl.Antecedent(np.arange(0, 101, 1), 'nivel_agua')
var_nivel_agua = ctrl.Antecedent(np.arange(-10, 11, 1), 'var_nivel_agua')
vel_bomba_agua = ctrl.Consequent(np.arange(0, 101, 1), 'vel_bomba_agua')

# Definindo as funções de pertinência
#Nivel da água
nivel_agua['baixo'] = fuzz.trimf(nivel_agua.universe, [0, 0, 50])
nivel_agua['medio'] = fuzz.trimf(nivel_agua.universe, [0, 50, 100])
nivel_agua['alto'] = fuzz.trimf(nivel_agua.universe, [50, 100, 100])

# Variação da água
var_nivel_agua['negativo'] = fuzz.trimf(var_nivel_agua.universe, [-10, -10, 0])
var_nivel_agua['neutro'] = fuzz.trimf(var_nivel_agua.universe, [-10, 0, 10])
var_nivel_agua['positivo'] = fuzz.trimf(var_nivel_agua.universe, [0, 10, 10])

# Velocidade da bomba de água
vel_bomba_agua['desligada'] = fuzz.trimf(vel_bomba_agua.universe, [0, 0, 0])
vel_bomba_agua['baixa'] = fuzz.trimf(vel_bomba_agua.universe, [0, 0, 30])
vel_bomba_agua['media'] = fuzz.trimf(vel_bomba_agua.universe, [20, 50, 80])
vel_bomba_agua['alta'] = fuzz.trimf(vel_bomba_agua.universe, [70, 100, 100])

# Definindo as regras
regra1 = ctrl.Rule(nivel_agua['baixo'] & var_nivel_agua['negativo'], vel_bomba_agua['desligada'])
regra2 = ctrl.Rule(nivel_agua['baixo'] & var_nivel_agua['neutro'], vel_bomba_agua['baixa'])
regra3 = ctrl.Rule(nivel_agua['baixo'] & var_nivel_agua['positivo'], vel_bomba_agua['baixa'])

regra4 = ctrl.Rule(nivel_agua['medio'] & var_nivel_agua['negativo'], vel_bomba_agua['baixa'])
regra5 = ctrl.Rule(nivel_agua['medio'] & var_nivel_agua['neutro'], vel_bomba_agua['baixa'])
regra6 = ctrl.Rule(nivel_agua['medio'] & var_nivel_agua['positivo'], vel_bomba_agua['media'])

regra7 = ctrl.Rule(nivel_agua['alto'] & var_nivel_agua['negativo'], vel_bomba_agua['media'])
regra8 = ctrl.Rule(nivel_agua['alto'] & var_nivel_agua['neutro'], vel_bomba_agua['alta'])
regra9 = ctrl.Rule(nivel_agua['alto'] & var_nivel_agua['positivo'], vel_bomba_agua['alta'])

# Criando o sistema de controle
sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6, regra7, regra8, regra9])
sistema_simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Atribuindo valores aos inputs
sistema_simulacao.input['nivel_agua'] = 70
sistema_simulacao.input['var_nivel_agua'] = -5
sistema_simulacao.compute()

# A variável de saída será "velocidade da bomba de água".
print("Velocidade da bomba de água: ", sistema_simulacao.output['vel_bomba_agua'])

# Salvando os gráficos
nivel_agua.view(sim=sistema_simulacao)
plt.savefig('nivel_agua.png', format='png')

var_nivel_agua.view(sim=sistema_simulacao)
plt.savefig('var_nivel_agua.png', format='png')

vel_bomba_agua.view(sim=sistema_simulacao)
plt.savefig('vel_bomba_agua.png', format='png')


