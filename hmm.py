
# پياده سازي مدل مخفي مارکوف با استفاده از الگوريتم هاي فوروارد، بکوارد و با ومولچ براي مثال کيسه و مهره


#################### دريافت دنباله مضاهدات و تعداد حالت ها از ورودي

states = int(input("Enter the number of your states: "))
#observations = int(input("Enter the number of your observations: "))
output1 = input("Enter the sequence of observations by space: ").split()
output = []
n = -1
for out in range(len(output1)):
    output.append(output1[n])
    n -= 1


string_to_num = []
for str in output:
    if str not in string_to_num:
        string_to_num.append(str)
#print(string_to_num)
        
#################### وارد کردن مقادير اوليه براي مدل مخفي مارکوف         
'''
#matrix_P = []
#for i in range(states):
#	matrix_P.append([float(x) for x in input('Type an element of matrix_P and click enter: ')])
#print()

#matrix_A = []
#for i in range(0, states):
#    matrix_A.append([float(x) for x in input("Enter elements of row = " + str(i+1) + " of matrix_A by space: ").split()])
#print()

'''

####take p_matrix from the user in one row
nn_matrix = input ("enter the numbers to make matrix_p: "). split()
total_cells = len(nn_matrix)
#### calculate 'n'
row_cells = int(total_cells** 0.5)
####calculate rows
matrix_P = [nn_matrix[i:i+ row_cells] for i in range(0, total_cells, row_cells)]
for i in range(len(matrix_P)):
    for j in range(len(matrix_P[i])):
        matrix_P[i][j] = float(matrix_P[i][j]) 
print('matrix_P= ', matrix_P)
matrix_B = {}
matrix_B = {(0, 'red'): .6, (1,'red'): .5, (2,'red'): .3, (0, 'blue'): .6, (1, 'blue'): .5, (2, 'blue'): .3}
print('matrix_B= ', matrix_B)
### take matrix_A from the user in one row
nn_matrix_1= input(" enter the numbers to make matrix_A: ").split()
total_cells_1 =len(nn_matrix_1)
#### calculate 'n'
row_cells_1 = int(total_cells_1**0.5)
####calculate rows
matrix_A= [nn_matrix_1[j:j+ row_cells_1] for j in range (0, total_cells_1, row_cells_1)]
for i in range(len(matrix_A)):
    for j in range(len(matrix_A)):
        matrix_A[i][j]=float(matrix_A[i][j])
        
print('matrix_A= ', matrix_A)

########################################## forward algorithm ########################################
                            
alpha = []
alphas = []
flag = 0
n = 0
for observation in output1:                      
    next_alpha = []
    if flag == 0:
################## Initialization ####
        for Q in range(states):
            alpha.append(matrix_P[Q][0] * matrix_B[(Q, observation)])
        alphas.append(alpha)
        flag = 1
####################### Induction ####    
    elif flag != 0:
        for q in range(states):
            temp = 0
            for Q in range(states):
                temp = temp + (alphas[n][Q] * matrix_A[Q][q])
            next_alpha.append(temp * matrix_B[(q, observation)])
        alphas.append(next_alpha)
        n += 1
    
##################### Termination ####            
summ = 0
for a in range(states):
    summ = summ + alphas[-1][a]
print('alphas', alphas)
print('P(O) by foreward= ', summ)
print()


################################################# backward algorithm ################################

######### Initialization ###############                            
beta = [1 for i in range(states)]
betas = []
betas.append(beta)
flag = 0
flag2 = 0
n = 0
summ2 = 0.0
for observation in output:                     
    pervious_beta = []
    if flag2 == 0:
        for q in range(states):
            temp = 0
            for Q in range(states):
                if flag == 0:
                    temp = temp + (matrix_A[q][Q] * matrix_B[(Q, observation)] * beta[Q])     
################ Induction #############
                else:
                    temp = temp + (matrix_A[q][Q] * matrix_B[(Q, observation)] * betas[n][Q])
            pervious_beta.append(temp)
        n += 1
        betas.append(pervious_beta)
        #print('betas=  ', betas)
        flag = 1
    
############# Termination #############
    if n == len(output)-1:
        flag2 = 1
for a in range(states):
    summ2 = summ2 + (matrix_P[a][0] * matrix_B[(a, output[-1])] * betas[-1][a])
print('betas', betas)
print('P(O) by backward= ', summ2)

############################# gama calculations for baum welch algorithm#################################

right_betas = []
n = -1
for beta in range(len(betas)):
    right_betas.append(betas[n])
    n -= 1
    

gamas = []
for i in range(len(output1)):
    gama = []
    for j in range(states):    #گاما را با استفاده از پارامترهاي آلفا و بتا محاسبه مي کنيم
        gama.append(alphas[i][j] * betas[i][j])
    diametere = 0
    for k in gama:
        diametere = diametere + k
    gamas.append([x/diametere for x in gama])
print()
print('gamas',gamas)
    

################################ zeta #################################
'''
zeta = []
zetas = []
final_zeta = []
final_zetas = []
diameter = 0
for i in range(states):
    for j in range(states):
        for t in range(len(output1)):
            zeta.append(alphas[i][t] * matrix_A[i][j] * matrix_B[(j, output1[t])] * betas[j][t+1])
            diameter = diameter + (alphas[i][t] * matrix_A[i][j] * matrix_B[(j, output1[t])] * betas[j][t+1])
    zatas.append(zeta)

for i in zetas:
    for j in i:
        final_zeta.append(j / diametere)
    final_zatas.append(final_zeta)
print()
print('zetas',final_zetas)

'''

print()
E_gama = []
for i in gamas:
    var = 0
    for j in range(states):    #اميد رياضي تعداد پرش ها از حالت آي به حالت هاي ديگر
        var = var + i[j]
    E_gama.append(var)
print('omid_gama', E_gama)
print()

######### پارامتر زتا طبق فرمول محاسبه مي کنيم
zeta2 = []
zetas = []
n = 0
for t in output1:
    zeta1 = []
    for i in range(states):
        zeta = []
        for j in range(states):
            zeta.append(alphas[n][j] * matrix_A[i][j] * matrix_B[(j, t)] * betas[n][j])
            #print("running")
        zeta1.append(zeta)
    zeta2.append(zeta1)
    n += 1
#print('zeta2', zeta2)    
   
summ_zeta = 0
for i in zeta2:
    for j in i:
        for x in j:
            summ_zeta = summ_zeta + x
print()


########################## M ###################################

#### مرحله ام از الگوريتم بام ولچ براي محاسبه پارامترهاي جديد
## محاسبه ماتريس جديد پرش بين حالات
new_A1 = []
for i in range(len(output1)):
    new_A = []
    for j in range(states):
        E_zeta = 0
        for k in range(states):
            E_zeta = E_zeta + (zeta2[i][j][k]/ summ_zeta)
        new_A.append(E_zeta / E_gama[i]) # اميد رياضي تعداد پرش ها از حالت آي به حات جي
    new_A1.append(new_A)
print('new matrix A', new_A1)
print()

new_P = gamas[0]
print('new matrix P', new_P)
print()

##### محاسبه ماتريس جديد احتمال رخداد خروجي ها
new_B = []
new_B1 = []
for i in range(states):
    n = 0
    for j in string_to_num:
        gama = 0
        for k in range(states):
            if j == output1[k]:
                gama = gama + gamas[k][n]
        new_B.append(gama / E_gama[i])
        n += 1
    new_B1.append(new_B)
new_B2 = new_B1[0]
print('new matrix B', new_B2)



    


        


        

