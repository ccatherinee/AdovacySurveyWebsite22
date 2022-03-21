from django.urls import path
from dashreporting.views import *
from dashreporting.dash_apps import q6_viz, q5_viz, q7_viz, q10_new, q12_viz, q17_viz, q18_viz, q28_viz, q22_viz, q23_viz, q21_viz, q11_viz, q13_viz, q26_viz

app_name = 'dashreporting'

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
