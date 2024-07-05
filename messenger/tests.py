from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message

# Create your tests here.
class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', None, 'test1234')    #Aqui cargamos los datos de los usuarios
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')    #Usuario que no deberia existir en conversacion 1-1

        self.thread = Thread.objects.create()               #Aqui creamos objetos de los hilos


    #Caso para si se agregan los usuarios a los threads
    def test_add_users_to_thread(self):                     
        self.thread.users.add(self.user1, self.user2)       #Aqui agregamos los usuarios 1 y 2
        self.assertEqual(len(self.thread.users.all()), 2)   #Aqui comprobamos que se tengan 2 usuarios registrados


    #Recuperar un hilo ya existente a partir de sus usuarios
    def test_filter_thread_by_users(self):                  
        self.thread.users.add(self.user1, self.user2)       #Cada que se corre un test diferente se agregan los usuarios
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)  #Filtrado de usuarios
        self.assertEqual(self.thread, threads[0])           #Validacion de hilos en la posicion 1 y si son iguales


    #Comprobar que un hilo no existe cuando los usuarios no son parte de el
    def test_filter_non_existent_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0) 


    #Validar si los mensajes fueron enviados y su cantidad(len)
    def test_add_messages_to_thread(self):
        self.thread.users.add(self.user1, self.user2)         
        message1 = Message.objects.create(user=self.user1, content='Muy buenas')
        message2 = Message.objects.create(user=self.user2, content='Yo muy bien y tu que tal')
        self.thread.messages.add(message1, message2)
        self.assertEqual(len(self.thread.messages.all()), 2) 

        #Imprimir los mensajes con el nombre del usuario y su mensaje
        for message in self.thread.messages.all():
            print("({}): {}".format(message.user, message.content))


                    #Refactorizacion
    #Testeo de usuario que no esta en el hilo de la conversacion y que pueda añadir un mensaje
    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Muy buenas')
        message2 = Message.objects.create(user=self.user2, content='Yo muy bien y tu que tal')
        message3 = Message.objects.create(user=self.user3, content='Soy el usuario espia')
        self.thread.messages.add(message1, message2, message3)        #Se añade al hilo los 3 mensajes
        self.assertEqual(len(self.thread.messages.all()), 2)          #Validador que solo existen 2


    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, thread)
    
    def test_find_or_create_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_create(self.user1, self.user2)
        self.assertEqual(self.thread, thread)
        thread = Thread.objects.find_or_create(self.user1, self.user3)
        self.assertIsNotNone(thread)