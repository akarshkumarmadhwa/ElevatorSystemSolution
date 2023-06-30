from django.apps import AppConfig


class ElevatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'elevator'

    def ready(self):
        '''
        Running the another thread containing infinite loop to move elevator 
        Note:- Uncomment below code to move the elevators to serve the requests
        '''
        # from .move_elevators import RunThread
        # RunThread().start()
