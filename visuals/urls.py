from django.urls import path
from visuals.views import *
from visuals.qs import q6_viz, q6_static, q5_viz, q5_static, q7_viz, q7_static, q10_new, q10_static, q12_viz, q12_static, q17_viz, q17_static, q18_viz, q18_static, q28_viz, q28_static, q22_viz, q22_static, q23_viz, q23_static, q21_viz, q21_static, q11_viz, q11_static, q13_viz, q13_static, q26_viz, q26_static, gender_viz, race_viz

app_name = 'visuals'

urlpatterns = [
   path('',intro,name="intro"),
   path('Methodology',methods,name="methods"),
   path('Background',background,name="backgroundm"),
   path('Academics',academics,name="academics"),
   path('PostGrad',postgrad,name="postgrad"),
   path('Discrimination',discrimination,name="discrimination"),
   path('Belonging',belonging,name="belonging"),
   path('Conclusion',conclusion,name="conclusion"),
]
