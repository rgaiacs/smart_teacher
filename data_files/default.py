# use execfile('default.py') from interpreter
from smart_teacher.sheet.models import *
from smart_teacher.smartqands.models import *
from smart_teacher.qands.models import *
from django.contrib.auth.models import User

user = User.objects.create_user('guest', 'r.gaia.cs@gmail.com', 'guest')
user.save()

s = SmartQAndS(arg='x1=input_box(default=-1, label="solucao 1", type=int), '
            'x2=input_box(default=-2, label="solucao 2", type=int), '
            'auto_update=False',
        question='print "Determinar os zeros reais de $" + latex(x^2 + (x1 + x2) * x + (x1 * x2)) + "$."',
        solution='print "Solucao: $x_1 = " + str(x1) + "$ e $x_2 = " + str(x2) + "$."')
s.save()

s = SmartQAndS(arg='c=input_box(default=20000, label="capital", type=float), '
            't=input_box(default=2, label="tempo", type=float), '
            'j=input_box(default=2, label="taxa de juros", type=float), '
            'auto_update=False',
        question='print "Um capital de R$" + str(c) + " e aplicado a juros simples durante " + str(t) + " anos, a taxa de " + str(j) + "% a.m. Qual o montante obtido?"\n'
            'r = c * (1 + j / 100) * (t * 12)',
        solution='print "Solucao: R$" + str(r)')

s = SmartQAndS(arg='l=input_box(default=[9, 8, 8, 7, 10, 12, 11, 8, 8, 7, 6, 14, 10], label="conjunto"), '
            'auto_update=False',
        question='print "Calcule a moda para o seguinte conjunto de valores:"\n'
            'for i in l:\n'
            'print str(i) + " - ",\n'
            'print ""',
        solution='print "Solucao: A moda e " + str(max(set(l), key=l.count)) + "."')
s.save()
